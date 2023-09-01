from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import string


df = pd.read_csv('/Users/camillemolen/code/mfaruki/replenish_frontend/raw_data/bbc_final_df.csv')


def model_specific_preprocessing(tokenized_sentence):
    stop_words = set(stopwords.words('english'))
    no_stopwords = [w for w in tokenized_sentence if not w in stop_words]
    verb_lemmatized = [WordNetLemmatizer().lemmatize(tok, pos = "v") for tok in no_stopwords]
    noun_lemmatized = [WordNetLemmatizer().lemmatize(tok, pos = "n")for tok in verb_lemmatized]
    ingredient_string = ' '.join(noun_lemmatized)
    return ingredient_string

def ingredients_list(sample_txt):
    elements = []
    for punc in string.punctuation:
        sample_txt = sample_txt.replace(punc,'')
    for word in sample_txt.split():
        elements.append(str(word))
    return elements


def k_means(bbc_final_df, clusters=10, min_df=0.005, max_df=0.99):
    """Returns the df inputted with an additional column with their respective cluster.
    Ensure that the ingredients columns is a string of a list called 'final_ingredients'.
    I.E row 1, col ingredient is '[bread,cheese,pasta,onions]'"""

    # Step 1: Filter out recipes with no names & remove duplicates, keeping dietary info
    filtered_df = bbc_final_df[bbc_final_df['recipe_title'] != 'n']

    # print(filtered_df)

    grouped_df = filtered_df.groupby('recipe_title')['dietary'].apply(lambda x: ', '.join(x)).reset_index().rename(columns = {'dietary':'combined'})
    # grouped_df = filtered_df.groupby('recipe_title').sum()[['dietary']].reset_index()
    # grouped_df.rename(columns = {'dietary':'combined'}, inplace=True)
    merged_df = grouped_df.merge(filtered_df, how='left',on='recipe_title')
    #dropped_df = merged_df.drop(columns = 'dietary')
    df = merged_df.drop_duplicates('recipe_title')


    # Step 2: Convert the final ingredients into a "sentence" for vectorising
    df['ingredients_list'] = df['final_ingredients'].apply(ingredients_list)
    df['clean_text']=df['ingredients_list'].map(lambda x: model_specific_preprocessing(x))

    # Step 3: Convert ingredients sentence into a bag-of-words representation
    vectorizer = CountVectorizer(min_df=min_df, max_df = max_df)
    counted_words = pd.DataFrame(vectorizer.fit_transform(df['clean_text']).toarray(), columns = vectorizer.get_feature_names_out())

    # Step 4: Apply KMeans clustering
    kmeans = KMeans(n_clusters=clusters, random_state=0)
    df['cluster'] = kmeans.fit_predict(counted_words)

    return df


# almost_df = pd.read_csv('/Users/camillemolen/code/mfaruki/replenish_frontend/raw_data/bbc_final_df.csv')

# filtered_df = almost_df[almost_df['recipe_title'] != 'n']
# # print(filtered_df.columns)
# grouped_df = filtered_df.groupby('recipe_title')['dietary'].apply(lambda x: ', '.join(x)).reset_index().rename(columns = {'dietary':'combined'})
# # print(grouped_df)
# dd = k_means()
# print(type(dd))
