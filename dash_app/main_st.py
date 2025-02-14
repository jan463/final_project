import streamlit as st
import pandas as pd
import ast
from st_aggrid import AgGrid, GridOptionsBuilder
from functions import seeker, to_minutes
from PIL import Image
from io import BytesIO
import requests
import re


# Page setup
st.set_page_config(
    page_title="Menunator",
    layout="wide", 
    page_icon="🍕",
)

# Title and Images
col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
with col2:
    st.header("Menu Browser")
with col3:
    st.image("Bowser.png", width=100)

# Tabs
#col1, col2, col3 = st.columns([10, 3, 10])
#with col2:
tab1, tab2 = st.tabs(["Finder", "About"])

with tab1:
    st.write("\n\n\n")

    # Load data
    df = pd.read_csv("../data/master.csv")
    def convert_list(x):
        return ast.literal_eval(x)
    df["nations"] = df["nations"].apply(convert_list)

    # Initialize session state variables
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = pd.DataFrame()

    if 'page_var' not in st.session_state:
        st.session_state.page_var = 0

    if 'button_pushed' not in st.session_state:
        st.session_state.button_pushed = 0

    # Declare search terms
    ingredients = "x"
    name = "x"
    cooktime = "x"
    preptime = "x"
    totaltime = "x"
    dish = "All"
    searchword = ""


    # Search filters
    col1, col2, col3, col4, col5, col6, col7 = st.columns([5, 3, 1, 3, 1, 3, 5])
    with col2:
        st.markdown("**Time**")
        preptime = st.slider("Preparation Time:", min_value=0, max_value=180)
        cooktime = st.slider("Cook Time:", min_value=0, max_value=180)
        totaltime = st.slider("Total Time:", min_value=0, max_value=240)

    with col4:
        st.markdown("**Dish**")
        dish = st.radio("", ["All", "Appetizer", "Salad", "Soup", "Main Dish", "Side", "Dessert"])
        #st.selectbox('Select', [1,2,3])
        #st.multiselect('Multiselect', [1,2,3])
        searchword = st.text_input("Enter a search word:")

    with col6:
        st.markdown("**Nutritional Values**")
        calories = st.slider("Calories per Serving:", min_value=0, max_value=1000)
        carbs = st.slider("Carbohydrates [g] per Serving:", min_value=0, max_value=1000)
        protein = st.slider("Protein [g] per Serving:", min_value=0, max_value=1000)

    col1, col2, col3 = st.columns([5, 1, 5])
    with col2:
        if st.button("Search Recipes"):
            # Filter the DataFrame based on user inputs
            st.session_state.filtered_df = seeker(df, ingredients, name, cooktime, preptime, totaltime, dish, searchword, calories, carbs, protein)
            st.session_state.page_var = 0  # Reset to first page
            st.session_state.button_pushed = 1

    st.divider()

    # Page navigation
    items_per_page = 10
    total_items = len(st.session_state.filtered_df)
    total_pages = (total_items - 1) // items_per_page + 1

    if st.session_state.button_pushed == 1:
        col1, col2, col3, col4, col5 = st.columns([5, 1, 2, 1, 5])
        with col2:
            if st.button("Previous") and st.session_state.page_var > 0:
                st.session_state.page_var -= 1

        with col4:
            if st.button("Next") and st.session_state.page_var < total_pages - 1:
                st.session_state.page_var += 1

        with col3:
            st.write(f"Page {st.session_state.page_var+1} from {total_pages}")

    # Slice DataFrame for the current page
    start_index = st.session_state.page_var * items_per_page
    end_index = start_index + items_per_page
    page_df = st.session_state.filtered_df.iloc[start_index:end_index]



    st.write("\n\n")

    # Custom CSS for Streamlit button styling
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            display: block;
            width: 100%;
            text-align: left;
            background-color: #f0f0f0;
            color: black;
            padding: 10px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: normal;
        }
        div.stButton > button:first-child:hover {
            background-color: #e0e0e0;
        }
        </style>
        """, unsafe_allow_html=True
    )


    # Display the current page of DataFrame with buttons
    col1, col2, col3, col4 = st.columns([3, 1, 2, 8])



    my_row = -1

    if not page_df.empty:
        

        with col1:
            st.subheader("Name")
        with col2:
            st.subheader("Rating")



        for index, row in page_df.iterrows():


            with col2:
                # fake button ;)
                st.button(f"{row['aggregatedrating']}", key=f'details_{row["aggregatedrating"]}_{index}', use_container_width=True)
            

            with col1:
                if st.button(f"{row['name']}", key=f"name_{index}"):
                    my_row = index


            with col3:
                if my_row == index:
                    st.subheader("Ingredients")
                    for i in (row["ingredients_raw_str"]).strip('"[]').split('","'):
                        st.write(i)
                    

            with col4:
                if my_row == index:
                    st.subheader("Recipe")

                    try:
                        url = re.findall(r'"([^"]*)"', row["images"])             
                        #url = row["images"].strip('"')
                        st.image(url, width=240)
                    except:
                        ""

                    st.write(f'{row["servings"]} Servings, Serving size: {row["serving_size"]}g')
                    st.markdown("**Nutritional values:**")
                    st.write(f'{row["calories"]} calories, '
                    f'{row["cholesterolcontent"]}mg cholesterol, {row["sodiumcontent"]}mg Sodium, '
                    f'{row["fibercontent"]}g Fibers')

                    st.write(f'{row["fatcontent"]}g fat, {row["saturatedfatcontent"]}g saturated fat, '
                    f'{row["carbohydratecontent"]}g Carbohydrates, '
                    f'{row["sugarcontent"]}g Sugar, {row["proteincontent"]}g Protein')

                    st.markdown("**Description:**")
                    st.write(row['description'])
                    st.subheader("Steps")
                    row_str =  (row["steps"]).strip("[]")
                    row_str = re.split(r";|', '", row_str)
                    for i in row_str:
                        st.write("- "+i)
