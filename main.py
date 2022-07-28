import streamlit as st
import pandas as pd
import plotly.express as px

# Dataset load
df = pd.read_pickle("data/moto_df.pkl")

# Page configuration and title
st.set_page_config(page_title='MotoCompare', layout='wide', page_icon="🏍️")
st.markdown("<h1 style='text-align: center; color: #666666;'>Motorcycle comparison.</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([2,10])

# Type of graph
plot = col1.radio(
     "Graph type:",
     ("Scatter Plot", "Bar Plot"))

# Color group for the graphs
group = col1.radio(
     "Group By:",
     ("Brand", "Country"))

# Color sequence for better readability
sequence = ['#8C564B', '#B82E2E', '#66AA00',
 '#DD4477', '#0099C6', '#990099', '#109618',
  '#FF9900', '#DC3912', '#3366CC'] if group == "Brand" else ['#990099',
  '#109618',
  '#3366CC',
  '#B82E2E',
  '#FF9900',
  '#0099C6']

# Y axis
y_sel = col1.selectbox(
     'Choose the y axis:',
     ('Fuel consumption (l/100km)', 'Power (CV)','Displacement (cc)', 'Top speed (km/h)',"Dry weight (kg)"))

if plot == "Scatter Plot":
     # X axis 
     x_sel = col1.selectbox(
          'Choose the x axis:',
          ('Power (CV)','Fuel consumption (l/100km)', 'Displacement (cc)', 'Top speed (km/h)',"Dry weight (kg)", 'Year'))

     # Scatter plot with the params selected above.
     fig = px.scatter(
     df, x=x_sel, y=y_sel, color=group,
     width=1200, height=700,
     trendline= "lowess",
     trendline_scope="overall", trendline_color_override="black",
     color_discrete_sequence= sequence,
     hover_name="Model")
     
     # Checkbox that toggles the legend of the graph, has to go after the graph for the update to work
     check = col1.checkbox("Show Legend",value=True)
     fig.update(layout_showlegend=check)

else:
     fig = px.box(
     df, x=group, y=y_sel, color=group,
     width=1200, height=700, points="all",
     hover_data=['Power (CV)','Fuel consumption (l/100km)', 'Displacement (cc)', 'Top speed (km/h)', 'Year'],
     color_discrete_sequence=sequence, hover_name="Model")
     fig.update(layout_showlegend=False)


col2.plotly_chart(fig, use_container_width=True)

# Part 2, a table search functionality
st.markdown("<h2 style=color: #666666;'>Search Database</h2>", unsafe_allow_html=True)

col1_down, col2_down = st.columns((2,10), gap="large")

brand_sel = col1_down.multiselect(
     'Brand',
     df.Brand.unique().tolist(),
     help="All by default. You can select multiple options for this field.")

# in case the list is empty, return all
brand_sel = brand_sel if len(brand_sel) > 0 else df.Brand.unique().tolist()


country_sel = col1_down.multiselect(
     'Country',
     df.Country.unique().tolist(),
     help="All by default. You can select multiple options for this field.")

# in case the list is empty, return all
country_sel = country_sel if len(country_sel) > 0 else df.Country.unique().tolist()


year_start, year_end = col1_down.select_slider(
     'Year Range',
     options = sorted(df.Year.unique().tolist()),
     value = (sorted(df.Year.unique().tolist())[0], sorted(df.Year.unique().tolist())[-1]))

power_start, power_end = col1_down.select_slider(
     'Power Range (CV)',
     options = sorted(df['Power (CV)'].unique().tolist()),
     value = (sorted(df['Power (CV)'].unique().tolist())[0], sorted(df['Power (CV)'].unique().tolist())[-1]))

fuel_start, fuel_end = col1_down.select_slider(
     'Fuel Consumption Range (l/100km)',
     options = sorted(df['Fuel consumption (l/100km)'].unique().tolist()),
     value = (sorted(df['Fuel consumption (l/100km)'].unique().tolist())[0], sorted(df['Fuel consumption (l/100km)'].unique().tolist())[-1]))

disp_start, disp_end = col1_down.select_slider(
     'Displacement Range (cc)',
     options = sorted(df['Displacement (cc)'].unique().tolist()),
     value = (sorted(df['Displacement (cc)'].unique().tolist())[0], sorted(df['Displacement (cc)'].unique().tolist())[-1]))


speed_start, speed_end = col1_down.select_slider(
     'Top Speed Range(km/h)',
     options = sorted(df['Top speed (km/h)'].dropna().unique().tolist()),
     value = (sorted(df['Top speed (km/h)'].dropna().unique().tolist())[0], sorted(df['Top speed (km/h)'].dropna().unique().tolist())[-1]))


col2_down.dataframe(df.loc[
     (df['Brand'].isin(brand_sel)) &
     (df['Country'].isin(country_sel)) &
     (df['Year'].between(year_start, year_end)) &
     (df['Power (CV)'].between(power_start, power_end)) &
     (df['Fuel consumption (l/100km)'].between(fuel_start, fuel_end)) &
     (df['Displacement (cc)'].between(disp_start, disp_end)) &
     (df['Top speed (km/h)'].between(speed_start, speed_end))
     ],height=700)