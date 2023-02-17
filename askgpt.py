#!/usr/bin/python

import json
import requests
import configparser
import os
import cmd

is_termcolor = False
try:
    from termcolor import colored, cprint
    is_termcolor = True
except ImportError:
    pass

try:
    import gnureadline
    import sys
    sys.modules['readline'] = gnureadline
except ImportError:
    pass

_VERSION = 0.2_1
_RELDATE = "2023-02-16"

userhome = os.path.expanduser('~')
configPath = userhome + '/.config/askgpt/'
configFile = configPath + 'config.cfg'
config = configparser.ConfigParser()

models = [
    "[default]",
    "text-ada-001",
    "text-babbage-001",
    "text-curie-001",
    "text-davinci-003",
    "code-davinci-002",
    "code-cushman-001",
]


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

def set_tokens(tokens = None):
    if tokens is None:
        print (c("Enter an integer (max 4096 for text-davinci-003)", "yellow"))
        try:
            tokens = int(input("max tokens [default : " + config.get('Params', 'tokens') + "]: "))
        except ValueError:
            tokens = config.get('Params', 'tokens')
    if tokens != "":
        config.set('Params', 'tokens', str(tokens))
        write_config()

def set_temperature(temperature = None):
    if temperature is None:
        print (c("Enter a decimal number between 0 and 1", "yellow"))
        try:
            temperature = float(input("temperature [default : " + config.get('Params', 'temperature') + "]: "))
        except ValueError:
            temperature = config.get('Params', 'temperature')
    if temperature !="":
        config.set('Params', 'temperature', str(temperature))
        write_config()

def set_model(model = None):
    if model is None:
        print (c("Enter the number of your choosen model:", "yellow"))
        for k in models:
            print (models.index(k), ":", k)
        modelid = int(input("model [default : " + config.get('Params', 'model') + "]: "))
        if modelid:
            config.set('Params', 'model', str(models[modelid]))
            write_config()
        return models[modelid]
    else:
        config.set('Params', 'model', str(model))
        write_config()
        return model

def set_prompt():
    prompt = c(config.get('Params', 'model'), 'green')
    prompt += "> "
    return prompt

def print_config():
    print('\n\t'.join([
        c('Configuration set:', 'blue'),
        'model: ' + config.get('Params', 'model'),
        'temperature: ' + config.get('Params', 'temperature'),
        'max_tokens: ' + config.get('Params', 'tokens'),''
    ]))

def print_version():
    print('\n'.join([
        c('askGPT version: ', 'blue') + str(_VERSION) + ' ' + str(_RELDATE),
        'https://github.com/pguimier/askgpt',''
    ]))

def print_about():
    print('\n\t'.join([
        c('Useful links: ', 'blue'),
        'Account usage: https://platform.openai.com/account/usage',
        'OpenAI availability: https://status.openai.com/'
    ]))

def c(myString, color):
    if is_termcolor:
        return colored(myString, color)
    else:
        return myString

def askgpt (query):
    url = "https://api.openai.com/v1/completions"
    read_config()
    api_key = config.get('Api', 'key')
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    request_body = {
        "prompt": query,
        "model": config.get('Params', 'model'),
        "max_tokens": int(config.get('Params', 'tokens')),
        "temperature": float(config.get('Params', 'temperature')),
    }
    response = requests.post(url, headers=headers, json=request_body)

    save_log(request_body, response.text)
    reponsetext = json.loads(response.text)['choices'][0]['text']
    print(reponsetext)

def save_log(query, response):
    read_config()
    line = json.dumps({'query': query, 'response': response})
    with open(userhome + '/askgptlog.json', 'a') as f:
        f.write(line)
        f.write('\n')

class AskGPT(cmd.Cmd):

    intro = c("Ask me anything.", "yellow")

    def default(self, query):
        askgpt(query)

    def do_api(self, line):
        set_apikey()

    def do_tokens(self, tokens):
        if tokens and int(tokens) <= 4096 :
            set_tokens(tokens)
        else :
            set_tokens()

    def do_temperature(self, temperature):
        if temperature and float(temperature) <= 1 :
            set_temperature(temperature)
        else :
            set_temperature()

    def do_model(self, model):
        global models
        if model and model in models:
            set_model(model)
            print (model + " selected")
        else :
            model = set_model()
        self.prompt = set_prompt()

    def complete_model(self, text, line, begidx, endidx):
        global models
        if not text:
            completions = models[:]
        else:
            completions = [
                f
                for f in models
                if f.startswith(text)
            ]
        return completions

    def do_info (self, line):
        print_version()
        print_config()
        print_about()

    def help_model(self):
        print('\n'.join([
            'model [model]',
            'Set the model in configuration',
        ]))

    def help_tokens(self):
        print('\n'.join([
            'tokens [max_tokens]',
            'Set the max_tokens in configuration',
        ]))

    def help_temperature(self):
        print('\n'.join([
            'temperature [temperature]',
            'Set the temperature in configuration',
        ]))

    def help_api(self):
        print('\n'.join([
            'api',
            'Set the OpenAI API key in configuration',
        ]))

    def help_info(self):
        print('\n'.join([
            'info',
            'Display configuration information',
        ]))

    def help_default(self):
        print('\n'.join([
            'query Your query',
            'Send your query to GPT3',
        ]))

    def emptyline(self):
        pass

    def do_exit(self, line):
        print("\n")
        return True

    def do_quit(self, line):
        print("\n")
        return True
    def do_EOF(self, line):
        print("\n")
        return True

if __name__ == "__main__":
    myGpt = AskGPT()
    read_config()
    command = ''

    import sys
    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser(description='A console interface to query openAI models')
        parser.add_argument('-t','--tokens', type=int, help='max tokens used')
        parser.add_argument('-r','--temperature', type=float, help='temperature required for the response')
        parser.add_argument('-m','--model', type=int, choices=range(1, 7), help='model used (1:ada, 2:babbage, 3:curie, 4:davinci, 5:code-davinci, 6:code-cushman)')
        parser.add_argument('command', nargs='*', help='command to execute')
        args = parser.parse_args()

        if args.tokens is not None:
            set_tokens(args.tokens)

        if args.temperature is not None:
            set_temperature(args.temperature)

        if args.model is not None:
            set_model(str(models[args.model]))

        command = ' '.join(args.command)

    myGpt.config = config
    myGpt.prompt = set_prompt()

    if len(command) > 1 :
        myGpt.onecmd(command)
    else:
        myGpt.cmdloop()