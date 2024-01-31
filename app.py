import streamlit as st
import pymysql

host = "assign-cloud.cda42qkoa0rd.us-east-2.rds.amazonaws.com"          # e.g., "localhost" or an IP address
user = "admin"      # the username, e.g., "root"
password = "Uday1989!"  # the password for the database
db = "devo"   # the name of the database you want to connect to
connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=db,
                                 cursorclass=pymysql.cursors.DictCursor)
print("Successfully connected to the database.")

def fetch_data(query):
    try:
        # Establish a database connection
        connection = pymysql.connect(host=host, user=user, password=password, database=db, cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    except pymysql.MySQLError as e:
        print(f"Error connecting to the MySQL Database: {e}")
        return None

    finally:
        if connection:
            connection.close()

# Create a function for each page
def show_home():
    st.title('Home Page')
    createSql = """
    CREATE TABLE login_users (
    username VARCHAR(255) PRIMARY KEY,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
    );

    """

    # Add other home page elements here

def show_login():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        # Perform login logic
        st.success('Logged in successfully!')

def show_register():
    st.title('Register')
    f_name = st.text_input('First Name')
    l_name = st.text_input('Last Name')
    email = st.text_input('Email')
    userName = st.text_input('User Name')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    # if uname exists in db then user already exists

    if st.button('Register'):
        # Perform registration logic
        sql = "INSERT INTO login_users (username, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, (userName, f_name, l_name, email, password))
        connection.commit()
        st.success('Registered successfully!')
        st.write(fetch_data("select * from login_users"))



# Use a selectbox for navigation
page = st.sidebar.selectbox('Choose a page:', ['Home', 'Login', 'Register'])

# Display the selected page
if page == 'Home':
    show_home()
elif page == 'Login':
    show_login()
elif page == 'Register':
    show_register()