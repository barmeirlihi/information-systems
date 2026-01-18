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
        SELECT AVG(ct.count_tickets) as avg_count_tickets
        FROM (
            SELECT f.flight_id, COUNT(*) as count_tickets
            FROM Flights as f
            JOIN FlightTickets as ft ON f.flight_id = ft.flight_id
            WHERE f.status = 'Landed'
            GROUP BY f.flight_id
        ) as ct
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
            SUM(CASE 
                    WHEN S.seat_class = 'Business' THEN IFNULL(F.price_business, 0)
                    ELSE F.price_economy 
                END) AS Total_Revenue
        FROM FlightTickets FT
            JOIN Orders as O ON FT.order_id = O.order_id
            JOIN Flights F ON FT.flight_id = F.flight_id
            JOIN Seats S ON FT.plane_id = S.plane_id 
                AND FT.seat_row = S.seat_row 
                AND FT.seat_column = S.seat_column
            JOIN Planes P ON F.plane_id = P.plane_id
        WHERE F.status = 'Landed' AND O.order_status <> 'Cancelled'    
        GROUP BY P.manufacturer, P.size, S.seat_class
        ORDER BY P.manufacturer, P.size, Total_Revenue DESC
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
        ORDER BY Order_Year DESC, Order_Month DESC
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
        SELECT F.plane_id,YEAR(F.departure_date) AS Year, MONTH(F.departure_date) AS Month,
    -- נתונים רגילים
    SUM(CASE WHEN F.status = 'Landed' THEN 1 ELSE 0 END) AS Flights_Executed,
    SUM(CASE WHEN F.status = 'Cancelled' THEN 1 ELSE 0 END) AS Flights_Cancelled,
    -- חישוב ניצולת 
    ROUND(
        (SUM(CASE WHEN F.status = 'Landed' THEN FR.flight_duration ELSE 0 END) * 100.0) 
        / 43200, 
    2) AS Utilization_Percent,
    -- מציאת המסלול השולט (לפי כל הטיסות שבוצעו)
    (
        SELECT CONCAT(inner_F.origin_airport_name, ' -> ', inner_F.destination_airport_name)
        FROM Flights inner_F
        WHERE inner_F.plane_id = F.plane_id
          AND inner_F.status = 'Landed'
        GROUP BY inner_F.origin_airport_name, inner_F.destination_airport_name
        ORDER BY COUNT(*) DESC  -- סדר לפי הכמות הגבוהה ביותר
        LIMIT 1
    ) AS Dominant_Route
FROM Flights F
    JOIN FlightRoutes FR ON F.origin_airport_name = FR.origin_airport_name 
		AND F.destination_airport_name = FR.destination_airport_name
GROUP BY F.plane_id, YEAR(F.departure_date), MONTH(F.departure_date)
ORDER BY F.plane_id, Year, Month;
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
                colors.append('#ffc857')  # Golden pollen for Economy
            else:
                colors.append('#255f85')  # Baltic blue for Business
        ax = df_pivot.plot(kind='bar', ax=plt.gca(), width=0.8, color=colors[:len(df_pivot.columns)])
        plt.xlabel('Manufacturer & Plane Size', fontsize=12)
        plt.ylabel('Total Revenue ($)', fontsize=12)
        plt.title('Revenue by Manufacturer, Plane Size, and Class', fontsize=14, fontweight='bold')
        plt.legend(title='Class', fontsize=10)
        plt.xticks(rotation=0, ha='center')  # Horizontal alignment, centered
        plt.grid(axis='y', alpha=0.3)
        chart_path = f"{charts_dir}/chart2_revenue.png"
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        charts['revenue_by_class'] = chart_path.replace('static/', '')
    
    
    # Chart 4: Cancellation rate by month (line chart)
    if reports_data['cancellation_rates']:
        df = pd.DataFrame(reports_data['cancellation_rates'],
                         columns=['Order_Year', 'Order_Month', 'Cancellation_Rate_Percent'])
        # Convert to numeric first
        df['Order_Year'] = pd.to_numeric(df['Order_Year'], errors='coerce')
        df['Order_Month'] = pd.to_numeric(df['Order_Month'], errors='coerce')
        # Create date string and convert to datetime
        df['Date'] = pd.to_datetime(df['Order_Year'].astype(str) + '-' + 
                                    df['Order_Month'].astype(str) + '-01')
        df = df.sort_values('Date')
        
        # Create a complete date range from first date to end of 2026
        if len(df) > 0:
            min_date = df['Date'].min()
            max_date = pd.to_datetime('2026-12-01')
            # Generate all months in the range
            date_range = pd.date_range(start=min_date, end=max_date, freq='MS')
            # Create a complete dataframe with all months
            complete_df = pd.DataFrame({'Date': date_range})
            # Merge with actual data
            df_complete = complete_df.merge(df[['Date', 'Cancellation_Rate_Percent']], 
                                          on='Date', how='left')
            df_complete['Cancellation_Rate_Percent'] = df_complete['Cancellation_Rate_Percent'].fillna(0)
        else:
            df_complete = df
        
        plt.figure(figsize=(14, 7))
        # Draw vertical lines from points to X-axis
        for date, rate in zip(df_complete['Date'], df_complete['Cancellation_Rate_Percent']):
            plt.plot([date, date], [0, rate], color='#c5283d', alpha=0.3, linewidth=0.8, linestyle='--', zorder=1)
        # Plot points
        plt.scatter(df_complete['Date'], df_complete['Cancellation_Rate_Percent'], 
                   s=80, color='#c5283d', marker='o', edgecolors='white', linewidths=2, zorder=3)
        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Cancellation Rate (%)', fontsize=12, fontweight='bold')
        plt.title('Cancellation Rate by Month', fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3, linestyle='--', linewidth=0.8)
        plt.ylim(bottom=0)
        # Format x-axis to show year-month
        ax = plt.gca()
        # Use MonthLocator for monthly ticks
        from matplotlib.dates import MonthLocator, DateFormatter
        ax.xaxis.set_major_locator(MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
        plt.xticks(rotation=45, ha='right')
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
        
        # Create dashboard with 3 subplots - larger size
        fig = plt.figure(figsize=(22, 16))
        gs = fig.add_gridspec(2, 2, height_ratios=[2.5, 1.2], width_ratios=[2.2, 1], hspace=0.4, wspace=0.5)
        
        # 1. Grouped vertical bar chart for flights (Plane ID on X-axis)
        ax1 = fig.add_subplot(gs[0, :])
        planes = df_agg['Plane_ID'].astype(str)
        executed = df_agg['Flights_Executed'].astype(int)
        cancelled = df_agg['Flights_Cancelled'].astype(int)
        
        x_pos = range(len(planes))
        width = 0.35  # Width of bars
        x1 = [x - width/2 for x in x_pos]
        x2 = [x + width/2 for x in x_pos]
        
        ax1.bar(x1, executed, width, label='Flights Executed', color='#ffc857', edgecolor='black', linewidth=0.5)
        ax1.bar(x2, cancelled, width, label='Flights Cancelled', color='#c5283d', edgecolor='black', linewidth=0.5)
        
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(planes)
        ax1.set_xlabel('Plane ID', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Number of Flights', fontsize=12, fontweight='bold')
        ax1.set_title('Monthly Flight Activity by Plane', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper right', fontsize=10)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        # Set Y-axis to show only integers
        ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        # 2. Utilization visualization (vertical bars, Plane ID on X-axis)
        ax2 = fig.add_subplot(gs[1, 0])
        utilization = df_agg['Utilization_Percent'].clip(0, 100)
        
        # Determine max utilization for better scaling
        max_util = max(utilization.max(), 10) if len(utilization) > 0 else 100
        y_max = min(max_util * 1.2, 100)  # Add 20% padding but cap at 100
        
        # Create vertical bar chart for utilization - New palette
        colors_util = ['#ffc857' if u >= 50 else '#e9724c' if u >= 25 else '#c5283d' for u in utilization]
        bars = ax2.bar(x_pos, utilization, color=colors_util, width=0.6, edgecolor='black', linewidth=0.5)
        
        # Add percentage labels on bars (always visible)
        for i, (bar, util) in enumerate(zip(bars, utilization)):
            height = bar.get_height()
            label_y = height + (y_max * 0.02)  # 2% of max above bar
            ax2.text(bar.get_x() + bar.get_width()/2, label_y, 
                    f'{util:.2f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(planes)
        ax2.set_xlabel('Plane ID', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Utilization (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Monthly Utilization Rate', fontsize=13, fontweight='bold')
        ax2.set_ylim(0, y_max)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add reference lines only if they're within the visible range
        if y_max >= 50:
            ax2.axhline(y=50, color='gray', linestyle=':', alpha=0.5, linewidth=1, label='50%')
        if y_max >= 75:
            ax2.axhline(y=75, color='gray', linestyle=':', alpha=0.5, linewidth=1, label='75%')
        
        # 3. Dominant routes table (text visualization)
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.axis('off')
        ax3.set_title('Dominant Routes', fontsize=13, fontweight='bold', pad=10)
        
        # Create table data
        table_data = []
        for _, row in df_agg.iterrows():
            route = row['Dominant_Route']
            # Check if route is valid (not NaN, not None, not empty string)
            if pd.isna(route) or route is None or route == '' or route == 'NULL' or str(route).strip() == '':
                route = 'N/A'
            else:
                route = str(route).strip()
            table_data.append([f"Plane {row['Plane_ID']}", route])
        
        # Create table - larger
        table = ax3.table(cellText=table_data,
                         colLabels=['Plane', 'Route'],
                         cellLoc='left',
                         loc='center',
                         colWidths=[0.25, 0.75])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2.5)
        
        # Style table
        for i in range(len(table_data) + 1):
            for j in range(2):
                cell = table[(i, j)]
                if i == 0:  # Header
                    cell.set_facecolor('#255f85')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f8f9fa' if i % 2 == 0 else 'white')
                cell.set_edgecolor('#dee2e6')
                cell.set_height(0.08)
        
        plt.suptitle('Monthly Plane Activity Dashboard', fontsize=16, fontweight='bold', y=0.98)
        
        chart_path = f"{charts_dir}/chart5_plane_activity.png"
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        charts['plane_activity'] = chart_path.replace('static/', '')
    
    return charts


def get_all_reports():
    """
    Executes all report queries and returns a dictionary with all report data
    """
    return {
        'avg_tickets': get_avg_tickets_per_flight(),
        'revenue_by_class': get_revenue_by_class(),
        'employee_hours': get_employee_flight_hours(),
        'cancellation_rates': get_cancellation_rate_by_month(),
        'plane_activity': get_plane_monthly_activity()
    }

