# Test 1

The folder structure of the project is as follows:

```md
❯ tree -L 2 .
.
├── README.md
├── image.png
├── main.py
├── pyenv
│ ├── bin
│ ├── include
│ ├── lib
│ └── pyvenv.cfg
├── test
└── utils
└── helper.py

7 directories, 5 files
```

Create a virtual environment using the following command:

```bash
python3 -m venv pyenv

# Activate the virtual environment
source pyenv/bin/activate
```

Verify the virtual environment is activated by checking the python version:

```bash
which python # should point to the virtual environment
python --version
```

Make sure the project is reproducible by locking dependencies using the following command:

```bash
pip freeze > requirements.txt

# Next time, install the dependencies using the following command:
pip install -r requirements.txt
```
