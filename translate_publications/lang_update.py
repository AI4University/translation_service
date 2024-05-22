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

INITIAL_RUN = True
df = pd.read_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet')

if INITIAL_RUN:
    df['lang'] = 'unknown'
    df['nmt_en'] = None
    df = df.dropna(subset=['abstract'])

df['lang'] = df.apply(lambda row: detect_language(row['abstract']) if row['lang'] == 'unknown' else row['lang'], axis=1)
df.to_parquet('data_ingest/match_semanticScholar_researchPortal/match_outputs/publications_translated.parquet')
