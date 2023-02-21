# Phone numbers pools generator

Just a side project made for the fun.  
**CAUTION: I am neither a telephony nor a Python pro** (this is my first Python script, lmao).  
This is probably not the most rigorous way to achieve the sake of this project.

## Features

- Data Persistence (MongoDB)
- Smart reload (Resumes at its last iteration)
- Deterministic generation (Finite generator)
- Unsafe mode (to force upserts on a specific pool interval)
- Configurable generator:
    - i18n configuration template
    - Country code
    - Operator codes
    - Fine-tuning rules:
        - Phone number length
        - Same digit threshold
        - Consecutive same digit threshold
        - Max heading zeros (at the beginning of the pseudo-randomly generated block)
        - Banned operator codes

## How to run

`$ python3 run.py`

### Dependencies

- [pymongo](https://pypi.org/project/pymongo/)
- [Python 3.8.10](www.python.org/)
- [MongoDB](https://www.mongodb.com/)
- [numba](https://pypi.org/project/numba/)
- CUDA
