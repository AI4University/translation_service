import pandas as pd
import ast
from langdetect import detect
from collections import Counter


def detect_language(text):
    '''
    text -> Text to detect language
    Function for detecting the language of a text
    '''
    try:
        return detect(text)
    except:
        return 'unknown'

df = pd.read_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet')
df = df.dropna(subset=['title'])
# Lets explore the number of documents of different languages before the preprocessing
languages = df['lang']
all_lang = Counter(languages)
for el, value in all_lang.items():
    print(f"Language: {el}, Documents: {value}")

# substitute abstracts by translated ones
for i in range(df.shape[0]):
    # Detect if the text has been transalted and in case yes, translate
    if df['nmt_en'][i] is not None:
        df.loc[i, 'title'] = df['nmt_en'][i]['text']

# Lets explore the number of documents of different languages after the preprocessing
print()
df['lang_after_translation'] = df['title'].apply(detect_language)
languages = df['lang_after_translation']
all_lang = Counter(languages)
for el, value in all_lang.items():
    print(f"Language: {el}, Documents: {value}")


df = df[['id', 'id_RP_paper', 'id_SS_paper', 'title', 'abstract', 'year', 'lang', 'lang_after_translation']]
#df = df[df['lang_after_translation']=='en']

df.to_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet', index=False)

a = 0






