import streamlit as st
import datetime
import requests
import random
from PIL import Image
import pandas as pd
import numpy as np
import os
from PIL import Image

cuisines = ['afghan', 'african', 'american','australian', 'asian','austrian',
            'azerbaijan', 'balinese', 'belgian','brazilian','british','cajun-creole',
            'caribbean', 'chinese','cuba','danish', 'dinner', 'eastern-european', 'egyptian', 'english',
            'finland','french', 'german', 'greek', 'hungarian', 'indian', 'indonesian', 'irish', 'italian', 'jamaican',
            'japanese', 'jewish', 'korean', 'latin-american', 'lithuanian', 'mediterranean', 'mexican',
            'middle-eastern', 'moroccan', 'nepalese', 'nigerian', 'north-african', 'persian', 'peruvian', 'polish', 'portuguese',\
            'scandinavian', 'senegalese', 'scottish', 'southern-soul', 'spanish', 'swedish', 'swiss',
            'taiwanese', 'thai', 'tunisian', 'turkish', 'ukrainian', 'vietnamese', 'welsh', 'balkan', 'czech', 'czech-cuisine']

dietary= ['vegetarian','vegan', 'gluten-free','nut-free','healthy', 'dairy-free', 'egg-free', 'low-calorie', 'low-sugar',
           'high-protein', 'low-fat', 'high-fibre', 'keto', 'low-carb']


#Dummy Data
df= pd.DataFrame.from_dict({'title':['chili con carne', 'meatballs'],
                                 'ingredients':[['cool','stuff','wow','hungry'],['chili','meat','balls']],
                                 'cluster':[2,1],'pref':['italian', 'german']})

#Setting Website Configuration
st.set_page_config(
            page_title="Replenish", # => Quick reference - Streamlit
            page_icon="🐍",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed


####################
### FUNCTIONS AND ##
###      APIS    ###
####################

def initial_recipes():
    pass

def carbon_foodprint():
    pass


#######################################         PAGE 1           ##########################
def intro():
    """Website page 1: Replenish introduction page for multifaced website."""
    ####################
    #### INTRO PAGE ####
    ####################

    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.2, .05, 1.3, .1))
    with row0_1:
        st.title('Replenish - A Recipe Optimizer')
    with row0_2:
        st.text("")
        st.subheader('Streamlit App by [Maaviya Faruki, Camille Molen, Jayesh Mistry, Jonas Korganas](https://www.linkedin.com/in/camille-molen/)')

    st.text("")

    row2_spacer1, row2_1, row2_spacer2 = st.columns((.1, 3.2, .1))
    with row2_1:
        st.markdown("""*Have you ever struggled with groceries and found yourself wondering:
                    what do I need to buy, do I really need this much broccoli if it is only for one recipe?
                    Have you ever felt like you are repeatedly throwing away expired food that you only used
                    for one meal but never had the chance to incorporate into another?
                    Well Replenish is here to solve these problems and minimise both your shopping expenses,
                    food wastage, and contribution to Carbon Footprint!*""")


    ####################
    ### CHECKOUT DATA ##
    ####################

    row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
    with row3_1:
        st.subheader("Currently selected recipes:")

    row4_spacer1, row4_1, row4_spacer2, row4_2, row4_spacer3, row4_3, row4_spacer4   = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2))
    with row4_1:
        unique_recipes_in_df = len(df.title)
        str_games = str(unique_recipes_in_df) + " Recipes"
        st.markdown(str_games)
    with row4_2:
        num_clusters_in_df = max(np.unique(df.cluster))
        str_clusters = str(num_clusters_in_df) + " Ingredients-based Clusters"
        st.markdown(str_clusters)
    with row4_3:
        total_preferences_in_df = df.pref.nunique()
        str_preferences =str(total_preferences_in_df) + " Preferences"
        st.markdown(str_preferences)

    #Click to see data button

    st.markdown("")
    see_data = st.expander('Click here for an insight into the dataset 👉')
    with see_data:
        st.dataframe(data=df.set_index('title'))
    st.text("")

    ####################
    ####  FOUNDERS  ####
    ####################

    text = 'Meet The Founders'
    st.markdown(
            f"<h1 style='text-align: center;'>{text}</h1>",
            unsafe_allow_html=True)
    st.write("--------------")

    row5_spacer1,row5_1,row5_spacer2,row_5_2,row5_spacer3,row5_3,row5_spacer4,row5_4,row5_spacer5 = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))

    path = os.path.join(os.path.dirname(os.getcwd()),'raw_data')

    with row5_1:
        image = Image.open(os.path.join((path),'maaviya.jpg'))
        st.subheader("***Maaviya Faruk***")
        st.image(image, use_column_width=True)

    with row_5_2:
        image1 = Image.open(os.path.join((path),'jay.jpeg'))
        st.subheader("***Jayesh Mistry***")
        st.image(image1, use_column_width=True)

    with row5_3:
        image2 = Image.open(os.path.join((path),'jonas.jpeg'))
        st.subheader("***Jonas Korganas***")
        st.image(image2, use_column_width=True)

    with row5_4:
        image3 = Image.open(os.path.join((path),'camille.jpg'))
        st.subheader("***Camille Molen***")
        st.image(image3, use_column_width=True)

    st.write("--------------")

    st.markdown("""*You can find the source code in the
                [Replenish Repository](https://github.com/mfaruki/replenish)*""")
    st.markdown("""*If you are interested in investing in the Replenish
                goal feel free to contact the team!*""")


#######################################         PAGE 2           ##########################

def output():
    """Website page 2: Given the user's food-preferences the user is returned
    a vareity of recipes which hold to the most similar in ingredients. Minimal ingredients
    and variety of recipes """
    st.title('Find Waste-Minimizing Recipes with Replenish!')

    row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
    with row6_1:
        st.subheader('Recipe Finder')
        st.markdown('Find recipes with similar ingredients according to the preference(s)...')

    ####################
    ###  PREFERENCES ###
    ####################

    row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3 = st.columns((.2, 2.3, .2, 2.3, .2))
    with row7_1:
        cuisine_pref = st.selectbox ("Cuisines", cuisines,key = 'hi_lo')
    with row7_2:
        diet_pref = st.selectbox ("Dietary", dietary,key = 'pref')

    st.write("--------------")

    ####################
    ###  1ST RECIPES ###
    ####################
    carb=1000  ######------------------DELETE LATER!!!!

    row8_spacer1,row8_1,row8_spacer2,row8_2,row8_spacer3,row8_3,row8_spacer4 = st.columns((.05, 1, .05, 1, .05, 1, .05))
    #title, plot, list carbon
    with row8_1:
        recipe_1 = str(df.title[0])
        st.subheader(recipe_1)
        st.text(f"Carbon Footprint:{carb}")
        for item in df.ingredients[0]:
            st.write(f"- {item}")

    with row8_2:
        recipe_2 = str(df.title[1])
        st.subheader(recipe_2)
        st.text(f"Carbon Footprint:{carb}")
        for item in df.ingredients[0]:
            st.write(f"- {item}")

    with row8_3:
        recipe_2 = str(df.title[0])
        st.subheader(recipe_2)
        st.text(f"Carbon Footprint:{carb}")
        for item in df.ingredients[0]:
            st.write(f"- {item}")

    st.write("--------------")

    ####################
    ###    SIMILAR   ###
    ###    RECIPES & ###
    ###  INGREDIENTS ###
    ####################

    st.text("Press below for more recipes of the same category")
    if st.button("Similar"):
        row10_spacer1,row10_1,row10_spacer2,row10_2,row10_spacer3,row10_3,row10_spacer4 = st.columns((.05, 1, .05, 1, .05, 1, .05))
        #title, plot, list carbon
        with row10_1:
            new_recipe1 = str(df.title[0])
            st.subheader(new_recipe1)
            st.text(f"Carbon Footprint:{carb}")
            for item in df.ingredients[0]:
                st.write(f"- {item}")

        with row10_2:
            new_recipe2 = str(df.title[1])
            st.subheader(new_recipe2)
            st.text(f"Carbon Footprint:{carb}")
            for item in df.ingredients[0]:
                st.write(f"- {item}")

        with row10_3:
            new_recipe3 = str(df.title[0])
            st.subheader(new_recipe3)
            st.text(f"Carbon Footprint:{carb}")
            for item in df.ingredients[0]:
                st.write(f"- {item}")

    ####################
    # DIVERSE RECIPES ##
    ###    SIMILAR   ###
    ###  INGREDIENTS ###
    ####################

    if st.button("Different"):
        row10_spacer1,row10_1,row10_spacer2,row10_2,row10_spacer3,row10_3,row10_spacer4 = st.columns((.05, 1, .05, 1, .05, 1, .05))
        #title, plot, list carbon
        with row10_1:
            new_recipe1 = str(df.title[0])
            st.subheader(new_recipe1)
            st.text(f"Carbon Footprint:{carb}")
            for item in df.ingredients[0]:
                st.write(f"- {item}")

        with row10_2:
            new_recipe2 = str(df.title[1])
            st.subheader(new_recipe2)
            st.text(f"Carbon Footprint:{carb}")
            for item in df.ingredients[0]:
                st.write(f"- {item}")

        with row10_3:
            new_recipe3 = str(df.title[0])
            st.subheader(new_recipe3)
            st.text(f"Carbon Footprint:{carb}")
            for item in df.ingredients[0]:
                st.write(f"- {item}")

    st.write("------")

    ####################
    ## SHOPPING LIST ###
    ####################

    row11_spacer1,row11_1,row11_spacer2,row11_2, row11_spacer3 = st.columns((.2, 1.6, .2, 1.6, .2))

    with row11_1:
        st.subheader("Your Shopping List:")
        for item in df.ingredients[0]:
            st.write(f"- {item}")

    with row11_2:
        st.subheader(f"Your Shopping List's Carbon Foodprint is: {carb}")

    st.write("------")

#######################################         PAGE 3           ##########################

def graphing():
    """Third website page will show the distribution of preferences across the clusters
    determined by Replenish's model, where the cluster to be seen is inputted/chosen by
    the viewer."""

    st.title("Graphing Replenish's Cluster Distributions!")
    select = st.selectbox("Select a cluster group you would like to observe", range(1, max(df.cluster)+1))

    if st.button("Submit"):
        st.text("Below is the distribution of preference categories")
        st.text(f"within the ingredient-based cluster {select}")



page_names_to_funcs = {
    "About Us": intro,
    "Recipe Generator": output,
    "Data Graphing": graphing,
}

demo_name = st.sidebar.selectbox("Click to find out more 👉", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
