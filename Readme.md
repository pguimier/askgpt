# askGPT

A console interface to query openAI models

![Terminal animation](https://raw.githubusercontent.com/pguimier/askgpt/main/termtosvg_v0.2.svg)

## Description

Write a prompt to ask your questions to the OpenAI models; You can choose your model from those available.

However, it is necessary to enter your API key which can be generated here:

https://beta.openai.com/account/api-keys

## Utilisation

Just run the script :

`$ python askgpt.py`

On first use, you will be asked for your API key, then you can define the number max of tokens, the model, the temperature of your request with the commands:

`> tokens`
`> temperature`
`> model`

It is also possible to give argument to command:

`> tokens 1024`

`> temperature 0.6`

`> model text-curie-001`

To define another API key use the `api` command.

Then just ask your question to the selected model:

`text-curie-001> Who is Marie Curie ?`

In CLI mode, commands and queries are enabled :

`$ askgpt.py model text-davinci-003`

`$ askgpt.py tokens 256`

`$ askgpt.py "What is the capital of India ?"`

A log of conversations is saved in a file : ~/askgptlog.json

Configuration is stored in ~/.config/askgpt/config.cfg

## Dependencies

- Python 3
- Json module
- Configparser module
- requests module
- Cmd module

Optional modules:
- gnureadline
- termcolor

## History

### V0.2 - 2023-02-10

Colorful GPT shell or CLI

- [x] Shell-like prompt (with recallable commands and queries)
- [x] Touch of colors (optionnal with termcolor)
- [x] Initial CLI for commands and queries
- [ ] Can't recall commands/queries over sessions
- [ ] Can't autocomplete models (because of dashes)
- [ ] GPT responses are not colorized yet

### V0.1 - 2023-02-09

Initial commit

- [x] Configuration is OK
- [x] requests are doable
- [ ] Can't recall last command/query
- [ ] Can't arrow-back the query text to edit prompt