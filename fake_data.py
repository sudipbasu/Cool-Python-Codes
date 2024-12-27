import pymysql
from faker import Faker

# MySQL connection details
db_config = {
    "host": "localhost",     # Change to your MySQL host
    "user": "root",          # Change to your MySQL username
    "password": "",  # Change to your MySQL password
}

# Initialize Faker
fake = Faker()

# Establish a connection to MySQL
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Create the database if it doesn't exist
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")
    print("Database 'test_db' created or already exists.")
except pymysql.MySQLError as e:
    print(f"Error creating database: {e}")

# Use the created database
cursor.execute("USE test_db")

# Create the users table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(50),
    company VARCHAR(255),
    job VARCHAR(255),
    ssn VARCHAR(50),
    credit_card_number VARCHAR(50),
    date_of_birth DATE,
    website VARCHAR(255)
);
"""
try:
    cursor.execute(create_table_query)
    print("Table 'users' created or already exists.")
except pymysql.MySQLError as e:
    print(f"Error creating table: {e}")

# SQL query to insert data
insert_query = """
    INSERT INTO users (name, address, email, phone_number, company, job, ssn, credit_card_number, date_of_birth, website)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Generate and insert 1000 fake data records
for _ in range(1000):
    name = fake.name()
    address = fake.address().replace("\n", ", ")  # Replace newlines in address
    email = fake.email()
    phone_number = fake.phone_number()
    company = fake.company()
    job = fake.job()
    ssn = fake.ssn()
    credit_card_number = fake.credit_card_number()
    date_of_birth = fake.date_of_birth().strftime('%Y-%m-%d')
    website = fake.url()

    # Data to insert
    data = (name, address, email, phone_number, company, job, ssn, credit_card_number, date_of_birth, website)

    # Execute the insert query
    cursor.execute(insert_query, data)

# Commit the changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print("1000 fake records inserted successfully!")
