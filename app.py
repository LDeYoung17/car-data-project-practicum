import pandas as pd
import streamlit as st
import plotly.express as px

st.title('Fuel Analysis')

st.markdown("""
This application contains a brief analysis of fuel and how it intersects with vehicle and transmission types. The source of this information is car advertisement dataset provided for this project.
""")

#reading in the data
car_data = car_data = pd.read_csv('/Users/leahdeyoung/Desktop/GitHub/car-data-project-practicum/vehicles_us.csv', encoding = "utf-8")

#data grouping for all three histograms
car_type_frequency = car_data.groupby('type')['type'].count()
car_fuel = car_data.groupby('fuel')['fuel'].count()
car_transmission = car_data.groupby('transmission')['transmission'].count()

#types of vehicle - histogram
car_type_hist = px.histogram(car_type_frequency, 
                             y='type', 
                             nbins=8, 
                             title='Car Type Frequency')

#different fuels vehicles use - histogram
car_fuel_hist = px.histogram(car_fuel, 
                             x='fuel', 
                             nbins=5, 
                             title='Fuel and Transmission Type Frequency')
#different transmissions vehicles use - histogram
car_trans_hist = px.histogram(car_transmission, 
                             x='transmission', 
                             nbins=10,
                             title='Transmission Type Frequency' 
                             )

#data grouping for first scatter plot
grp = car_data.groupby(['fuel', 'transmission'])
car_fuel_transmission = grp['price'].mean()
car_fuel_transmission = car_fuel_transmission.reset_index().rename(columns={0: 'price'})

#average price for vehicle based on their fuel and transmission type -  scatter plot
car_fuel_scatter = px.scatter(car_fuel_transmission,
                              x='fuel',
                              y='price',
                              color='transmission',
                              labels={
                                'value': 'Average Price',
                                'index': 'Transmission Type'},                              
                              title='Average Price per Type of Transmission and Fuel')

#data grouping for second scatter plot
grp2 = car_data.groupby(['fuel', 'type'])
car_type = grp2['price'].mean()
car_type = car_type.reset_index().rename(columns={0: 'price'})

#Vehicle and fuel type and average price - scatter plot
car_type_scatter = px.scatter(car_type,
                              x='type',
                              y='price',
                              color='fuel',
                              labels={
                                  'price': 'Average Price',
                                  'type': 'Vehicle Type',
                                  'fuel': 'Fuel Type'},
                              title='Average Price for Vehicle and Fuel Type')

#this function will display graphs and dataframes for various data breakdowns when the appropriate button is clicked
def show_info (carlist, cargraph, button_1, button_2):
    if st.button(button_1):
        st.dataframe(carlist)
    if st.button(button_2):
        st.plotly_chart(cargraph, theme=None, use_container_width=True) 

#first data breakdown
st.header('Vehicle Type Frequency')
st.markdown("""
This lists the various types of vehicles and how often they occur in the data.
""")
            
show_info(car_type_frequency, car_type_hist, 'Vehicle Type List', 'Vehicle Type Graph')

#second data breakdown
st.header('Fuel or Transmission Type')
st.markdown("""
This lists the various types of fuels and transmissions and how often they occur in the data.
""")
#this does not use the show_info() function because it has multiple charts included. It uses checkboxes instead of buttons as well.        
if st.checkbox('Fuel List'):
    st.dataframe(car_fuel)
if st.checkbox('Transmission List'):
    st.dataframe(car_transmission)

if st.checkbox('Fuel Type'):
    st.plotly_chart(car_fuel_hist, theme=None, use_container_width=True)
if st.checkbox('Transmission Type'):
    st.plotly_chart(car_trans_hist, theme=None, use_container_width=True)

#third data breakdown
st.header('Vehicle Fuel and Transmission Types and Prices')
st.markdown("""
This lists the  combinations of fuels and transmissions and average prices, and a scatter plot to visualize how they occur in the data.
""")

show_info(car_fuel_transmission, car_fuel_scatter, 'Vehicle Fuel/Transmission List', 'Vehicle Fuel/Transmission Graph')

#fourth data breakdown
st.header('Vehicle Types and the Fuels They Use')
st.markdown("""
This lists the various types of vehicles, the fuels they use, and the average price per vehicle/fuel type and displays a scatter plot demonstrating the data visually.
""")
            
show_info(car_type, car_type_scatter, 'Vehicle Type/Fuel List', 'Vehicle Type/Fuel Graph')
