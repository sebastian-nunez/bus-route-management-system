# Bus Route Management System

> A command line interface (CLI) designed to ease the management of a bus transportation network. This system provides a streamlined way for administrators, drivers, and riders to interact with the system according to their respective roles.

## Features

1. **Role-Based Access:** Each role is granted access to specific functions aligned with their responsibilities.

   1. **Riders**

      1. View all routes
      2. View interested routes
      3. Express interest in specific routes

   2. **Drivers**

      1. View their assigned routes
      2. Update route distance

   3. **Admins:**
      1. View all user accounts with full details
      2. Update a user's password
      3. View available routes
      4. Create new routes
      5. Remove existing routes
      6. Assign a route
      7. View all assigned routes

2. **Database Backend:** Utilizing a `PostgreSQL` database, the system stores user data, bus route details, and associations between drivers and routes.

3. **Command Line Interface:** Users interact with the system through a command line interface, which presents clear menus and prompts based on their respective roles.

4. **Modular Design:** The system's modular architecture enables the seamless addition of new features in the future.

## Tables

### `Roles`

| Column    | Data Type    | Constraints | Description |
| --------- | ------------ | ----------- | ----------- |
| role_id   | SERIAL       | PRIMARY KEY | Role ID     |
| role_name | VARCHAR(255) | NOT NULL    | Role name   |

#### Mappings _(role_id -> role_name)_

| role_id | role_name |
| ------- | --------- |
| 1       | Driver    |
| 2       | Rider     |
| 3       | Admin     |

#### Permissions

- `Routes` Table
  - **Riders** have `SELECT` access
  - **Drivers** have `SELECT` and `INSERT`
  - **Admins** have full privileges (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, etc.)

### `Users`

| Column   | Data Type    | Constraints      | Description  |
| -------- | ------------ | ---------------- | ------------ |
| user_id  | SERIAL       | PRIMARY KEY      | User ID      |
| username | VARCHAR(255) | UNIQUE, NOT NULL | Username     |
| password | VARCHAR(255) | NOT NULL         | Password     |
| role_id  | INT          |                  | Role ID (FK) |

### `Routes`

| Column      | Data Type    | Constraints | Description |
| ----------- | ------------ | ----------- | ----------- |
| route_id    | SERIAL       | PRIMARY KEY | Route ID    |
| route_name  | VARCHAR(255) | NOT NULL    | Route name  |
| start_point | VARCHAR(255) | NOT NULL    | Start point |
| end_point   | VARCHAR(255) | NOT NULL    | End point   |
| distance    | FLOAT        |             | Distance    |

### `DriverRoutes`

| Column    | Data Type | Constraints | Description    |
| --------- | --------- | ----------- | -------------- |
| driver_id | INT       | FK (Users)  | Driver ID (FK) |
| route_id  | INT       | FK (Routes) | Route ID (FK)  |

### `RiderRoutes`

| Column   | Data Type | Constraints | Description   |
| -------- | --------- | ----------- | ------------- |
| rider_id | INT       | FK (Users)  | Rider ID (FK) |
| route_id | INT       | FK (Routes) | Route ID (FK) |

## Relationships

- `Users` are associated with roles through the `role_id` foreign key in the `Users` table. This establishes a **one-to-many** relationship between roles and users.
- The `DriverRoutes` table establishes a **many-to-many** relationship between drivers and routes. Each entry associates a driver (user) with a specific route.
- The `RiderRoutes` table also establishes a **many-to-many** relationship between riders and routes. Each entry associates a rider (user) with a specific route.

## Running Locally

1. **Install `PostgreSQL` and other dependencies**

   - Ensure you have `PostgreSQL` installed and can access the `psql` shell
   - Install the project dependencies:

     ```bash
     pip install -r requirements.txt
     ```

2. **Create `PostgresSQL` Database and Tables**

   > This will create the necessary tables and populate them with sample data.

   - Login into `psql` console: `psql -U postgres`
   - Create the `bus_route_management` database: `CREATE DATABASE bus_route_management;`
   - Open a terminal and run the following command:

     ```bash
     psql -U postgres -d bus_route_management -a -f setup_bus_routes.sql
     ```

   - **Note:** Replace `-U postgres` with your PostgreSQL username if it's different.

3. **Update Database Credentials (.env)**

   - Rename `.env.template` to `.env`
   - Update the `POSTGRESSQL_PASSWORD` with the password for your `postgres` user account

     ```bash
     # example .env
     POSTGRESSQL_HOST="localhost"
     POSTGRESSQL_DATABASE_NAME="bus_route_management"
     POSTGRESSQL_USER="postgres"
     POSTGRESSQL_PASSWORD="1234"
     ```

4. **Run the Application**

   ```bash
   python3 main.py
   ```
