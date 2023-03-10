# askGPT

A console TUI/CLI to query openAI models

![Terminal animation](https://raw.githubusercontent.com/pguimier/askgpt/main/termtosvg_v0.2.2.svg)

## Description

Shell-like interface to send queries to OpenAI models.

It is necessary to enter your API key which can be generated here: https://beta.openai.com/account/api-keys

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

Previous queries and responses are availables suing `history` command:

![History example](https://raw.githubusercontent.com/pguimier/askgpt/main/askgpt_3.0_history.png)

![History screen with colored code](https://raw.githubusercontent.com/pguimier/askgpt/main/askgpt_0.4_CodeColor.png)

In CLI mode, commands and queries are enabled :

`$ askgpt.py model text-davinci-003`

`$ askgpt.py tokens 256`

`$ askgpt.py info`

`$ askgpt.py history`

`$ askgpt.py -t 120 -r 0.2 -m 2 "What is the capital of India ?"`

Options are described by invoquing :

`$ askgpt.py --help`


A log of conversations is saved in a file : ~/askgptlog.json

Configuration is stored in ~/.config/askgpt/config.cfg

## Tips & tricks

- In [Termux](https://github.com/termux), add askgpt.py to ~/.shortcuts directory to invoke it from the home widget (using termux-widget)
- To give a file in stdin, use :
	`$ askgpt.py -m 5 -t 500 -r 0.5 "Find why I got error messages in following script: " $(cat myscript.lua)`
	or
	`$ cat myscript.lua | askgpt.py --model 5 --tokens 500 --temperature 0.5 --stdin "Find why I got error messages in following script: "`
- Use [bat](https://github.com/sharkdp/bat) to output response with color and line numbers:
	`$ askgpt.py -m 5 -t 122 -r 0.2 '"""\nAsk the user for his name and say "Hello"\n"""' | bat -l python`

## Dependencies

- Python 3

Required modules :
- Json
- Configparser
- requests
- Cmd
- argparse
- sys
- time

Optional modules:
- gnureadline
- termcolor
- simple_term_menu for history display
- pygments for code colorization

## History

### V0.4 - 2023-02-23

Output colorified code Version

- [x] Ouput responses are colorized using pygments module, in queries and history
- [x] Code cleaning

### V0.3 - 2023-02-19

History display version

- [x] Previous queries and responses can be recalled

### V0.2.3 - 2023-02-19

CLI with options

- [x] Options to repeat prompt at output
- [x] Commands feedback additions
- [x] Colors in help

### V0.2.2 - 2023-02-18

CLI with options

- [x] Options to send stdin, before sending request
- [x] Bug fix

### V0.2.1 - 2023-02-16

CLI with options

- [x] Options to change temperature, max_tokens and model directly on the command line, before sending request
- [x] Bug fix (model 0 is not a change)
- [ ] Insertion / Edition modes not implemented yet

### V0.2 - 2023-02-10

Colorful GPT shell or CLI

- [x] Shell-like prompt (with recallable commands and queries)
- [x] Touch of colors (optional with termcolor)
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