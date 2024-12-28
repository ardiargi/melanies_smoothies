# Import python packages
import streamlit as st
import datetime
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize your Smothie!")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))



order_name = st.text_input("Order name")
st.write("Order names", order_name)


ingredients_list = st.multiselect(
        'Choose up to 5 fruits:'
    , my_dataframe
    , max_selections =5
)




if ingredients_list:
    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit+' '

   
    time_to_insert = st.button('Submit Order')
   

   
    
    if time_to_insert:
        today = datetime.datetime.now()
        st.write(today)
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER, order_ts)
            values ('""" + ingredients_string+ """','"""+order_name+ """',current_timestamp)"""

        st.write(my_insert_stmt)
        
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
