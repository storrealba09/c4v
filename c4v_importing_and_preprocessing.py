# -*- coding: utf-8 -*-
"""C4V_Importing and Preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p5ad-0WityuCAvtDhJm8iEQl90xqeH_h
"""

# # Enable outputting results interactively. 
# # All the results from code in a given cell will be displayed instead of only the last one.

# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"

# install spaCy packages and dependencies


# ! pip install -U spacy
# ! python -m spacy validate

# ! pip install -U spacy[cuda92]

# import spacy

# spacy.prefer_gpu()

# ! python -m spacy download es_core_news_sm

import es_core_news_sm
nlp = es_core_news_sm.load()

# import packages for data processing

import pandas as pd
import numpy as np
import sqlite3
import scipy.stats as stats
from datetime import datetime
import re
import string


# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

# Code to read csv file into Colaboratory:
# !pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
# Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

link = "https://drive.google.com/open?id=1GMn-9mQbXWrzwNFP7WCkJEBJxIsiVNKM"

fluff, id = link.split('=')
print (id)

downloaded = drive.CreateFile({'id':id}) 
downloaded.GetContentFile('filtered_tweets.csv')

df = pd.read_csv('filtered_tweets.csv',error_bad_lines=False, sep = '|')

df.shape

df.head()

df = df.set_index(pd.DatetimeIndex(df['tweet_date']))
df['year'] =df.index.strftime('%Y')
df['month_yr'] =df.index.strftime('%Y-%m')
df.head()

cols = df.columns
cols

df['is_duplicated'] = df.duplicated(['username', 'hash_tags', 'tweet_text'])

# df['is_duplicated'] = df.duplicated(cols)

df['is_duplicated'].sum()

df['is_duplicated2'] = df.duplicated(['tweet_text','username'])

df['is_duplicated2'].sum()

df['is_duplicated3'] = df.duplicated(['tweet_text'])

df['is_duplicated3'].sum()

df2  = df[df.is_duplicated3 != True].drop(['is_duplicated','is_duplicated2', 'is_duplicated3'],axis=1)
df2.shape

df2['tweet_text2'] =  df2['tweet_text'].str.replace('#','')
df2['tweet_text2'] = df2['tweet_text2'].str.replace(' RT ','')

df2['RT_tag'] = df2['tweet_text2'].str.contains('RT')
df2['RT_tag'].sum()

df2[df2.RT_tag == 1]

df2.resample('Y').size()

m_tmp = df2.resample('M').size().reset_index(name='Counts') 
m_tmp

df2['tweet_text3'] = df2['tweet_text2'].astype(str).str.lower()
df2.head()

def extract_nouns(tweet_text3):
    """Extract NOUN and PROPN using spaCy's POS (part of speech) tagging. 
    
    Keyword arguments:
    text -- the actual text source from which to extract entities
    
    """
    keep_pos = ['NOUN']


    return [tok.text for tok in nlp(tweet_text3) if tok.pos_  in keep_pos]
  
#     df2['token'] = df2['tweet_text'].apply(lambda x: ";".join(tok.text for tok in nlp(tweet_text) if tok.pos_  in keep_pos))
  
  

def add_nouns(df2):
    """Create new column in data frame with nouns extracted.
    
  
    
    """
    df2['nouns'] = df2['tweet_text3'].apply(extract_nouns)

add_nouns(df2)

df2.head(30)

lst = df2.columns.tolist()
lst

cols = ['username', 'tweet_url','tweet_text', 'nouns']
df3 = df2[cols].reset_index()

df3.head(1)

with open('tweets_nouns.json', 'w') as f:
  f.write(df3.to_json())

# Download the file.
from google.colab import files
files.download('tweets_nouns.json')

import pickle

with open('tweets_nouns.pkl', 'wb') as f:
    pickle.dump(df3, f)

# Download the file.
from google.colab import files
files.download('tweets_nouns.pkl')

# import spacy
# # nlp = spacy.load('es_core_news_sm')
# doc = nlp(u"#ServicioPúblico | Se requiere con urgencia malaria paciente en terapia intensiva en #maracay Ciprofloxacina de 200 gm en ampolla, Levofloxacina de de 80g o 750mg y Ertapenem de 1 g en ampolla. Contacto: 0424-2594256")
# for token in doc:
#     print(token.text, token.pos_, token.dep_)

"""# New Section

# New Section
"""

