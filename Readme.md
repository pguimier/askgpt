# askGPT

A console interface to query openAI models

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

It is also possible to define another API key with the "api" command.

Then just ask your question to the selected model.

A log of conversation is saved in a file : ~/askgptlog.json

Configuration is stored in ~/.config/askgpt/config.cfg

## Dependencies

- Python
- Json module
- Configparser module
- requests module

## History

### V0.1 - 2023-02-09

Initial commit

- [x] Configuration is OK
- [x] requests are doable
- [ ] Can't recall last command/query
- [ ] Can't arrow-back the query text to edit prompt