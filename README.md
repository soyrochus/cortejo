# Cortejo

Creation of tests based on a human language definition (using AI)

## Why 'cortejo'? 

''En lenguaje claro,<br>
el cortejo de palabras,<br>
pruebas danzarán''

## Usage 

```bash
❯ cortejo -h
usage: cortejo [-h] [-c CONFIG] test_def_path [project_path]

Create tests based on a human language definition (using AI)

positional arguments:
  test_def_path         Path to the test definition Excel file
  project_path          Project Path (default: current directory)

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the config TOML file (take "{current_dir}/cortejo.toml" if not set)
```

The test definition Excel file contains the human readable test definitions. See the [example file](data/test-data.xlsx). Use cases contain a number of test cases. Use cases are grouped by Bounded context.

Generated tests are generated in a file per use case. The files are stored in a directory per corresponding Bounded context. 

The data from this file is used to expand templates which are used to be send as prompts to the OpenAI LLM. 
Each bounded context/use case collection can have a template associated with it by naming it '{bounded_context}-{use_case}.j2', for example: "auth_login.j2" (see the example excel file).

There must be a template with name '\__default\__.j2' to serve as default/fallback case.

For the specification of the tests, see the [example Toml file](test_cortejo.toml).
The [tests] section contains two mandatory items:

```bash
#mandatory configuration
[tests]
tests-path="cypress/e2e"  #path generate the tests
templates-path = "cypress/templates" #path to the Jinja2 templates
```

The templates-path directory must point to a directory containing [Jinja2](https://jinja.palletsprojects.com/) templates. The templates is passed the following parameters:

- bounded_context: First column of the Excel data 
- use_case: Second column of the Excel data
- list: list of columns from the Excel with the bounded_context and use_case as given, with the rows marked with "skip generation" set to "yes" filtered out.

## Installation

Clone the repository. Use the dependency and package manager [Poetry](https://python-poetry.org/) to install all the dependencies of Cortejo.

```bash
poetry install
```

## Configuration for usage with OpenAI

Create a text file _"openai_api_key.env"_ in the root of the project. This will contain the "OPENAI_API_KEY" environment variable used by the application to obtain the token associated to a valid OpenAI account when calling the API.

```bash
OPENAI_API_KEY=sk-A_seCR_et_key_GENERATED_foryou_by_OPENAI
```
The key is loaded into the execution context of the application when run from the command line or run in the debugger.

Alternatively, if the file is not present, then 'Cortejo' will look for the environment variable "OPENAI_API_KEY".


## Development
[Activate the Python virtual environment](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment) with

```bash
poetry shell
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Copyright and license

Copyright © 2024 Iwan van der Kleijn

Licensed under the MIT License 
[MIT](https://choosealicense.com/licenses/mit/)