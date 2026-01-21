"""
Management Reports Module
Contains all SQL queries and functions for generating management reports
"""

import data
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from datetime import datetime

# Configure matplotlib for Hebrew text support
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


def get_avg_tickets_per_flight():
    """
    Report 1: Average tickets per flight (for landed flights only)
    Returns the average number of tickets sold per landed flight
    """
    query = """
        SELECT AVG(flight_occupancy) AS avg_flight_occupancy
    FROM (
        SELECT 
            f.flight_id,
            COUNT(*) / COUNT(DISTINCT s.seat_row, s.seat_column) AS flight_occupancy
        FROM Flights f
            JOIN FlightTickets ft 
                ON f.flight_id = ft.flight_id
            JOIN Seats s
                ON f.plane_id = s.plane_id
        WHERE f.status = 'Landed'
        GROUP BY f.flight_id
    ) AS per_flight;

    """
    try:
        result = data.sql_query(query)
        return result[0][0] if result and result[0][0] is not None else 0
    except Exception as e:
        print(f"Error in get_avg_tickets_per_flight: {str(e)}")
        return 0


def get_revenue_by_class():
    """
    Report 2: Revenue by manufacturer, plane size, and class
    Returns total revenue breakdown by plane manufacturer, size, and seat class
    Only includes landed flights with active (non-cancelled) orders
    """
    query = """
        SELECT P.manufacturer AS Manufacturer, P.size AS Plane_Size, S.seat_class AS Class,
    SUM(
        CASE 
            WHEN O.order_status = 'Cancelled' THEN 
                0.05 * 
                CASE 
                    WHEN S.seat_class = 'Business' THEN IFNULL(F.price_business, 0)
                    ELSE F.price_economy
                END
            ELSE 
                CASE 
                    WHEN S.seat_class = 'Business' THEN IFNULL(F.price_business, 0)
                    ELSE F.price_economy
                END
        END
    ) AS Total_Revenue
    FROM FlightTickets FT
        JOIN Orders O ON FT.order_id = O.order_id
        JOIN Flights F ON FT.flight_id = F.flight_id
        JOIN Seats S ON FT.plane_id = S.plane_id  AND FT.seat_row = S.seat_row AND FT.seat_column = S.seat_column
        JOIN Planes P ON F.plane_id = P.plane_id
    WHERE F.status  <> 'Cancelled'    
    GROUP BY P.manufacturer, P.size, S.seat_class
    ORDER BY Total_Revenue DESC;
    """
    try:
        return data.sql_query(query)
    except Exception as e:
        print(f"Error in get_revenue_by_class: {str(e)}")
        return []


def get_employee_flight_hours():
    """
    Report 3: Cumulative flight hours by employees
    Returns flight hours for pilots and attendants, separated by short flights (<=6 hours) 
    and long flights (>6 hours)
    Only includes landed flights
    Returns a dictionary with 'pilots' and 'attendants' keys
    """
    pilots_query = """
        SELECT P.pilot_id, P.first_name_he, P.last_name_he,
            SUM(CASE WHEN FR.flight_duration <= 360 THEN FR.flight_duration ELSE 0 END) / 60.0 AS Short_Flight_Hours,
            SUM(CASE WHEN FR.flight_duration > 360 THEN FR.flight_duration ELSE 0 END) / 60.0 AS Long_Flight_Hours
        FROM Pilots P
        JOIN Pilots_In_Flights PIF ON P.pilot_id = PIF.pilot_id
        JOIN Flights F ON PIF.flight_id = F.flight_id
        JOIN FlightRoutes FR ON F.origin_airport_name = FR.origin_airport_name 
                             AND F.destination_airport_name = FR.destination_airport_name
        WHERE F.status = 'Landed'
        GROUP BY P.pilot_id, P.first_name_he, P.last_name_he
        ORDER BY (Short_Flight_Hours + Long_Flight_Hours) DESC
    """
    
    attendants_query = """
        SELECT A.attendant_id, A.first_name_he, A.last_name_he,
            SUM(CASE WHEN FR.flight_duration <= 360 THEN FR.flight_duration ELSE 0 END) / 60.0 AS Short_Flight_Hours,
            SUM(CASE WHEN FR.flight_duration > 360 THEN FR.flight_duration ELSE 0 END) / 60.0 AS Long_Flight_Hours
        FROM Attendants A
        JOIN Attendants_In_Flights AIF ON A.attendant_id = AIF.attendant_id
        JOIN Flights F ON AIF.flight_id = F.flight_id
        JOIN FlightRoutes FR ON F.origin_airport_name = FR.origin_airport_name 
                             AND F.destination_airport_name = FR.destination_airport_name
        WHERE F.status = 'Landed'
        GROUP BY A.attendant_id, A.first_name_he, A.last_name_he
        ORDER BY (Short_Flight_Hours + Long_Flight_Hours) DESC
    """
    
    try:
        pilots_data = data.sql_query(pilots_query) or []
        attendants_data = data.sql_query(attendants_query) or []
        return {
            'pilots': pilots_data,
            'attendants': attendants_data
        }
    except Exception as e:
        print(f"Error in get_employee_flight_hours: {str(e)}")
        return {'pilots': [], 'attendants': []}


def get_cancellation_rate_by_month():
    """
    Report 4: Cancellation rate by month
    Returns the percentage of cancelled orders grouped by year and month
    """
    query = """
        SELECT YEAR(order_date) AS Order_Year, MONTH(order_date) AS Order_Month,
    ROUND((SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0) 
        / COUNT(*), 2) AS Cancellation_Rate_Percent
    FROM Orders
    GROUP BY YEAR(order_date), MONTH(order_date)
    ORDER BY Order_Year DESC, Order_Month DESC;
    """
    try:
        return data.sql_query(query)
    except Exception as e:
        print(f"Error in get_cancellation_rate_by_month: {str(e)}")
        return []


def get_plane_monthly_activity():
    """
    Report 5: Monthly activity summary per plane
    Returns for each plane and month:
    - Number of executed flights (Landed)
    - Number of cancelled flights
    - Utilization percentage (flight duration / 43200 minutes per month)
    - Dominant route (most frequent route for that plane in that month)
    """
    query = """
        WITH Flights_By_Month AS (
    SELECT flight_id, plane_id, origin_airport_name, destination_airport_name, status,
        DATE(departure_date) AS dep_date,
        YEAR(departure_date) AS dep_year,
        MONTH(departure_date) AS dep_month
    FROM Flights
)

SELECT fbm.plane_id, fbm.dep_year AS Year, fbm.dep_month AS Month,
    SUM(CASE WHEN fbm.status = 'Landed' THEN 1 ELSE 0 END) AS Flights_Executed,
    SUM(CASE WHEN fbm.status = 'Cancelled' THEN 1 ELSE 0 END) AS Flights_Cancelled,
    ROUND(
        COUNT(DISTINCT CASE 
            WHEN fbm.status = 'Landed' THEN fbm.dep_date
        END) * 100.0 / 30, 2) AS Utilization_Percent,
    (
        SELECT GROUP_CONCAT(route SEPARATOR ', ')
        FROM (
            SELECT 
                CONCAT(f2.origin_airport_name, ' -> ', f2.destination_airport_name) AS route
            FROM Flights_By_Month f2
            WHERE f2.plane_id = fbm.plane_id
              AND f2.dep_year = fbm.dep_year
              AND f2.dep_month = fbm.dep_month
              AND f2.status = 'Landed'
            GROUP BY f2.origin_airport_name, f2.destination_airport_name
            HAVING COUNT(*) = (
                SELECT MAX(cnt)
                FROM (
                    SELECT COUNT(*) AS cnt
                    FROM Flights_By_Month f3
                    WHERE f3.plane_id = fbm.plane_id
                      AND f3.dep_year = fbm.dep_year
                      AND f3.dep_month = fbm.dep_month
                      AND f3.status = 'Landed'
                    GROUP BY f3.origin_airport_name, f3.destination_airport_name
                ) AS route_counts
            )
        ) AS dominant_routes
    ) AS Dominant_Routes

FROM Flights_By_Month fbm
GROUP BY fbm.plane_id, fbm.dep_year, fbm.dep_month
HAVING SUM(CASE WHEN fbm.status = 'Landed' THEN 1 ELSE 0 END) > 0
ORDER BY fbm.plane_id, Year, Month;
    """
    try:
        result = data.sql_query(query)
        return result if result else []
    except Exception as e:
        print(f"Error in get_plane_monthly_activity: {str(e)}")
        return []


def create_charts(reports_data):
    """
    Creates charts for all reports using seaborn
    Returns a dictionary with chart file paths
    """
    # Set style
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    
    charts = {}
    charts_dir = "static/charts"
    os.makedirs(charts_dir, exist_ok=True)
    
    # Chart 2: Revenue by class (grouped bar chart)
    if reports_data['revenue_by_class']:
        df = pd.DataFrame(reports_data['revenue_by_class'], 
                         columns=['Manufacturer', 'Plane_Size', 'Class', 'Total_Revenue'])
        plt.figure(figsize=(12, 6))
        df_pivot = df.pivot_table(values='Total_Revenue', index=['Manufacturer', 'Plane_Size'], 
                                  columns='Class', fill_value=0)
        # Create custom colors - New palette
        colors = []
        for col in df_pivot.columns:
            if col == 'Economy':
                colors.append('#EA7B7B')  # Economy color
            else:
                colors.append('#9E3B3B')  # Business color
        ax = df_pivot.plot(kind='bar', ax=plt.gca(), width=0.8, color=colors[:len(df_pivot.columns)])
        plt.xlabel('Manufacturer & Plane Size', fontsize=12, fontfamily='DejaVu Sans', fontweight='bold')
        plt.ylabel('Total Revenue ($)', fontsize=12, fontfamily='DejaVu Sans', fontweight='bold')
        plt.title('Revenue by Manufacturer, Plane Size, and Class', fontsize=14, fontweight='bold', fontfamily='DejaVu Sans')
        legend = plt.legend(title='Class', fontsize=10)
        legend.get_title().set_fontfamily('DejaVu Sans')
        for text in legend.get_texts():
            text.set_fontfamily('DejaVu Sans')
        plt.xticks(rotation=0, ha='center')  # Horizontal alignment, centered
        # Set font for all tick labels
        ax = plt.gca()
        for label in ax.get_xticklabels():
            label.set_fontfamily('DejaVu Sans')
        for label in ax.get_yticklabels():
            label.set_fontfamily('DejaVu Sans')
        plt.grid(axis='y', alpha=0.3)
        chart_path = f"{charts_dir}/chart2_revenue.png"
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        charts['revenue_by_class'] = chart_path.replace('static/', '')
    
    
    # Chart 4: Cancellation rate by month (line chart)
    if reports_data['cancellation_rates'] and len(reports_data['cancellation_rates']) > 0:
        # Convert to DataFrame - handle both list of tuples and list of lists
        data_list = reports_data['cancellation_rates']
        df = pd.DataFrame(data_list,
                         columns=['Order_Year', 'Order_Month', 'Cancellation_Rate_Percent'])
        
        # Convert to numeric first
        df['Order_Year'] = pd.to_numeric(df['Order_Year'], errors='coerce')
        df['Order_Month'] = pd.to_numeric(df['Order_Month'], errors='coerce')
        df['Cancellation_Rate_Percent'] = pd.to_numeric(df['Cancellation_Rate_Percent'], errors='coerce')
        
        # Remove any rows with NaN values
        df = df.dropna()
        
        if len(df) > 0:
            # Sort by year and month (ascending for chronological order)
            df = df.sort_values(['Order_Year', 'Order_Month'])
            
            # Create date objects for proper x-axis scaling
            df['Date'] = pd.to_datetime(df['Order_Year'].astype(int).astype(str) + '-' + 
                                       df['Order_Month'].astype(int).astype(str) + '-01')
            
            # Filter only rows with cancellation rate > 0
            df_non_zero = df[df['Cancellation_Rate_Percent'] > 0].copy()
            
            # Create complete date range from first date to last date
            min_date = df['Date'].min()
            max_date = df['Date'].max()
            # Generate all months in the range
            date_range = pd.date_range(start=min_date, end=max_date, freq='MS')
            
            plt.figure(figsize=(14, 6))
            
            # Plot vertical lines only for data points with cancellation rate > 0 (no connecting line)
            if len(df_non_zero) > 0:
                # Draw vertical lines from each point to X-axis
                for date, rate in zip(df_non_zero['Date'], df_non_zero['Cancellation_Rate_Percent']):
                    plt.plot([date, date], [0, rate], 
                            color='#c5283d', linewidth=2, zorder=3)
                # Plot points at the top of each vertical line
                plt.scatter(df_non_zero['Date'], df_non_zero['Cancellation_Rate_Percent'], 
                           s=60, color='#c5283d', marker='o', edgecolors='white', linewidths=1.5, zorder=4)
            
            plt.xlabel('Month', fontsize=12, fontweight='bold', fontfamily='DejaVu Sans')
            plt.ylabel('Cancellation Rate (%)', fontsize=12, fontweight='bold', fontfamily='DejaVu Sans')
            plt.title('Cancellation Rate by Month', fontsize=14, fontweight='bold', fontfamily='DejaVu Sans')
            plt.grid(alpha=0.3, linestyle='--', linewidth=0.8)
            plt.ylim(bottom=0)
            
            # Format x-axis to show all months
            ax = plt.gca()
            from matplotlib.dates import DateFormatter, MonthLocator
            # Set x-axis to show all months in range
            ax.xaxis.set_major_locator(MonthLocator(interval=1))
            ax.xaxis.set_major_formatter(DateFormatter('%m/%Y'))
            plt.xticks(rotation=45, ha='right')
            
            # Set font for all tick labels
            for label in ax.get_xticklabels():
                label.set_fontfamily('DejaVu Sans')
            for label in ax.get_yticklabels():
                label.set_fontfamily('DejaVu Sans')
            
            plt.tight_layout()
            chart_path = f"{charts_dir}/chart4_cancellation_rate.png"
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            charts['cancellation_rates'] = chart_path.replace('static/', '')
    
    # Chart 5: Plane activity dashboard
    if reports_data['plane_activity']:
        df = pd.DataFrame(reports_data['plane_activity'],
                         columns=['Plane_ID', 'Year', 'Month', 'Flights_Executed', 
                                 'Flights_Cancelled', 'Utilization_Percent', 'Dominant_Route'])
        # Convert to numeric
        df['Flights_Executed'] = pd.to_numeric(df['Flights_Executed'], errors='coerce').fillna(0)
        df['Flights_Cancelled'] = pd.to_numeric(df['Flights_Cancelled'], errors='coerce').fillna(0)
        df['Utilization_Percent'] = pd.to_numeric(df['Utilization_Percent'], errors='coerce').fillna(0)
        
        # Aggregate data by plane (sum flights, average utilization, get most recent dominant route)
        df_agg = df.groupby('Plane_ID').agg({
            'Flights_Executed': 'sum',
            'Flights_Cancelled': 'sum',
            'Utilization_Percent': 'mean',  # Average utilization across months
            'Dominant_Route': lambda x: x[x.notna() & (x != '') & (x != 'NULL')].iloc[-1] if len(x[x.notna() & (x != '') & (x != 'NULL')]) > 0 else None  # Get most recent non-null route
        }).reset_index()
        
        df_agg = df_agg.sort_values('Plane_ID')
        
        # Create dashboard with 3 subplots - proportional sizes
        fig = plt.figure(figsize=(24, 8))
        gs = fig.add_gridspec(1, 3, width_ratios=[1.2, 1.2, 1.6], wspace=0.4)  # Enlarged right graph and shifted left
        
        # 1. Grouped vertical bar chart for flights (Plane ID on X-axis)
        # Use separate query data for this chart
        ax1 = fig.add_subplot(gs[0, 0])
        if reports_data.get('flights_by_plane') and len(reports_data['flights_by_plane']) > 0:
            df_flights = pd.DataFrame(reports_data['flights_by_plane'],
                                     columns=['Plane_ID', 'Flights_Executed', 'Flights_Cancelled'])
            df_flights['Plane_ID'] = pd.to_numeric(df_flights['Plane_ID'], errors='coerce')
            df_flights['Flights_Executed'] = pd.to_numeric(df_flights['Flights_Executed'], errors='coerce').fillna(0)
            df_flights['Flights_Cancelled'] = pd.to_numeric(df_flights['Flights_Cancelled'], errors='coerce').fillna(0)
            df_flights = df_flights.sort_values('Plane_ID')
            planes_chart1 = df_flights['Plane_ID'].astype(str)
            executed_chart1 = df_flights['Flights_Executed'].astype(int)
            cancelled_chart1 = df_flights['Flights_Cancelled'].astype(int)
        else:
            # Fallback to aggregated data if new query fails
            planes_chart1 = df_agg['Plane_ID'].astype(str)
            executed_chart1 = df_agg['Flights_Executed'].astype(int)
            cancelled_chart1 = df_agg['Flights_Cancelled'].astype(int)
        
        x_pos_chart1 = range(len(planes_chart1))
        width = 0.35  # Width of bars
        x1 = [x - width/2 for x in x_pos_chart1]
        x2 = [x + width/2 for x in x_pos_chart1]
        
        ax1.bar(x1, executed_chart1, width, label='Flights Executed', color='#215E61', edgecolor='black', linewidth=0.5)
        ax1.bar(x2, cancelled_chart1, width, label='Flights Cancelled', color='#9E2A3A', edgecolor='black', linewidth=0.5)
        
        ax1.set_xticks(x_pos_chart1)
        ax1.set_xticklabels(planes_chart1, fontfamily='DejaVu Sans')
        ax1.set_xlabel('Plane ID', fontsize=12, fontweight='bold', fontfamily='DejaVu Sans')
        ax1.set_ylabel('Number of Flights', fontsize=12, fontweight='bold', fontfamily='DejaVu Sans')
        ax1.set_title('Monthly Flight Activity by Plane', fontsize=14, fontweight='bold', fontfamily='DejaVu Sans', pad=15)
        legend1 = ax1.legend(loc='upper right', fontsize=10)
        legend1.get_frame().set_facecolor('white')
        for text in legend1.get_texts():
            text.set_fontfamily('DejaVu Sans')
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        # Set Y-axis to show only integers
        ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        # Set font for all tick labels
        for label in ax1.get_xticklabels():
            label.set_fontfamily('DejaVu Sans')
        for label in ax1.get_yticklabels():
            label.set_fontfamily('DejaVu Sans')
        
        # 2. Utilization visualization (vertical bars, Plane ID on X-axis)
        ax2 = fig.add_subplot(gs[0, 1])
        utilization = df_agg['Utilization_Percent'].clip(0, 100)
        
        # Set y-axis to always show 0-100%
        y_max = 100
        
        # Use planes from df_agg for this chart
        planes_chart2 = df_agg['Plane_ID'].astype(str)
        x_pos_chart2 = range(len(planes_chart2))
        
        # Create vertical bar chart for utilization - New palette
        colors_util = ['#ffc857' if u >= 50 else '#e9724c' if u >= 25 else '#ABDADC' for u in utilization]
        bars = ax2.bar(x_pos_chart2, utilization, color=colors_util, width=0.6, edgecolor='black', linewidth=0.5)
        
        # Add percentage labels on bars (always visible)
        for i, (bar, util) in enumerate(zip(bars, utilization)):
            height = bar.get_height()
            label_y = height + (y_max * 0.02)  # 2% of max above bar
            ax2.text(bar.get_x() + bar.get_width()/2, label_y, 
                    f'{util:.2f}%', ha='center', va='bottom', fontsize=10, fontweight='bold', fontfamily='DejaVu Sans')
        
        ax2.set_xticks(x_pos_chart2)
        ax2.set_xticklabels(planes_chart2, fontfamily='DejaVu Sans')
        ax2.set_xlabel('Plane ID', fontsize=12, fontweight='bold', fontfamily='DejaVu Sans')
        ax2.set_ylabel('Utilization (%)', fontsize=12, fontweight='bold', fontfamily='DejaVu Sans')
        ax2.set_title('Monthly Utilization Rate', fontsize=14, fontweight='bold', fontfamily='DejaVu Sans', pad=15)
        ax2.set_ylim(0, y_max)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        # Set font for all tick labels
        for label in ax2.get_xticklabels():
            label.set_fontfamily('DejaVu Sans')
        for label in ax2.get_yticklabels():
            label.set_fontfamily('DejaVu Sans')
        
        # 3. Dominant routes table (text visualization)
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.axis('off')
        ax3.set_title('Dominant Routes', fontsize=14, fontweight='bold', pad=15, fontfamily='DejaVu Sans')  # Same font and pad as other titles
        
        # Create table data - only planes with valid routes (no N/A)
        table_data = []
        for _, row in df_agg.iterrows():
            route = row['Dominant_Route']
            # Only include planes with valid routes (not NaN, not None, not empty string, not NULL)
            if not (pd.isna(route) or route is None or route == '' or route == 'NULL' or str(route).strip() == ''):
                route = str(route).strip()
                table_data.append([f"Plane {row['Plane_ID']}", route])
        
        # Only create table if there's data
        if table_data:
            # Create table - improved design with centered text and wider columns
            table = ax3.table(cellText=table_data,
                             colLabels=['Plane', 'Route'],
                             cellLoc='center',  # Changed from 'left' to 'center'
                             loc='center',
                             bbox=[0.02, 0, 0.96, 1])  # Wider table: [left, bottom, width, height] - reduced margins for more width
            table.auto_set_font_size(False)
            table.set_fontsize(16)
            table.scale(1.8, 3.2)  # Increased horizontal scale to make columns wider (was 1, now 1.8)
            # Set column widths - make Plane column wider
            col_widths = [0.3, 0.7]  # Plane column 30%, Route column 70%
            for i in range(2):
                for j in range(len(table_data) + 1):
                    cell = table[(j, i)]
                    cell.set_width(col_widths[i])
            
            # Style table with improved design
            for i in range(len(table_data) + 1):
                for j in range(2):
                    cell = table[(i, j)]
                    if i == 0:  # Header
                        cell.set_facecolor('#3F9AAE')  # Blue color
                        cell.set_text_props(weight='bold', color='white', size=17, family='DejaVu Sans')  # Same font as main titles
                        cell.set_height(0.1)
                    else:
                        # Alternating row colors for better readability
                        bg_color = '#f8fafc' if i % 2 == 0 else 'white'
                        cell.set_facecolor(bg_color)
                        cell.set_text_props(size=15, weight='bold', family='DejaVu Sans')  # Same font as main titles
                        cell.set_height(0.09)
                    # Better borders
                    cell.set_edgecolor('#cbd5e1')
                    cell.set_linewidth(1.2)
        else:
            # No data message
            ax3.text(0.5, 0.5, 'No route data available', 
                    ha='center', va='center', fontsize=16, color='#64748b', style='italic', weight='bold', family='DejaVu Sans')  # Same font
        
        plt.suptitle('Monthly Plane Activity Dashboard', fontsize=16, fontweight='bold', y=0.98, fontfamily='DejaVu Sans')
        
        chart_path = f"{charts_dir}/chart5_plane_activity.png"
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        charts['plane_activity'] = chart_path.replace('static/', '')
    
    return charts


def get_total_orders():
    """
    Returns the total number of orders
    """
    query = """
        SELECT COUNT(*) as total_orders
        FROM Orders
    """
    try:
        result = data.sql_query(query)
        return result[0][0] if result and result[0][0] is not None else 0
    except Exception as e:
        print(f"Error in get_total_orders: {str(e)}")
        return 0


def get_active_flights():
    """
    Returns the total number of active flights
    """
    query = """
        SELECT COUNT(*) as active_flights
        FROM Flights
        WHERE status = 'Active'
    """
    try:
        result = data.sql_query(query)
        return result[0][0] if result and result[0][0] is not None else 0
    except Exception as e:
        print(f"Error in get_active_flights: {str(e)}")
        return 0


def get_total_passengers():
    """
    Returns the total number of passengers (tickets sold)
    """
    query = """
        SELECT COUNT(*) as total_passengers
        FROM FlightTickets
    """
    try:
        result = data.sql_query(query)
        return result[0][0] if result and result[0][0] is not None else 0
    except Exception as e:
        print(f"Error in get_total_passengers: {str(e)}")
        return 0


def get_flights_by_plane():
    """
    Returns flights executed and cancelled by plane (for chart display only)
    This is a separate query specifically for the left chart in plane activity dashboard
    """
    query = """
        SELECT 
            plane_id,
            SUM(CASE WHEN status = 'Landed' THEN 1 ELSE 0 END) AS Flights_Executed,
            SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS Flights_Cancelled
        FROM Flights
        GROUP BY plane_id
        ORDER BY plane_id;
    """
    try:
        result = data.sql_query(query)
        return result if result else []
    except Exception as e:
        print(f"Error in get_flights_by_plane: {str(e)}")
        return []


def get_all_reports():
    """
    Executes all report queries and returns a dictionary with all report data
    """
    return {
        'avg_tickets': get_avg_tickets_per_flight(),
        'revenue_by_class': get_revenue_by_class(),
        'employee_hours': get_employee_flight_hours(),
        'cancellation_rates': get_cancellation_rate_by_month(),
        'plane_activity': get_plane_monthly_activity(),
        'flights_by_plane': get_flights_by_plane(),  # New query for left chart
        'total_orders': get_total_orders(),
        'active_flights': get_active_flights(),
        'total_passengers': get_total_passengers()
    }

