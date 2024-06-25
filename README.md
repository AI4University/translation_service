Application creation for translation of big datasets form the detected language to the desired one.
- Check that the Docker destinated for translation are preloaded. In case not load them with:
  - docker load --input tilde-intelcomp-xx-xx.tar.gz   
- Run the docker compose file using:
  - docker-compose -p traductor -f docker-compose.yml up --build
- Run the application allocated at port 10000 using:
  - curl -X POST -H "Content-Type: application/json" -d '{"text": "TEXT_TO_TRANSLATE", "to_lang": "LANGUAGE_CODE"}' http://kumo01:10000/translate

> [!CAUTION]
> Currently, the translation service is down. Try the translation pipelines (using Google Translate API) available in the [TranslateTecnoempleo](TranslateTecnoempleo/Traduccion.ipynb) and [TranslateResearchPortal](TranslateResearchPortal/TranslationKeywords.ipynb) folders.
