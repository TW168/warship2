from django.shortcuts import render
from .utils.db_utils import fetch_from_db
import plotly.express as px
from plotly.offline import plot
import pandas as pd
import numpy as np
import calendar
import plotly.graph_objects as go

def warehouse_dashboard(request):
    # Hourly Stacker Stats
    query_stacker = """
    SELECT stacker, height, status, COUNT(*) AS count, scraped_dt
    FROM warship2_db.hourly_all_cells
    GROUP BY stacker, status, height, scraped_dt
    ORDER BY stacker, status
    """
    df_stacker = fetch_from_db(query_stacker)
    max_dt = df_stacker['scraped_dt'].max()

    stacker_charts = []
    custom_order = ['Empty', 'Couple', '48 inch', '96 inch', 'Disabled', 'Not used', '9', '12', 'Duplicate', 'Engaged']

    if not df_stacker.empty:  # Ensure data is not empty
        for stacker in df_stacker['stacker'].unique():
            stacker_data = df_stacker[df_stacker['stacker'] == stacker]
            if not stacker_data.empty:  # Ensure stacker data is not empty
                fig = px.pie(
                    stacker_data,
                    values='count',
                    names='status',
                    title=f"Stacker {stacker} Status Distribution",
                    category_orders={'status': custom_order}
                )
                stacker_charts.append(plot(fig, output_type='div'))

    # ASH Event Heatmap
    query_heatmap = """
    SELECT event_date, description, COUNT(*) AS total_count
    FROM event
    GROUP BY event_date, description
    """
    df_heatmap = fetch_from_db(query_heatmap)
    df_pivot = df_heatmap.pivot_table(
        index='description',
        columns='event_date',
        values='total_count',
        fill_value=0
    )
    fig_heatmap = px.imshow(
        df_pivot,
        labels=dict(x="Event Date", y="Description", color="Total Count"),
        title="ASH Event Heatmap",
        color_continuous_scale='Blues'
    )
    heatmap_div = plot(fig_heatmap, output_type='div')

    # Monthly Trends of Pallet Entry
    df = pd.read_excel(r"D:\Shipping_Daily_Report\DAILY_DATA_AUTO_WAREHOUSE_All.xlsx")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    years = df['Year'].unique()
    fpp_data = []
    for year in years:
        year_data = df[df['Year'] == year]
        monthly_data = [
            {
                'Month': month,
                'Year': year,
                'Pallet Entry': year_data.loc[year_data['Month'] == month, 'Pallet Entry'].sum()
            }
            for month in range(1, 13)
        ]
        fpp_data.append(pd.DataFrame(monthly_data))

    fpp_df = pd.concat(fpp_data)
    fig1 = px.line(
        fpp_df,
        x='Month',
        y='Pallet Entry',
        color='Year',
        title='Monthly Trends of Pallet Entry',
        labels={'Month': 'Month', 'Pallet Entry': 'Pallet Entry'},
        markers=True
    )
    fig1.update_xaxes(
        tickvals=np.arange(1, 13),
        ticktext=[calendar.month_abbr[i] for i in range(1, 13)]
    )
    chart1 = plot(fig1, output_type='div')

    # Cumulative Over/Underproduction Trends
    df_monthly = df.resample('MS', on='Date').sum()
    df_monthly['Month-Year'] = df_monthly.index.to_period('M').strftime('%b-%Y')
    df_monthly['Over/underproduce'] = df_monthly['Pallet Entry'] - df_monthly['Pallet Shipped']
    df_monthly['Cumulative Over/underproduce'] = df_monthly['Over/underproduce'].cumsum()

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=df_monthly['Month-Year'],
            y=df_monthly['Cumulative Over/underproduce'],
            name='Cumulative Over/underproduce',
            line=dict(color='blue')
        )
    )
    fig2.update_layout(
        title="Cumulative Over/Underproduction Trends",
        xaxis_title="Date",
        yaxis=dict(
            title="Cumulative Over/underproduce",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue")
        ),
        xaxis=dict(tickangle=-45)
    )
    chart2 = plot(fig2, output_type='div')

    return render(request, 'warehouse/dashboard.html', {
        'max_dt': max_dt,
        'stacker_charts': stacker_charts,
        'heatmap_div': heatmap_div,
        'chart1': chart1,
        'chart2': chart2,
    })
