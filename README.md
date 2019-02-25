TYSHscore Web
===

## A Flask based system.
For this build, only semestral exam is avaliable.

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

### Some thing needs to note here:

1. I `DO NOT` store any credentials
2. This project is licensed under the `MIT License`.

