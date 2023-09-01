import sqlite3
import random
import string
from faker import Faker

# Create a SQLite database
conn = sqlite3.connect('random_people.db')
cursor = conn.cursor()

################ TO CREATE THE DATABASE #################

# Create a table to store the data
cursor.execute('''CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    date_of_birth TEXT,
                    age INTEGER,
                    sex TEXT,
                    email TEXT
                )''')

# Initialize the Faker library
fake = Faker()

# Generate and insert random people's data
for i in range(10):
    # Generate random data
    username = fake.user_name()
    password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
    age = fake.random_int(min=18, max=80)
    sex = random.choice(['Male', 'Female'])
    email = fake.email()

    # Insert data into the database
    cursor.execute('''INSERT INTO people (username, password, date_of_birth, age, sex, email) 
                      VALUES (?, ?, ?, ?, ?, ?)''', (username, password, date_of_birth, age, sex, email))
    
print("Random database of 10 people generated successfully.")

############### TO VIEW THE DATABASE ###################
# Execute an SQL query to fetch data from a table
cursor.execute('SELECT * FROM people')

# Fetch and display the data
data = cursor.fetchall()
for row in data:
    print(row)

# Commit changes and close the database connection
conn.commit()
conn.close()