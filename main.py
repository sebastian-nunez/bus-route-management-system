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


class Driver(User):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    def view_assigned_routes(self):
        query = """
        SELECT Routes.route_id, Routes.route_name, Routes.start_point, Routes.end_point, Routes.distance
        FROM DriverRoutes
        JOIN Routes ON DriverRoutes.route_id = Routes.route_id
        WHERE DriverRoutes.driver_id = %s
        """
        cursor.execute(query, (self.user_id,))
        assigned_routes = cursor.fetchall()

        print("Assigned Routes:")
        for route in assigned_routes:
            print("Route ID:", route[0])
            print("Route Name:", route[1])
            print("Start Point:", route[2])
            print("End Point:", route[3])
            print("Distance (miles):", route[4])
            print("---------------------------")

    def update_route_information(self, route_id: int, new_distance: float):
        query = "UPDATE Routes SET distance = %s WHERE route_id = %s"
        cursor.execute(query, (new_distance, route_id))
        conn.commit()

        print(f"Route {route_id} distance updated to {new_distance}mi")

    def menu(self):
        print("Driver Menu")
        print("1. View Assigned Routes")
        print("2. Update Route Information")
        selection = int(input("Make a selection: "))
        print("---------------------------")

        if selection == 1:
            self.view_assigned_routes()
        elif selection == 2:
            route_id = int(input("Enter the Route ID: "))
            new_distance = float(input("Enter the new distance (miles): "))
            self.update_route_information(route_id, new_distance)
        else:
            print("Invalid selection.")


class Admin(User):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    def view_available_routes(self):
        query = "SELECT route_id, route_name, start_point, end_point, distance FROM Routes"
        cursor.execute(query)
        available_routes = cursor.fetchall()

        print("Available Routes:")
        for route in available_routes:
            print("Route ID:", route[0])
            print("Route Name:", route[1])
            print("Start Point:", route[2])
            print("End Point:", route[3])
            print("Distance (miles):", route[4])
            print("---------------------")

    def change_password(self, user_id: int, new_password: str):
        query = "UPDATE Users SET password = %s WHERE user_id = %s"
        cursor.execute(query, (new_password, user_id))
        conn.commit()

        print(f"Changed the password of user {user_id}!")

    def view_all_users(self):
        query = """
        SELECT Users.user_id, Users.username, Users.password, Roles.role_name
        FROM Users
        JOIN Roles ON Users.role_id = Roles.role_id
        """
        cursor.execute(query)
        users = cursor.fetchall()

        print("All Users:")
        for user in users:
            print("User ID:", user[0])
            print("Username:", user[1])
            print("Password:", user[2])
            print("Role:", user[3])
            print("---------------------------")

    def add_new_route(self, route_name, start_point, end_point, distance):
        query = """
        INSERT INTO Routes (route_name, start_point, end_point, distance)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (route_name, start_point, end_point, distance))
        conn.commit()
        print("New route added successfully.")

    def remove_route(self, route_id):
        query = "DELETE FROM Routes WHERE route_id = %s"
        cursor.execute(query, (route_id,))
        conn.commit()
        print("Route removed successfully.")

    def menu(self):
        print("Admin Menu")
        print("1. View All Users")
        print("2. Change Password")
        print("3. View Available Routes")
        print("4. Add New Route")
        print("5. Remove Route")
        selection = int(input("Make a selection: "))
        print("---------------------------")

        if selection == 1:
            self.view_all_users()
        elif selection == 2:
            user_id = int(input("Enter the User ID: "))
            new_password = input("Enter the new password: ")
            self.change_password(user_id, new_password)
        elif selection == 3:
            self.view_available_routes()
        elif selection == 4:
            route_name = input("Enter the route name: ")
            start_point = input("Enter the start point: ")
            end_point = input("Enter the end point: ")
            distance = float(input("Enter the distance (miles): "))
            self.add_new_route(route_name, start_point, end_point, distance)
        elif selection == 5:
            route_id = int(input("Enter the Route ID: "))
            self.remove_route(route_id)
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

            # logout option
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
