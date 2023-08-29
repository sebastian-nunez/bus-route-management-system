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


class Rider(User):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    def view_available_routes(self):
        query = "SELECT route_id, route_name, start_point, end_point FROM Routes"
        cursor.execute(query)
        available_routes = cursor.fetchall()

        print("Available Routes:")
        for route in available_routes:
            print("Route ID:", route[0])
            print("Route Name:", route[1])
            print("Start Point:", route[2])
            print("End Point:", route[3])
            print("---------------------")

    def express_interest(self, route_id: int):
        query = "INSERT INTO RiderRoutes (rider_id, route_id) VALUES (%s, %s)"
        cursor.execute(query, (self.user_id, route_id))
        conn.commit()

        print(f"Success! Route {route_id} was added for Rider {self.user_id}.")

    def menu(self):
        print("Rider Menu")
        print("1. View Available Routes")
        print("2. Express Interest in a Route")
        selection = int(input("Make a selection: "))
        print("---------------------------")

        if selection == 1:
            self.view_available_routes()
        elif selection == 2:
            route_id = int(input("Enter the Route ID: "))
            self.express_interest(route_id)
        else:
            print("Invalid selection.")


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
                driver = Driver(user_id)
                driver.menu()
            elif role_id == 2:  # Rider
                rider = Rider(user_id)
                rider.menu()
            elif role_id == 3:  # Admin
                admin = Admin(user_id)
                admin.menu()
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
    while True:
        main()

        selection = input("Do you want to quit? (y/n): ")
        if selection.lower() == "y":
            print('\n--------- Quit ---------')
            print("Quitting the Bus Route Management System...")
            break
