import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SFPRIS Demo", page_icon="pipeline", layout="wide")
st.title("Seismic-Fault Pipeline Risk Intelligence System")
st.markdown("SFPRIS - Predicting pipeline incident risk across the US using ML and geospatial data.")
st.warning("This is a demo version with 500 sample incidents. Full dataset has 7,958 incidents across 49 states.")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/sonawane-gopal/Seismic-Fault-Pipeline-Risk-Intelligence-System/main/sample_data.csv"
    return pd.read_csv(url)

df = load_data()
st.success("Data loaded: " + str(df.shape[0]) + " sample incidents")

st.info("""
**What is a Significant Incident?**
A pipeline incident is SIGNIFICANT if it causes:
- Fatality or hospitalization
- Fire or explosion  
- Property damage over $50,000
- Major liquid or gas spill
""")
# Sidebar filters
st.sidebar.header("Filters")
pipe_type = st.sidebar.selectbox("Pipeline Type", ['All', 'hazardous_liquid', 'gas'])
states = ['All'] + sorted(df['ONSHORE_ST'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("State", states)
cause_list = ['All'] + sorted(df['CAUSE'].dropna().unique().tolist())
selected_cause = st.sidebar.selectbox("Cause", cause_list)

# Filter data
filtered_df = df.copy()
if pipe_type != 'All':
    filtered_df = filtered_df[filtered_df['pipe_type'] == pipe_type]
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['ONSHORE_ST'] == selected_state]
if selected_cause != 'All':
    filtered_df = filtered_df[filtered_df['CAUSE'] == selected_cause]

# KPI metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", filtered_df.shape[0])
col2.metric("Significant Incidents", (filtered_df['SIGNIFICAN'] == 'YES').sum())
col3.metric("Avg Fault Distance (km)", str(round(filtered_df['HubDist'].mean()/1000, 1)))
col4.metric("Avg Earthquake Count", str(round(filtered_df['eq_count'].mean(), 1)))

# Map
st.subheader("Incident Map")
basemap = st.selectbox("Select Basemap", ["open-street-map", "carto-positron", "carto-darkmatter"])
map_df = filtered_df.dropna(subset=['latitude', 'longitude'])
fig = px.scatter_mapbox(
    map_df, lat='latitude', lon='longitude',
    color='SIGNIFICAN', size='TOTAL_COST', size_max=15,
    hover_name='CAUSE',
    hover_data={
        'ONSHORE_ST': True, 'TOTAL_COST': True, 'eq_count': True,
        'eq_max_mag': True, 'HubDist': True, 'pipe_type': True,
        'latitude': False, 'longitude': False
    },
    color_discrete_map={'YES': 'red', 'NO': 'green'},
    zoom=3, height=600
)
fig.update_layout(mapbox_style=basemap, margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

# Charts
st.subheader("Statistical Analysis")
col1, col2 = st.columns(2)

with col1:
    state_counts = filtered_df.groupby('ONSHORE_ST').size().reset_index(name='count')
    state_counts = state_counts.sort_values('count', ascending=False).head(15)
    fig1 = px.bar(state_counts, x='ONSHORE_ST', y='count', title='Top 15 States by Incident Count', color='count', color_continuous_scale='reds')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    cause_counts = filtered_df.groupby('CAUSE').size().reset_index(name='count')
    cause_counts = cause_counts.sort_values('count', ascending=False)
    fig2 = px.bar(cause_counts, x='count', y='CAUSE', title='Incidents by Cause', orientation='h', color='count', color_continuous_scale='oranges')
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    sig_state = filtered_df.groupby(['ONSHORE_ST', 'SIGNIFICAN']).size().reset_index(name='count')
    sig_state = sig_state[sig_state['ONSHORE_ST'].isin(state_counts['ONSHORE_ST'])]
    fig3 = px.bar(sig_state, x='ONSHORE_ST', y='count', color='SIGNIFICAN', title='Significant vs Non-Significant by State', color_discrete_map={'YES': 'red', 'NO': 'green'}, barmode='stack')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    year_counts = filtered_df.groupby('IYEAR').size().reset_index(name='count')
    fig4 = px.line(year_counts, x='IYEAR', y='count', title='Incidents by Year', markers=True)
    st.plotly_chart(fig4, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    sig_counts = filtered_df['SIGNIFICAN'].value_counts().reset_index()
    sig_counts.columns = ['Significant', 'Count']
    fig5 = px.pie(sig_counts, names='Significant', values='Count', title='Significant vs Non-Significant', color='Significant', color_discrete_map={'YES': 'red', 'NO': 'green'})
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    cost_sig = filtered_df.groupby('SIGNIFICAN')['TOTAL_COST'].mean().reset_index()
    fig6 = px.bar(cost_sig, x='SIGNIFICAN', y='TOTAL_COST', title='Average Cost: Significant vs Non-Significant', color='SIGNIFICAN', color_discrete_map={'YES': 'red', 'NO': 'green'})
    st.plotly_chart(fig6, use_container_width=True)

# Top 10
st.subheader("Top 10 Most Expensive Incidents")
top10 = filtered_df.nlargest(10, 'TOTAL_COST')[['ONSHORE_ST', 'CAUSE', 'TOTAL_COST', 'SIGNIFICAN', 'eq_count', 'eq_max_mag', 'HubDist', 'pipe_type']].reset_index(drop=True)
top10.index += 1
st.dataframe(top10, use_container_width=True)

# Year trend
st.subheader("Year-wise Trend by State")
top5_states = filtered_df['ONSHORE_ST'].value_counts().head(5).index.tolist()
year_state = filtered_df[filtered_df['ONSHORE_ST'].isin(top5_states)]
year_state = year_state.groupby(['IYEAR', 'ONSHORE_ST']).size().reset_index(name='count')
fig10 = px.line(year_state, x='IYEAR', y='count', color='ONSHORE_ST', title='Year-wise Trend for Top 5 States', markers=True)
st.plotly_chart(fig10, use_container_width=True)