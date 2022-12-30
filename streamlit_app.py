import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("My parents had Healthy dinner")
streamlit.header('🍳Breakfast Menu')
streamlit.text('🥑Omega 3 & Blueberry Oatmeal')
streamlit.text('☘️Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)



# Display the table on the page.
#streamlit.dataframe(my_fruit_list)

streamlit.header("Fruityvice Fruit Advice!")
try :
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select which fruit to select')
  else:
    streamlit.write('The user entered ', fruit_choice)

    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

    # normalise response
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # write your own comment - what does this do?
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("use warehouse compute_wh") 
my_cur.execute("use database pc_rivery_db") 
my_cur.execute("use schema public") 
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)


add_my_fruit = streamlit.text_input('What fruit would you like to add?','Peach') 
streamlit.write('Thanks for adding ', add_my_fruit)
