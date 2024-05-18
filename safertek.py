import mysql.connector


def given_query(query, parameter=None):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="zaq1mlp0",
        database='safertek2'
    )
    cursor = connection.cursor()
    cursor.execute(query, parameter or ())
    results = cursor.fetchall()
    connection.close()
    return results


# query for list of all customers
def listOfCustomers():
    query = "select * from Customers"
    return given_query(query)


# orders placed in January 2023
def findOrdersInJanuary():
    query = """
    select * from Orders
    where OrderDate BETWEEN '2023-01-01' AND '2023-01-31'
    """
    return given_query(query)


# details of each order
def orderDetails():
    query = """
    select Orders.OrderID, Customers.FirstName, Customers.LastName, Customers.Email, Orders.OrderDate,
    GROUP_CONCAT(Products.ProductName SEPARATOR ', ') AS ProductsOrdered
    from Orders
    JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    GROUP BY Orders.OrderID, Customers.FirstName, Customers.LastName, Customers.Email, Orders.OrderDate
    """
    return given_query(query)


# list the products purchased in a specific order
def productsOfOrder(orderId):
    query = """
    select Products.ProductName, OrderItems.Quantity 
    from OrderItems
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    where OrderItems.OrderID = %s
    """
    return given_query(query, (orderId,))


# total amount spent by each customer
def totalSpent():
    query = """
    select Customers.CustomerID, Customers.FirstName, Customers.LastName, 
    SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
    from Customers
    JOIN Orders ON Customers.CustomerID = Orders.CustomerID
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    GROUP BY Customers.CustomerID, Customers.FirstName, Customers.LastName
    """
    return given_query(query)


# To find popular product
def popularProduct():
    query = """
    select Products.ProductID, Products.ProductName, 
    SUM(OrderItems.Quantity) AS TotalQuantityOrdered
    from OrderItems
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    GROUP BY Products.ProductID, Products.ProductName
    ORDER BY TotalQuantityOrdered DESC
    LIMIT 1
    """
    return given_query(query)


# total number of orders and the total sales amount for each month in 2023
def salesIn2023():
    query = """
    select DATE_FORMAT(OrderDate, '%Y-%m') AS Month, 
    COUNT(DISTINCT Orders.OrderID) AS TotalOrders, 
    SUM(Products.Price * OrderItems.Quantity) AS TotalSalesAmount
    from Orders
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    where YEAR(OrderDate) = 2023
    GROUP BY DATE_FORMAT(OrderDate, '%Y-%m')
    """
    return given_query(query)


# customers who have spent more than a specific amount
def customersSpendingMoreThan(amount):
    query = """
    select Customers.CustomerID, Customers.FirstName, Customers.LastName, 
    SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
    from Customers
    JOIN Orders ON Customers.CustomerID = Orders.CustomerID
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    GROUP BY Customers.CustomerID, Customers.FirstName, Customers.LastName
    HAVING TotalSpent > %s
    """
    return given_query(query, (amount,))


def main():
    while True:
        print("Select the task you want to perform:")
        print("1. List all customers")
        print("2. Find all orders placed in January 2023")
        print("3. Get the details of each order, including the customer name, email, and products ordered")
        print("4. List the products purchased in a specific order")
        print("5. Calculate the total amount spent by each customer")
        print("6. Find the most popular product (the one that has been ordered the most)")
        print("7. Get the total number of orders and the total sales amount for each month in 2023")
        print("8. Find customers who have spent more than a specific amount")
        print("9. Exit")

        choice = int(input("Enter the number of the task: "))

        if choice == 1:
            results = listOfCustomers()
            if results:
                for row in results:
                    print(f"Customer ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}, Date of Birth: {row[4]}")
            else:
                print("No customers found.")
        elif choice == 2:
            results = findOrdersInJanuary()
            if results:
                for row in results:
                    print(f"Order ID: {row[0]}, Customer ID: {row[1]}, Order Date: {row[2]}")
            else:
                print("No orders found in January 2023.")
        elif choice == 3:
            results = orderDetails()
            if results:
                for row in results:
                    print(
                        f"Order ID: {row[0]}, Customer: {row[1]} {row[2]}, Email: {row[3]}, Order Date: {row[4]}, Products Ordered: {row[5]}")
            else:
                print("No order details found.")
        elif choice == 4:
            order_id = int(input("Enter the OrderID: "))
            results = productsOfOrder(order_id)
            if results:
                print(f"Products in Order {order_id}:")
                for row in results:
                    print(f"Product: {row[0]}, Quantity: {row[1]}")
            else:
                print(f"No products found for OrderID {order_id}.")
        elif choice == 5:
            results = totalSpent()
            if results:
                for row in results:
                    print(f"Customer ID: {row[0]}, Name: {row[1]} {row[2]}, Total Spent: {row[3]}")
            else:
                print("No spending data found.")
        elif choice == 6:
            results = popularProduct()
            if results:
                row = results[0]
                print(f"Most Popular Product: {row[1]} (Product ID: {row[0]}, Total Quantity Ordered: {row[2]})")
            else:
                print("No popular product found.")
        elif choice == 7:
            results = salesIn2023()
            if results:
                for row in results:
                    print(f"Month: {row[0]}, Total Orders: {row[1]}, Total Sales Amount: {row[2]}")
            else:
                print("No sales data found for 2023.")
        elif choice == 8:
            amount = float(input("Enter the amount: "))
            results = customersSpendingMoreThan(amount)
            if results:
                print(f"Customers who spent more than {amount}:")
                for row in results:
                    print(f"Customer ID: {row[0]}, Name: {row[1]} {row[2]}, Total Spent: {row[3]}")
            else:
                print(f"No customers found who spent more than {amount}.")
        elif choice == 9:
            print("Exiting...")
            break
        else:
            print("Invalid choice")

        # Ask if the user wants to continue
        continue_choice = input("Do you want to perform another task? (yes/no): ").strip().lower()
        if continue_choice != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
