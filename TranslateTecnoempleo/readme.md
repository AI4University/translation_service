# Translation Tecnoempleo
Jupyter notebooks with the automatized process to translate the tecnoempleo database.

> [!NOTE]
> The resulting database is too large to upload it on GitHub, you can find them in the following route: `smb://vanir.tsc.uc3m.es/data_ml4ds/IntelComp/Datasets/tecnoempleo/translation`

### Contents
- `Traduccion.ipynb` contains the pipeline to explore the data and to translate the title, skills and description of all job offers to Spanish (if they are in another language)
  
### Outputs (in the folder of the `vanir.tsc.uc3m.es` server)
- `tecnoempleo_translated.parquet`: Contains the raw translation.
- `complete_tecnoempleo_spanish.parquet`: Contains all the information merged form the original database (tecnoempleo) and the translated rows.

Last update: June, 2024.
