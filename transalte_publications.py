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

publications = pd.read_parquet(path + 'publications.parquet')
publications_translated = pd.DataFrame(columns=['id_paper', 'text'])
publications_translated = pd.read_parquet('/Volumes/usuarios_ml4ds/mbalairon/github/translated_publications.parquet')

publications = publications.dropna(subset=['abstract']) 


ids_to_translated = list(set(publications['id_paper']) - set(publications_translated['id_paper']))
indexes = list(publications[publications['id_paper'].isin(ids_to_translated)].index)

count = 0
for i in tqdm(indexes, desc="Procesando publicaciones"):
    count +=1
    id_paper = publications['id_paper'][i]
    title = publications['title'][i]
    abstract = publications['abstract'][i]

    if '='  in title:
        title = clean_equals(title)
    
    if '='  in abstract:
        abstract = clean_equals(abstract)

    text_to_translate = limpiar_resumenes(title + '. ' + abstract)
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

    row = pd.DataFrame([[id_paper, translated_text]], columns=['id_paper', 'text'])
    publications_translated = pd.concat([publications_translated, row])
    
    if count % 1000 == 0:
        publications_translated.to_parquet('/Volumes/usuarios_ml4ds/mbalairon/github/translated_publications.parquet')


publications_translated.to_parquet('/Volumes/usuarios_ml4ds/mbalairon/github/translated_publications.parquet')


publications_translated = publications_translated.rename(columns={'text':'translation'})
df = pd.merge(publications, publications_translated, on='id_paper')
df.to_parquet('/Volumes/data_ml4ds/AI4U/Datasets/ResearchPortal/20240321/processed_parquets/publications_translated.parquet')