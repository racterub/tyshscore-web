TYSHscore Web
===

## A Flask based system.
For this build, only semestral exam is avaliable.
**MAYBE** all skyweb's system works :/

Screenshot:

![screenshot](https://i.imgur.com/VjoMHLv.png)

## Structure

```
.
├── config.py #Few configs in here
├── log
├── requirements.txt
├── run_parser.sh #Call websites/tests/run_crawler.py for easier debugging
├── serve.py #Startup script
└── website
    ├── __init__.py
    ├── static #Stores static files
    ├── templates #Stores jinja templates
    ├── tests #Stores crawler debugging script
    │   └── run_crawler.py
    └── views #Stores views script
        ├── lib
        └── main.py
```
## How to use:
**This Project is using python3, and PLEASE use python3.**

1. Edit the config.
2. run `pip3 install -r requirements.txt`
3. run `python3 serve.py` (add dev at the end of the command will open debug mode)
4. Profit :)

### Some thing needs to note here:

1. I `DO NOT` store any credentials
2. This project is licensed under the `MIT License`.

