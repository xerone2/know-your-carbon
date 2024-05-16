import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Know Your Carbon", page_icon=":four_leaf_clover:", layout="centered")
carbon_emissions = {
    'Train': {'Diesel': 0.75},
    'Airplane': {'Jet Fuel': 0.15},
    '2-Wheeler': {'Petrol': 0.10},
    'Car': {'Diesel': 2.68,
            'CNG': 0.15,
            'Petrol': 0.25},
    'Bus': {'Diesel': 0.56,
            'CNG': 0.114}
    ,
    'cooking': {
        'LPG': 0.365,
        'Natural Gas': 2.00,
        'Electricity': 0.50
    },
    'food': {
        'Beef': 0.027,
        'Lamb': 0.022,
        'Pork': 0.012,
        'Poultry': 0.006,
        'Cheese': 0.013,
        'Milk': 0.0015
    }
}


def form():

    global meat_count, travel_emission, dairy_count
    try:
        with st.form(key='travel-form'):

            st.subheader("Travelling   :small_airplane:")
            col1, col2 = st.columns(2)

            with col1:
                vehicle_type = st.selectbox('Mode of Travel', ('Car', '2-Wheeler', 'Bus', 'Train', 'Airplane'),
                                            label_visibility='visible')
                distance = st.number_input(label='Distance travelled', min_value=0, step=10, label_visibility='visible')

            with col2:
                fuel_type = st.selectbox('Fuel Type', ('Petrol', 'Diesel', 'CNG', 'Jet Fuel'),
                                         label_visibility='visible')
                distance_unit = st.radio('', ['Kms', 'Miles'], horizontal=True, label_visibility='visible')

            st.subheader("Cooking  :cooking:")
            col3, col4 = st.columns(2)

            with col3:
                cooking_mode = st.selectbox('Mode of cooking', ('LPG', 'Electricity', 'Natural Gas'),
                                            label_visibility='visible')
            with col4:
                cooking_time = st.number_input(label='Cooking Time(hrs)', min_value=0, label_visibility='visible')

            st.subheader("Food   :pancakes:")
            col5, col6 = st.columns(2)

            with col5:
                meat_type = st.multiselect("Meat Consumption", ['Beef', 'Lamb', 'Pork', 'Poultry'], default=None,
                                           label_visibility='visible')
                meat_qty = st.number_input(label="Total Weight", min_value=0, step=1, placeholder='Type',
                                           label_visibility='visible')

            with col6:
                dairy_type = st.multiselect("Dairy Consumption", ['Cheese', 'Milk'], default=None,
                                            label_visibility='visible')
                dairy_qty = st.number_input(label="Total Weight ", min_value=0, step=1,
                                            label_visibility='visible')
                weight_unit = st.radio('Weighing unit', ['grams', 'lbs'], horizontal=True, label_visibility='visible')

            submit_button = st.form_submit_button(label='Show results', help='Submit form')

        if submit_button:

            if distance_unit == 'Kms':
                travel_emission = distance * carbon_emissions[vehicle_type][fuel_type]
            if distance_unit == 'Miles':
                travel_emission = distance * carbon_emissions[vehicle_type][fuel_type] * 1.62137119

            cooking_emission = cooking_time * carbon_emissions['cooking'][cooking_mode]

            if meat_type:
                for meat in meat_type:
                    meat_count = carbon_emissions['food'][meat] * (meat_qty/len(meat_type))
                if weight_unit == 'lbs':
                    meat_count = meat_count * 453.592
            else:
                meat_count = 0.0

            if dairy_type:
                for dairy in dairy_type:
                    dairy_count = carbon_emissions['food'][dairy] * (dairy_qty/len(dairy_type))
                if weight_unit == 'lbs':
                    dairy_count = dairy_count * 453.592
            else:
                dairy_count = 0.0

            total_kg = round(travel_emission + cooking_emission + meat_count + dairy_count, 2)
            total_lbs = round(total_kg * 2.20462, 2)

            st.success(f'Total emission: {total_kg} Kilograms or {total_lbs} lbs of CO₂')

            data = {'category': [f'Travelled by {vehicle_type}', f'Cooking by {cooking_mode}', 'Food'],
                    'value': [travel_emission, cooking_emission, meat_count+dairy_count]}
            df = pd.DataFrame(data)

            fig = px.pie(df, values='value', names='category', title='Overall distribution',
                         width=400, height=400)
            st.plotly_chart(fig)
    except KeyError:
        st.warning("Invalid Configuration -- Try again")


def main():
    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<h1 style='font-size: 70px' class='centered-title'>Know Your Carbon</h1>", unsafe_allow_html=True)
    st.write('')
    st.markdown("<h5 class= 'centered-title'>Find your greenhouse gas emissions based on lifestyle factors</h5>",
                unsafe_allow_html=True)
    st.write('')
    st.write('')
    form()
    st.warning(" Please note that results are approximate and may not reflect precise emissions levels due to "
               "standard estimation methods.")


if __name__ == '__main__':
    main()
