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

INITIAL_RUN = False
#df = pd.read_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet')
df = pd.read_parquet('/Volumes/usuarios_ml4ds/mbalairon/github/data_ingest/match_semanticScholar_researchPortal/match_outputs/publications_translated.parquet')
if INITIAL_RUN:
    df['lang'] = 'unknown'
    df['nmt_en'] = None
    df = df.dropna(subset=['title'])

df['lang'] = df.apply(lambda row: detect_language(row['title']), axis=1)
df.to_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet')
