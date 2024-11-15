# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

name_on_order = st.text_input("Name on the Smoothie")
st.write("The name on the Smoothie will be:", name_on_order)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose upto 5 ingredients:', my_dataframe, max_selections = 5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_respnse.json(), use_container_width = True)
        #st.write(ingredients_list)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button ('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!,'+ name_on_order)


