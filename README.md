# Phone numbers pool generator

Just a side project made for the fun.  
**CAUTION: I am neither a telephony nor a Python pro** (this is my first Python script, lmao).  
This is probably not the most rigorous way to achieve the sake of this project.

## Features

- Data Persistence (MongoDB)
- Smart reload (Resumes at its last iteration)
- Deterministic generation (Finite generator)
- Unsafe mode (to force a subpool upsert)
- Configurable generator:
    - i18n configuration template
    - Country code
    - Operator codes
    - Fine-tuning rules for the generation of the pseudo-random tail element

## How to run

`$ python3 phone_number_generator.py`

### Dependencies

- [pymongo](https://pypi.org/project/pymongo/)
