import json 
import requests
import os
from langdetect import detect
from flask import Flask, request, jsonify, send_file
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.yml'  # Esta es la ruta donde se sirve tu especificación de Swagger

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Opcional: Configura la interfaz de Swagger UI
        'app_name': "Translation Service API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text_to_translate = data.get('text')
        to_lang = data.get('to_lang')

        # Detect original language and define traduction language
        from_lang = detect_language(text_to_translate)

        # Obtain the port
        port = define_port(from_lang, to_lang)

        # Translates the text
        translated_text = translate_text(text_to_translate, port)
        return jsonify({'Text': text_to_translate, 'translated_text': translated_text})

    except Exception as e:
        return jsonify({'error': f"Error translating text: {e}"}), 500

@app.route('/swagger.yml')
def swagger():
    return send_file('swagger.yml', mimetype='text/yaml')


def translate_text(text, port):
    '''
    Receives the text, breaks it into sentences and traduces each sentence

    text -> Text to traduce
    port -> Port where the traductor is located
    '''
    url = "http://kumo01.tsc.uc3m.es:{}/api/1.0.0/translate".format(str(port))
    headers = {'content-type': 'application/json'}

    text_to_translate = {'texts': [sentence.strip() for sentence in text.split('.') if sentence.strip()]}
    text_to_translate = json.dumps(text_to_translate)

    response = requests.post(url, data=text_to_translate, headers=headers)
    translations = json.loads(response.text)

    translated_text = ' '.join([t['translation'] for t in translations['translations']])
    return translated_text

def detect_language(text): 
    '''
    Receives the text and detects its language

    text -> Text to detect the language
    '''
    try: 
        lang = detect(text)

    except: 
        lang = None
    
    return lang

def define_port(from_lang, to_lang):
    '''
    Receives the original language and the desired language and defines the port where that traductor is allocated

    from_language -> Original language of the text
    to_language -> Desired language
    '''
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        key = from_lang+'-'+to_lang
        port = config[key]
        return port

    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

