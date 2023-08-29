-- Create Roles
CREATE ROLE rider;
CREATE ROLE driver;
CREATE ROLE admin;
-- Assign Table Ownership
ALTER TABLE Routes OWNER TO admin;
-- Rider Permissions
GRANT SELECT ON TABLE Routes TO rider;
-- Driver Permissions
GRANT SELECT,
    INSERT ON TABLE Routes TO driver;
-- Admin Permissions
GRANT ALL PRIVILEGES ON TABLE Routes TO admin;
-- Create Roles Table
CREATE TABLE Roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL
);
-- Insert Roles
INSERT INTO Roles (role_name)
VALUES ('Driver'),
    ('Rider'),
    ('Admin');
-- Create Users Table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT REFERENCES Roles(role_id)
);
-- Insert Users
INSERT INTO Users (username, password, role_id)
VALUES ('driver1', '1234', 1),
    ('rider1', '1234', 2),
    ('admin1', '1234', 3);
-- Associate Users with Roles
ALTER USER driver WITH ROLE driver;
ALTER USER rider WITH ROLE rider;
ALTER USER admin1 WITH ROLE admin;
-- Create Routes Table
CREATE TABLE Routes (
    route_id SERIAL PRIMARY KEY,
    route_name VARCHAR(255) NOT NULL,
    start_point VARCHAR(255) NOT NULL,
    end_point VARCHAR(255) NOT NULL,
    distance FLOAT
);
-- Insert Routes
INSERT INTO Routes (route_name, start_point, end_point, distance)
VALUES (
        'Route A',
        'Miami, FL',
        'Jacksonville, FL',
        345.8
    ),
    ('Route B', 'Boston, MA', 'New York, NY', 215.5),
    ('Route C', 'Chicago, IL', 'Columbus, OH', 358.6);
-- Create DriverRoutes Table
CREATE TABLE DriverRoutes (
    driver_id INT REFERENCES Users(user_id),
    route_id INT REFERENCES Routes(route_id),
    PRIMARY KEY (driver_id, route_id)
);
-- Insert DriverRoutes
INSERT INTO DriverRoutes (driver_id, route_id)
VALUES (1, 1),
    (1, 2);
-- Create RiderRoutes Table
CREATE TABLE RiderRoutes (
    rider_id INT REFERENCES Users(user_id),
    route_id INT REFERENCES Routes(route_id),
    PRIMARY KEY (rider_id, route_id)
);
-- Insert RiderRoutes
INSERT INTO RiderRoutes (rider_id, route_id)
VALUES (2, 1),
    (2, 3);
