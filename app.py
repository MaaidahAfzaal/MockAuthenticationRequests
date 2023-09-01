from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# This route is called at the start of the application and it renders the html page
@app.route('/')
def hello():
    return render_template('index.html')


# This route is called when the user clicks the authenticate button, it returns the result of 
# the authentication
@app.route('/get_authentication', methods=['POST'])
def authenticate_data():
    # Get the data from front-end as JSON and get username and password entered by the user
    request_data = request.get_json()
    user_name = request_data.get('user_name')
    password = request_data.get('password')

    # Connect to the SQLite database
    conn = sqlite3.connect('random_people.db')
    cursor = conn.cursor()

    # Execute the SQL query for the usernames
    cursor.execute('SELECT * FROM people WHERE username = ?', (user_name,))

    # Fetch the result
    user_data = cursor.fetchone()

    # Close the database connection
    conn.close()

    # If the username does not exist in the database return error to front-end
    if user_data is None:
        return {'Authentication': 'User not found. Please register.'}
    # If the username does exist, verify password
    else:
        # Get the correct password from the database corresponding to the user
        stored_password = user_data[2]

        # If the password matches the one entered by the user, send the data of the user to front-end
        if password == stored_password:
            return {'Authentication' : 'Login successful.',
                    'Data' : { 'User Name' : user_data[1], 
                              'Date of Birth' : user_data[3], 
                              'Age' : user_data[4], 
                              'Sex' : user_data[5], 
                              'Email' : user_data[6]}
                    }
        # If password does not match, send error to front-end
        else:
            return {'Authentication' : 'Incorrect password. Please try again.'}
    