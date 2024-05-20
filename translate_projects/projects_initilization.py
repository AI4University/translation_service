import pandas as pd

df = pd.read_parquet('data_ingest/match_semanticScholar_researchPortal/match_outputs/projects.parquet')
df = df[df['Keywords'].notna() | df['resumen'].notna()]

def limpiar_y_separar(texto):
    try:
        return texto[0]
    except:
        None

# Aplicar la función a la columna
df['Keywords'] = df['Keywords'].apply(limpiar_y_separar)
df['text'] = df['Keywords'].str.cat(df['resumen'], sep=' ', na_rep='').str.strip()

df.to_parquet('data_ingest/match_semanticScholar_researchPortal/match_outputs/projects_to_translate.parquet')