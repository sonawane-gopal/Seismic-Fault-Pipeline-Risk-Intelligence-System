import streamlit as st
import pandas as pd
import plotly.express as px
import json
import joblib
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="SFPRIS", page_icon="pipeline", layout="wide")
st.title("Seismic-Fault Pipeline Risk Intelligence System")
st.markdown("SFPRIS - Predicting pipeline incident risk across the US using ML and geospatial data.")

@st.cache_data
def load_data():
    return pd.read_csv(r'D:\sfpris\data\processed\final_dataset_map.csv')

@st.cache_data
def load_networks():
    with open(r'D:\sfpris\data\processed\hl_network.geojson') as f:
        hl = json.load(f)
    with open(r'D:\sfpris\data\processed\gas_network.geojson') as f:
        gas = json.load(f)
    return hl, gas

@st.cache_resource
def load_model():
    return joblib.load(r'D:\sfpris\models\xgboost_pipeline_risk.pkl')

df = load_data()
hl_geojson, gas_geojson = load_networks()
model = load_model()

st.success("Data loaded: " + str(df.shape[0]) + " incidents across 49 states")

st.info("What is a Significant Incident? A pipeline incident is classified as SIGNIFICANT if it results in a fatality or injury requiring hospitalization, fire or explosion, property damage exceeding $50,000, or a liquid spill of 50 or more barrels.")

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
show_hl = st.checkbox("Show Hazardous Liquid Pipelines (Orange)", value=True)
show_gas = st.checkbox("Show Gas Pipelines (Blue)", value=True)

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

layers = []
if show_hl:
    layers.append({'source': hl_geojson, 'type': 'line', 'color': 'orange', 'opacity': 0.6, 'line': {'width': 1.5}})
if show_gas:
    layers.append({'source': gas_geojson, 'type': 'line', 'color': 'dodgerblue', 'opacity': 0.6, 'line': {'width': 1.5}})

fig.update_layout(
    mapbox_style=basemap,
    mapbox={'layers': layers},
    margin=dict(l=0, r=0, t=30, b=0),
    legend_title_text='Significant?'
)
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

# Fault Distance vs Cost
st.subheader("Fault Distance vs Incident Cost")
fig7 = px.scatter(filtered_df, x='HubDist', y='TOTAL_COST', color='SIGNIFICAN', color_discrete_map={'YES': 'red', 'NO': 'green'}, title='Fault Distance vs Total Cost', labels={'HubDist': 'Distance to Fault (m)', 'TOTAL_COST': 'Total Cost ($)'}, hover_data=['ONSHORE_ST', 'CAUSE'])
st.plotly_chart(fig7, use_container_width=True)

# Earthquake Impact
st.subheader("Earthquake Impact Analysis")
col7, col8 = st.columns(2)

with col7:
    eq_sig = filtered_df.groupby('eq_count')['SIGNIFICAN'].apply(lambda x: (x == 'YES').sum()).reset_index()
    eq_sig.columns = ['eq_count', 'significant_count']
    fig8 = px.bar(eq_sig.head(20), x='eq_count', y='significant_count', title='Earthquake Count vs Significant Incidents', color='significant_count', color_continuous_scale='reds')
    st.plotly_chart(fig8, use_container_width=True)

with col8:
    fig9 = px.scatter(filtered_df, x='eq_max_mag', y='TOTAL_COST', color='SIGNIFICAN', color_discrete_map={'YES': 'red', 'NO': 'green'}, title='Max Earthquake Magnitude vs Cost', labels={'eq_max_mag': 'Max Magnitude', 'TOTAL_COST': 'Total Cost ($)'})
    st.plotly_chart(fig9, use_container_width=True)

# Top 10 Most Expensive
st.subheader("Top 10 Most Expensive Incidents")
top10 = filtered_df.nlargest(10, 'TOTAL_COST')[['ONSHORE_ST', 'CAUSE', 'TOTAL_COST', 'SIGNIFICAN', 'eq_count', 'eq_max_mag', 'HubDist', 'pipe_type']].reset_index(drop=True)
top10.index += 1
st.dataframe(top10, use_container_width=True)

# Year-wise Trend by State
st.subheader("Year-wise Trend by State")
top5_states = filtered_df['ONSHORE_ST'].value_counts().head(5).index.tolist()
year_state = filtered_df[filtered_df['ONSHORE_ST'].isin(top5_states)]
year_state = year_state.groupby(['IYEAR', 'ONSHORE_ST']).size().reset_index(name='count')
fig10 = px.line(year_state, x='IYEAR', y='count', color='ONSHORE_ST', title='Year-wise Trend for Top 5 States', markers=True)
st.plotly_chart(fig10, use_container_width=True)

# Risk Predictor
st.subheader("Risk Score Predictor")
st.markdown("Enter pipeline details to predict if an incident will be significant:")

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    p_year = st.number_input("Incident Year", min_value=2010, max_value=2030, value=2020)
    p_cost = st.number_input("Total Cost ($)", min_value=0, value=50000)
    p_diameter = st.number_input("Pipe Diameter (inches)", min_value=0.0, value=12.0)
with col_p2:
    p_install = st.number_input("Installation Year", min_value=1900, max_value=2024, value=1980)
    p_hubdist = st.number_input("Distance to Fault (meters)", min_value=0.0, value=50000.0)
    p_eqcount = st.number_input("Earthquake Count Nearby", min_value=0, value=10)
with col_p3:
    p_eqmag = st.number_input("Max Earthquake Magnitude", min_value=0.0, value=3.5)
    p_eqdepth = st.number_input("Avg Earthquake Depth (km)", min_value=0.0, value=5.0)
    p_pipetype = st.selectbox("Pipeline Type ", ['hazardous_liquid', 'gas'])

p_cause = st.selectbox("Cause ", sorted(df['CAUSE'].dropna().unique().tolist()))
p_state = st.selectbox("State ", sorted(df['ONSHORE_ST'].dropna().unique().tolist()))
p_material = st.selectbox("Material", sorted(df['MATERIAL_I'].dropna().unique().tolist()))
p_system = st.selectbox("System Part", sorted(df['SYSTEM_PAR'].dropna().unique().tolist()))

if st.button("Predict Risk"):
    df_map_enc = pd.read_csv(r'D:\sfpris\data\processed\final_dataset_map.csv')
    input_data = pd.DataFrame([{
        'IYEAR': p_year, 'CAUSE': p_cause, 'ONSHORE_ST': p_state,
        'TOTAL_COST': p_cost, 'PIPE_DIAME': p_diameter, 'MATERIAL_I': p_material,
        'INSTALLATI': p_install, 'SYSTEM_PAR': p_system, 'HubDist': p_hubdist,
        'eq_count': p_eqcount, 'eq_max_mag': p_eqmag, 'eq_avg_depth': p_eqdepth,
        'pipe_type': p_pipetype
    }])
    cat_cols = ['CAUSE', 'ONSHORE_ST', 'MATERIAL_I', 'SYSTEM_PAR', 'pipe_type']
    le = LabelEncoder()
    for col in cat_cols:
        le.fit(df_map_enc[col].fillna('UNKNOWN'))
        input_data[col] = le.transform(input_data[col])
    prob = model.predict_proba(input_data)[0][1]
    pred = model.predict(input_data)[0]
    if pred == 1:
        st.error("HIGH RISK - Significant incident predicted! Probability: " + str(round(prob*100, 1)) + "%")
    else:
        st.success("LOW RISK - Non-significant incident predicted. Probability: " + str(round(prob*100, 1)) + "%")