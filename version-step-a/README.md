# User Data Fetcher and Processor

This project is designed to retrieve, sanitize, and save user data from the RandomUser.me API to a CSV file. RandomUser is a free, open-source API for generating random user data.

## Features

- **Data Retrieval**: Fetches random user data from the RandomUser.me API.
- **Data Sanitization**: Processes and sanitizes user data using custom logic encapsulated in the `Sanitizer` class.
- **Data Persistence**: Saves the sanitized user data into a CSV file for easy access and analysis.

## Installation

To run this application, you will need Python 3.6 or later. Clone this repository to your local machine using:

```bash
git clone https://github.com/indamutsa/SEC-fullastack-ebury.git
cd SEC-fullastack-ebury
```

The folder structure of the project is as follows:

```md
❯ tree -L 2 .
.
├── README.md
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

Let us get working container:
Follow the instructions [here](../working-container.md) to get started.
Nothing will be installed on your machine regarding the dependencies. You need to have docker installed on your machine.
Inside the container, you will have the current project folder, so everything done in the container will be reflected on your local machine.

Create a virtual environment using the following command:

```bash
python3 -m venv pyenv

# Activate the virtual environment
source pyenv/bin/activate
```

Verify the virtual environment is activated by checking the python version:

```bash
which python # should point to the virtual environment
python --version # Verify the python you are using...
```

Make sure the project is reproducible by locking dependencies using the following command:

```bash
pip freeze > requirements.txt

# Next time, install the dependencies using the following command:
pip install -r requirements.txt
```

## Usage

To start fetching, processing, and saving user data, simply run the `main.py` script:

```bash
python main.py
```

By default, the script fetches data for 10 users. You can modify this number directly in the `main.py` file or enhance the script to accept command-line arguments for greater flexibility.

## Configuration

- **API Endpoint**: The script uses `https://randomuser.me/api/?results={num_users}` to fetch user data. You can adjust the `num_users` parameter in the `fetch_random_users` function to control the number of users fetched.
- **Output File**: User data is saved in `solutions/results.csv`. This path can be modified in the `write_to_csv` function.
