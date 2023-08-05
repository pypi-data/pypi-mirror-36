# pcu_json (JSON parser for PCU project)

JSON parser component for PCU project.
From the path of a json file, get its textual content.

[Check PCU project][pcu].

[pcu]: https://github.com/zevio/pcu_core

----

## Usage in another project

If you wish to import this module in another Python project, please install it :

`pip install pcu-json`

Then, add this import line at the beginning of your Python file :

`from pcu_json import json_parser`

You can now use pcu_nlp's functions, for example :

`json_parser.JSONParser(path/to/json/file)`

## Test

To test your installation, go to pcu_json/ directory and execute the Makefile with the following command line : 

`make test`
