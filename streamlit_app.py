import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 kale, Spinach & Rocket Smoothie')
streamlit.text('🥚 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🍓 Build your Own Fruit Smoothie 🥝🍇')
my_fruit_list=pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
# display the table on page
streamlit.dataframe(fruits_to_show)
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
   #streamlit.text(fruityvice_response.json())
   fruityvice_normalized=pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
#New section to display fruityvice api response   
streamlit.header('Fruityvice Fruit Advice!')
try:
   fruit_choice=streamlit.text_input('what fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("please select a fruit to get information")
   else:
      back_from_function=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)     
      
except URLError as e:
   streamlit.error()
streamlit.write('The user entered',fruit_choice)
streamlit.header("The fruit load list contains:")
#Snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
      return my_cur.fetchall()
 # Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows=get_fruit_load_list()
   streamlit.dataframe(my_data_rows)
# don't run anything past here while we trouble shoot
#streamlit.stop()  
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+new_fruit+"')")
      return "Thanks for adding "+new_fruit
add_fruit=streamlit.text_input('what fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=insert_row_snowflake(add_fruit)
   streamlit.text(back_from_function)

