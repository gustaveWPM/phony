# ☎️ Phony

**CAUTION: I am neither a telephony nor a Python pro** (this is my first Python script, lmao).  
This is probably not the most rigorous way to achieve the sake of this project.  
Remember that it is just a side project made for the fun.  

## Features

- Data Persistence (MongoDB)
- Deterministic generation (Finite generator)
- Configuration:
    - i18n configuration template
    - Country code
    - Operator codes
    - Operator codes order shuffling
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
