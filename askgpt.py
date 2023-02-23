#!/usr/bin/python
_VERSION = 0.4
_RELDATE = "2023-02-23"

import json,requests,configparser,os,cmd,sys,time
is_termcolor = False
try:from termcolor import colored,cprint;is_termcolor=True
except ImportError:pass
try:import gnureadline;sys.modules['readline']=gnureadline
except ImportError:pass
is_termmenu = False
try:from simple_term_menu import TerminalMenu;is_termmenu=True
except ImportError:pass
is_pygments = False
try:from pygments import formatters,highlight,lexers;from pygments.lexers import guess_lexer;is_pygments=True
except ImportError:pass

userhome = os.path.expanduser('~')
configPath = userhome + '/.config/askgpt/'
configFile = configPath + 'config.cfg'
config = configparser.ConfigParser()

models=['[default]','text-ada-001','text-babbage-001','text-curie-001','text-davinci-003','code-davinci-002','code-cushman-001']

default_config='\n[Api]\nkey = OPENAI_API_KEY\n[Params]\nmodel = text-curie-001\ntemperature = 0.5\ntokens = 1024\n'

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
    return tokens

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
    return temperature

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

    save_log(request_body, json.loads(response.text))
    reponsetext = "\n".join(json.loads(response.text)['choices'][0]['text'].split('\n')[2:])
    print(colorify_text(reponsetext))

def colorify_text(text):
  if is_pygments:
    lexer = guess_lexer(text)
    formatter = formatters.TerminalFormatter(bg="dark")  # dark or light
    highlighted_file_content = highlight(text, lexer, formatter)
    return highlighted_file_content
  else:
      return text

def save_log(query, response):
    read_config()
    line = json.dumps({'query': query, 'response': response})
    with open(userhome + '/askgptlog.json', 'a') as f:
        f.write(line)
        f.write('\n')

def read_log():
    logs = []
    with open(userhome + '/askgptlog.json', 'r') as f:
        Lines = f.readlines()
    for line in Lines:
        logs.append(line.strip())
    return logs

def list_history():
    if not is_termmenu:
        print ("python module simple-term-menu required")
        return
    titles = []
    Logs = read_log()
    for log in Logs:
        jsonlog = json.loads(log)
        titles.append(
            time.ctime(jsonlog['response']['created']) + " - "
            + jsonlog['response']['model'] + " - "
            + str(jsonlog['response']['usage']['total_tokens'])
            + " tokens"
            + "|" + jsonlog['query']['prompt'] + "\n"
            + "\n".join(jsonlog['response']['choices'][0]['text'].split('\n')[2:])
            )
    terminal_menu = TerminalMenu(titles, preview_command=preview_text, preview_size=0.5)
    menu_entry_index = terminal_menu.show()
    display_hist(menu_entry_index)

def preview_text (text):
    return colorify_text(text)

def display_hist(index):
    log = read_log()[index]
    jsonlog = json.loads(log)
    out=c(jsonlog['query']['prompt'], 'yellow') + "\n"
    out+=colorify_text("\n".join(jsonlog['response']['choices'][0]['text'].split('\n')[2:])) + "\n"
    print("\033c", end='') # clean screen
    print (out)

class AskGPT(cmd.Cmd):

    intro = c("AskGPT " + str(_VERSION) + " (" + _RELDATE + ")\n", "red")
    intro += c("Ask me anything.", "yellow")

    def default(self, query):
        askgpt(query)

    def do_api(self, line):
        set_apikey()

    def do_tokens(self, tokens):
        if tokens and int(tokens) <= 4096 :
            set_tokens(tokens)
        else :
            tokens = set_tokens()
        print (c("max_tokens set : " + str(tokens), "yellow"))

    def do_temperature(self, temperature):
        if temperature and float(temperature) <= 1 :
            set_temperature(temperature)
        else :
            temperature = set_temperature()
        print (c("temperature set : " + str(temperature), "yellow"))

    def do_model(self, model):
        global models
        if model and model in models:
            set_model(model)
        else :
            model = set_model()
        self.prompt = set_prompt()
        print (c(model + " selected", "yellow"))

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

    def do_history (self, line):
        list_history()

    def help_model(self):
        print('\n'.join([
            c('model [model]', 'yellow'),
            c('Set the model in configuration', 'blue'),
        ]))

    def help_tokens(self):
        print('\n'.join([
            c('tokens [max_tokens]', 'yellow'),
            c('Set the max_tokens in configuration', 'blue'),
        ]))

    def help_temperature(self):
        print('\n'.join([
            c('temperature [temperature]', 'yellow'),
            c('Set the temperature in configuration', 'blue'),
        ]))

    def help_api(self):
        print('\n'.join([
            c('api', 'yellow'),
            c('Set the OpenAI API key in configuration', 'blue'),
        ]))

    def help_info(self):
        print('\n'.join([
            c('info', 'yellow'),
            c('Display configuration information', 'blue'),
        ]))

    def help_default(self):
        print('\n'.join([
            c('query Your query', 'yellow'),
            c('Send your query to GPT3', 'blue'),
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

    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser(description=c('A console interface to query openAI models', 'yellow'))
        parser.add_argument('-t','--tokens', type=int, help=c('max tokens used', 'blue'))
        parser.add_argument('-r','--temperature', type=float, help=c('temperature required for the response', 'blue'))
        parser.add_argument('-m','--model', type=int, choices=range(1, 7), help=c('model used (1:ada, 2:babbage, 3:curie, 4:davinci, 5:code-davinci, 6:code-cushman)', 'blue'))
        parser.add_argument('-s','--stdin', action='store_true', help=c('if stdin has to be sent', 'blue'))
        parser.add_argument('-p','--prompt-repeat', action='store_true', help=c('repeat prompt at output', 'blue'))
        parser.add_argument('command', nargs='*', help=c('command to execute', 'blue'))
        args = parser.parse_args()

        if args.tokens is not None:
            set_tokens(args.tokens)

        if args.temperature is not None:
            set_temperature(args.temperature)

        if args.model is not None:
            set_model(str(models[args.model]))

        # in case datas are piped via stdin
        multiline_text = ''
        if args.stdin :
            for line in sys.stdin:
                multiline_text += "\n" + line

        command = ' '.join(args.command).replace('\\n', '\n') + multiline_text

        if args.prompt_repeat :
            print (command)

    myGpt.config = config
    myGpt.prompt = set_prompt()

    if len(command) > 1 :
        myGpt.onecmd(command)
    else:
        myGpt.cmdloop()