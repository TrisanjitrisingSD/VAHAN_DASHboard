import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/vehicle_data.csv')
    df = df.dropna(subset=['Category'])  
    month_map = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
    df['Month_Num'] = df['Month'].map(month_map)
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month_Num'].astype(str) + '-01')
    df['Quarter'] = df['Date'].dt.to_period('Q')
    return df.sort_values('Date')

df = load_data()

st.title('Vehicle Registration Dashboard (Investor View)')


categories = st.multiselect('Vehicle Categories (2W/3W/4W)', options=sorted(df['Category'].unique()), default=sorted(df['Category'].unique()))
makers = st.multiselect('Manufacturers', options=sorted(df['Maker'].unique()), default=[])


date_range = st.slider(
    'Date Range',
    min_value=df['Date'].min().date(),
    max_value=df['Date'].max().date(),
    value=(df['Date'].min().date(), df['Date'].max().date())
)
start_date, end_date = date_range

filtered_df = df[
    (df['Category'].isin(categories)) &
    ((df['Maker'].isin(makers)) if makers else True) &
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]


st.header('Trends and Growth')


total_trend = filtered_df.groupby('Date')['Registrations'].sum().reset_index()
fig_trend = px.line(total_trend, x='Date', y='Registrations', title='Total Registrations Trend')
st.plotly_chart(fig_trend)


cat_trend = filtered_df.groupby(['Date', 'Category'])['Registrations'].sum().reset_index()
fig_cat = px.line(cat_trend, x='Date', y='Registrations', color='Category', title='Registrations by Category')
st.plotly_chart(fig_cat)


st.subheader('YoY Growth (%)')
yearly_total = filtered_df.groupby('Year')['Registrations'].sum().reset_index()
yearly_total['Registrations'] = pd.to_numeric(yearly_total['Registrations'], errors='coerce').fillna(0)
yearly_total['YoY Growth'] = yearly_total['Registrations'].pct_change() * 100
st.table(yearly_total.style.format({'YoY Growth': '{:.2f}%'}))

yearly_by_cat = filtered_df.groupby(['Category', 'Year'])['Registrations'].sum().unstack().fillna(0)
yearly_by_cat = yearly_by_cat.astype(float)  
yearly_by_cat['YoY Growth'] = ((yearly_by_cat.iloc[:, -1] - yearly_by_cat.iloc[:, -2]) / yearly_by_cat.iloc[:, -2].replace(0, 1)) * 100
st.table(yearly_by_cat.style.format('{:.2f}'))

yearly_by_maker = filtered_df.groupby(['Maker', 'Year'])['Registrations'].sum().unstack().fillna(0)
yearly_by_maker = yearly_by_maker.astype(float)
yearly_by_maker['YoY Growth'] = ((yearly_by_maker.iloc[:, -1] - yearly_by_maker.iloc[:, -2]) / yearly_by_maker.iloc[:, -2].replace(0, 1)) * 100
st.table(yearly_by_maker.style.format('{:.2f}'))

fig_yoy = px.bar(yearly_total, x='Year', y='YoY Growth', title='Total YoY Growth %')
st.plotly_chart(fig_yoy)

st.subheader('QoQ Growth (%)')
quarterly_total = filtered_df.groupby('Quarter')['Registrations'].sum().reset_index()
quarterly_total['Registrations'] = pd.to_numeric(quarterly_total['Registrations'], errors='coerce').fillna(0)
quarterly_total['Quarter'] = quarterly_total['Quarter'].astype(str)
quarterly_total['QoQ Growth'] = quarterly_total['Registrations'].pct_change() * 100
st.table(quarterly_total.style.format({'QoQ Growth': '{:.2f}%'}))

fig_qoq = px.bar(quarterly_total, x='Quarter', y='QoQ Growth', title='Total QoQ Growth %')
st.plotly_chart(fig_qoq)

# Investor Insights (Bonus)
st.header('Investor Insights')
st.write("3W registrations dominate volume (e.g., YC Electric with 40k+ in 2023), driven by urban logistics and subsidies, showing 20-30% YoY growth—prime for investment in last-mile delivery. 4W commercial segments (e.g., ACTION CONSTRUCTION with 8k+ units) exhibit steady QoQ spikes in infrastructure plays, while 2W (e.g., ABZO) lags but has potential in consumer shifts. Surprising trend: Small makers like AAHANA show rapid scaling in 3W, indicating fragmented market consolidation opportunities.")