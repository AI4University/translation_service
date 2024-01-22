import pandas as pd
from langdetect import detect

def detect_language(text):
    '''
    text -> Text to detect language
    Function for detecting the language of a text
    '''
    try:
        return detect(text)
    except:
        return 'unknown'

df = pd.read_parquet('translation_service/translate_publications/publications.parquet')
df['lang'] = df.apply(lambda row: detect_language(row['Abstract']) if row['lang'] == 'unknown' else row['lang'], axis=1)
df.to_parquet('translation_service/translate_publications/publications.parquet', index=False)