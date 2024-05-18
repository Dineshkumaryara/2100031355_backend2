CREATE DATABASE safertek2;

USE safertek2;

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    DateOfBirth DATE
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Price DECIMAL(10, 2)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);


INSERT INTO Customers VALUES (1, 'John', 'Doe', 'john.doe@example.com', '1985-01-15');
INSERT INTO Customers VALUES (2, 'Jane', 'Smith', 'jane.smith@example.com', '1990-06-20');

INSERT INTO Products VALUES (1, 'Laptop', 1000);
INSERT INTO Products VALUES (2, 'Smartphone', 600);
INSERT INTO Products VALUES (3, 'Headphones', 100);

INSERT INTO Orders VALUES (1, 1, '2023-01-10');
INSERT INTO Orders VALUES (2, 2, '2023-01-12');

INSERT INTO OrderItems VALUES (1, 1, 1, 1);
INSERT INTO OrderItems VALUES (2, 1, 3, 2);
INSERT INTO OrderItems VALUES (3, 2, 2, 1);
INSERT INTO OrderItems VALUES (4, 2, 3, 1);
