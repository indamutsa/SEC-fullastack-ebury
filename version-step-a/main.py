import requests, csv, os
from utils.helper import Sanitizer

def fetch_random_users(num_users=10):
    url = f"https://randomuser.me/api/?results={num_users}"
    try:
        response = requests.get(url, verify=True) # Ensure ssl verification is enabled
        response.raise_for_status() # checks if the request was successful
        data = response.json()
        return data['results']
    except requests.RequestException as e:
        print(f"Failed to fetch users: {e}")
        return []

def process_users(users):
    process_users = []

    for user in users:
        processed_user = {
            "name": f"{Sanitizer(user['name']['first']).get_valid_name()} {Sanitizer(user['name']['last']).get_valid_name()}" ,
            "username": f"{Sanitizer(user['login']['username']).get_valid_username()}",
            "email": f"{Sanitizer(user['email']).get_valid_email()}",
            "phone": f"{Sanitizer(user['phone']).get_valid_phone()}",
            "city": f"{Sanitizer(user['location']['city']).get_valid_location()}",
            "country": f"{Sanitizer(user['location']['country']).get_valid_location()}"
        }

        process_users.append(processed_user)

    return process_users

# This function checks if the file exists, if not it creates a new file and writes the data to it.
import os
import csv

def write_to_csv(users, filename="solutions/results.csv"):
    """
    Write a list of user dictionaries to a CSV file.

    Args:
        users (list): A list of dictionaries representing user data.
        filename (str, optional): The name of the CSV file to write to. Defaults to "solutions/results.csv".

    Returns:
        None
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Check if the file exists to decide the mode ('a' for append, 'w' for write)
    file_exists = os.path.isfile(filename)
    mode = 'a' if file_exists else 'w'

    fields = ["name", "username", "email", "phone", "city", "country"]
    with open(filename, mode=mode, newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if not file_exists:
            writer.writeheader()
        
        for user in users:
            writer.writerow(user)



def main():
    users = fetch_random_users()
    processed_users = process_users(users)
    write_to_csv(processed_users)

if __name__ == "__main__":
    main()