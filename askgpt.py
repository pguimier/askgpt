#!/usr/bin/python

import json
import requests
import configparser
import os

_VERSION = 0.1

userhome = os.path.expanduser('~')
configPath = userhome + '/.config/askgpt/'
configFile = configPath + 'config.cfg'
config = configparser.ConfigParser()

models = {
        1 : "text-ada-001",
        2 : "text-babbage-001",
        3 : "text-curie-001",
        4 : "text-davinci-003",
        5 : "code-davinci-002",
        6 : "code-cushman-001",
          }

default_config = """
[Api]
key = OPENAI_API_KEY
[Params]
model = text-curie-001
temperature = 0.5
tokens = 1024
"""

def read_config():
    try:
        with open(configFile, 'r') as f:
            f = f.read()
            config.read_string(f)
    except (IOError, OSError, FileNotFoundError):
        try:
            os.mkdir(configPath)
        except FileExistsError:
            pass
        # Set default config
        config.read_string(default_config)
        write_config()
        set_apikey()
    config.read(configFile)

def write_config():
    with open(configFile, 'w+') as f:
        config.write(f)

def set_apikey():
    api_key = input("OpenAI API key [default : " + config.get('Api', 'key') + "]: ")
    if len(api_key):
        config.set('Api', 'key', str(api_key))
        write_config()

def set_tokens():
    tokens = int(input("max tokens [default : " + config.get('Params', 'tokens') + "]: "))
    if tokens:
        config.set('Params', 'tokens', str(tokens))
        write_config()

def set_temperature():
    temperature = float(input("temperature [default : " + config.get('Params', 'temperature') + "]: "))
    if temperature:
        config.set('Params', 'temperature', str(temperature))
        write_config()

def set_model():
    for k in models.keys():
        print (k, ":", models[k])
    modelid = int(input("model [default : " + config.get('Params', 'model') + "]: "))
    if modelid:
        config.set('Params', 'model', str(models[modelid]))
        write_config()
    return models[modelid]

def askgpt (query):
    url = "https://api.openai.com/v1/engines/" + config.get('Params', 'model') + "/completions"
    read_config()
    api_key = config.get('Api', 'key')
    model = config.get('Params', 'model')
    temperature = float(config.get('Params', 'temperature'))
    tokens = int(config.get('Params', 'tokens'))
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # Definition of the query
    request_body = "{"
    request_body += f'"prompt": "{query}",'
    request_body += f'"max_tokens": {tokens},'
    request_body += f'"temperature": {temperature}'
    request_body += "}"

    # Sending the request
    response = requests.post(url, headers=headers, data=request_body)

    save_log(request_body, response.text)

    reponsetext = json.loads(response.text)['choices'][0]['text']

    # Display of the answer
    print(reponsetext)

def save_log(query, response):
    read_config()
    line = json.dumps({'query': query, 'response': response})
    with open(userhome + '/askgptlog.json', 'a') as f:
        f.write(line)
        f.write('\n')

def main():
    while True:
        read_config()
        model = config.get('Params', 'model')
        try:
            query = input(model + ": ")
            if query=="q" or query=="quit" :
                print("Quit")
                break;
            elif query=="" or query=="help" :
                print("Commands : help, api, model, tokens, temperature or quit")
                print("Otherwise, ask your question")
                continue
                break
            elif query=="api":
                set_apikey()
                continue
                break
            elif query=="model" or query=="models":
                set_model()
                continue
                break
            elif query=="token" or query=="tokens":
                set_tokens()
                continue
                break
            elif query=="temp" or query=="temperature":
                set_temperature()
                continue
                break
            else:
                askgpt(query)
                continue
        except ValueError:
            print("Invalid")
            continue

if __name__ == "__main__":
    main()
