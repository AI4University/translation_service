import pandas as pd
from traductor import detect_language
import re
import requests
import json
from tqdm import tqdm

def limpiar_resumenes(texto):
    try:
        # Convertir a minúsculas
        texto = texto.lower()
        # Eliminar números
        texto = re.sub(r'\d+', '', texto)
        # Eliminar caracteres especiales, excepto letras, espacios, y puntos
        texto = re.sub(r'[^\w\s.]', '', texto)
        # Eliminar caracteres de nueva línea y retornos de carro
        texto = texto.replace('\r', '').replace('\n', '')
        return texto
    except:
        return None

def clean_equals(text):
    sentences = text.split('= ')
    languages = {}
    for i, sentence in enumerate(sentences):
        lang = detect_language(sentence)
        languages[lang] = i

    if 'en' in languages.keys():
        idx = languages['en']
        return sentences[idx]
    elif 'es' in languages.keys():
        idx = languages['es']
        return sentences[idx]
    else:
        return ''
    
path = '/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/parquet/'
port = 10000

url = "http://kumo01:{}/translate".format(port) 
headers = {'content-type': 'application/json'}

projects = pd.read_parquet(path + 'projects.parquet')
projects_translated = pd.DataFrame(columns=['actID', 'text'])
#projects_translated = pd.read_parquet('translated_projects.parquet')
projects_translated_keywords = pd.read_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/projects_translated_keywords.parquet')

projects = projects[projects['Keywords'].notna() | projects['resumen'].notna()]


ids_to_translated = list(set(projects['actID']) - set(projects_translated['actID']))
indexes = list(projects[projects['actID'].isin(ids_to_translated)].index)

count = 0
for i in tqdm(indexes, desc="Procesando publicaciones"):
    count +=1
    id_project = projects['actID'][i]
    title = projects['Title'][i]
    resumen = projects['resumen'][i]

    if resumen is None:
        resumen = ''

    if '='  in title:
        title = clean_equals(title)
    
    if '='  in resumen:
        resumen = clean_equals(resumen)

    text_to_translate = limpiar_resumenes(title + '. ' + resumen)
    sentences = [sentence.strip() for sentence in text_to_translate.split('.') if sentence.strip()]

    translated_text = []
    for sentence in sentences:
        if detect_language(sentence) == 'en':
            translated_text .append(sentence)
        else:
            to_translate = {"text": sentence, "to_lang": "en"}
            r = requests.post(url, data=json.dumps(to_translate), headers=headers)
            if r.status_code == 200:
                translation = json.loads(r.text)["translated_text"]
            else:
                translation = ''

            if detect_language(translation)=='en':
                translated_text .append(translation)

    translated_text = '. '.join(translated_text)

    row = pd.DataFrame([[id_project, translated_text]], columns=['actID', 'text'])
    projects_translated = pd.concat([projects_translated, row])
    
    if count % 500 == 0:
        projects_translated.to_parquet('translated_projects.parquet')


projects_translated.to_parquet('translated_projects.parquet')


projects_translated = projects_translated.rename(columns={'text':'translation'})
df = pd.merge(projects_translated_keywords, projects_translated, on='actID', how='outer')
df['StartYear'] = df['StartYear'].astype(float)
df['EndYear'] = df['EndYear'].astype(float)
df['translation'] = df['translation'].str.cat(df['Translated_Keywords'], sep=' ', na_rep='').str.strip()
df = df[df['translation'] != '']

df.to_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/projects_translated.parquet')