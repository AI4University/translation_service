import json
import requests
from collections import Counter
from tqdm import tqdm
import time
import pandas as pd

port = 10000

url = "http://kumo01:{}/translate".format(port) 
headers = {'content-type': 'application/json'}

df = pd.read_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet')
df['nmt_en'] = None
# Let us see what are the availables languages and how many documents of each language we have
languages = df['lang']
all_lang = Counter(languages)
for el, value in all_lang.items():
    print(f"Language: {el}, Documents: {value}")

# Let us check how many docuemnts are already translated
translated = df.dropna(subset=['nmt_en'])
print(f"Number of transalted documents: {translated.shape[0]}")

### PHASE 1 - We translate all Spanish documents to English

# Locate elements that need to be translated
en_df = df[df['lang'].isin(['es', 'fr', 'de', 'sv'])]

for iter, (idx, row) in enumerate(tqdm(en_df.iterrows(), desc="Progreso", unit="iter")):
    
    #Carry out translation, only if it is not already available
    if pd.isnull(row["nmt_en"]):
        text_to_translate = {"text": row['title'], "to_lang": "en"}


        #Carry out translation
        try:
            sttime = time.time()
            r = requests.post(url, data=json.dumps(text_to_translate), headers=headers)
            translation = json.loads(r.text)["translated_text"]
            nmt_en = {
                "status_code": r.status_code,
                "text": translation,
                "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nmt_time": time.time() - sttime
            }

        except:
            nmt_en = {
                "status_code" : r.status_code,
                "text" : ''
            }

        # df['nmt_en'][idx] = nmt_en
        df.at[idx, 'nmt_en'] = nmt_en

    if (iter+1) % 100 == 0:
        #Save after 1000 translations
        df.to_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet', index=False)


df.to_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet', index=False)
