from dotenv import load_dotenv
import os
import psycopg2
from abc import ABC, abstractmethod

load_dotenv()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv('POSTGRESSQL_HOST'),
    database=os.getenv('POSTGRESSQL_DATABASE_NAME'),
    user=os.getenv('POSTGRESSQL_USER'),
    password=os.getenv('POSTGRESSQL_PASSWORD')
)

# Create a cursor
cursor = conn.cursor()

class User(ABC):
    def __init__(self, user_id: int):
        self.user_id = user_id

    @abstractmethod
    def menu(self):
        pass

def main():
    # welcome text
    print(r"""
                           _____   ___   _   _
                          |  ___| |_ _| | | | |
                          | |_     | |  | | | |
                          |  _|    | |  | |_| |
                          |_|     |___|  \___/

                        Bus Route Management System
                               Version 1.0
    """)
    print('--------- Login ---------')
    username = input("Username: ")
    password = input("Password: ")

    # login
    auth_query = "SELECT role_id, user_id FROM Users WHERE username = %s AND password = %s"
    cursor.execute(auth_query, (username, password))
    user_info = cursor.fetchone()

    # display menus
    if user_info:
        print("Login successful!")
        role_id, user_id = user_info

        while True:
            print('\n--------- Select ---------')
            if role_id == 1:  # Driver
                pass # TODO: add the driver menu
            elif role_id == 2:  # Rider
                pass # TODO: add the rider menu
            elif role_id == 3:  # Admin
                pass # TODO: add the admin menu
            else:
                print("Unknown role. Try again!")

            selection = input("Do you want to logout? (y/n): ")
            if selection.lower() == "y":
                print('\n--------- Logout ---------')
                print("Logging off...")
                break
    else:
        print("User not found. Unable to login!")


if __name__ == "__main__":
    main()
