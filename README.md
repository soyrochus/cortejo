# Cortejo

Creation of Cypress tests based on a human language definition (using AI)

## Why 'cortejo'? 

''En lenguaje claro,<br>
el cortejo de palabras,<br>
pruebas danzarán''

## Installation

Clone the repository. Use the dependency and package manager [Poetry](https://python-poetry.org/) to install all the dependencies of AItheneum.

```bash
poetry install
```

## Configuration for usage with OpenAI

Create a text file _"openai_api_key.env"_ in the root of the project. This will contain the "OPENAI_API_KEY" environment variable used by the application to obtain the token associated to a valid OpenAI account when calling the API.

```bash
OPENAI_API_KEY=sk-A_seCR_et_key_GENERATED_foryou_by_OPENAI
```
The key is loaded into the execution context of the application when run from the command line or run in the debugger.

Alternatively, if the file is not present, then 'AItheneum' will look for the environment variable "OPENAI_API_KEY".


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