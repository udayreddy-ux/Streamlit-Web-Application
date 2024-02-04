import streamlit as st
import pymysql
from io import StringIO
import re
from collections import Counter
import pandas as pd
import time


def homePage():
    try:
        st.markdown("<p style='text-align:center; font-size: 38px;'>University of Cincinnati</p>",
                    unsafe_allow_html=True)

        st.write("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.image('rt.png', caption='Go Bearcats!!!!', use_column_width=True)
        st.write("</div>", unsafe_allow_html=True)

        custom_css = """
        <style>
            /* Target the .stButton>button element for button adjustments */
            .stButton>button {
                margin: 1px 1px; /* Adjusts the margin around buttons */
                padding: 0px 0px; /* Adjust padding inside buttons, if needed */
                width: 80px; /* Set maximum width for each button */
                /* Optional: You might want to add this to ensure the text is centered if the button doesn't expand to max-width */
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
        """

        st.markdown(custom_css, unsafe_allow_html=True)
        homeCol, registerCol, loginCol = st.columns(3)
        with homeCol:
            navBarHomeInHome = st.button('Home')
            if navBarHomeInHome:
                st.session_state.current_page = 'home'
                st.session_state.page = 'home'
                st.experimental_rerun()

        with registerCol:
            navBarRegisterInHome = st.button('Register')
            if navBarRegisterInHome:
                st.session_state.current_page = 'register'
                st.session_state.page = 'register'
                st.experimental_rerun()
        with loginCol:
            navBarLogin = st.button('Login')
            if navBarLogin:
                st.session_state.current_page = 'login'
                st.session_state.page = 'login'
                st.experimental_rerun()

    except Exception as e:
        print("In homePage:")
        raise Exception(e)


def loginPage(connection):
    custom_css = """
            <style>
                /* Target the .stButton>button element for button adjustments */
                .stButton>button {
                    margin: 1px 1px; /* Adjusts the margin around buttons */
                    padding: 0px 0px; /* Adjust padding inside buttons, if needed */
                    width: 110px; /* Set maximum width for each button */
                    height: 40px;
                    /* Optional: You might want to add this to ensure the text is centered if the button doesn't expand to max-width */
                    display: block;
                     margin-left: auto;
                     margin-right: auto;
                }
            </style>
            """

    st.markdown(custom_css, unsafe_allow_html=True)
    homeColInLogin, registerColInLogin = st.columns(2)

    with homeColInLogin:
        navBarHomeInLogin = st.button('Home')
        if navBarHomeInLogin:
            st.session_state.current_page = 'home'
            st.session_state.page = 'home'
            st.experimental_rerun()

    with registerColInLogin:
        navBarRegisterInLogin = st.button('Register')
        if navBarRegisterInLogin:
            st.session_state.current_page = 'register'
            st.session_state.page = 'register'
            st.experimental_rerun()

    try:
        print("In loginPage: ")
        print(st.session_state)

        loginPlaceholder = st.empty()
        loginSuccess = 0
        with loginPlaceholder.form("login"):
            st.title('Login')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            login_button = st.form_submit_button("Login")

            if login_button:
                # Perform login logic
                user_data = execute_query(
                    f"SELECT * FROM login_users WHERE username = '{username}' AND password = '{password}'", connection)

                if user_data:
                    loginSuccess = 1
                    # loginPlaceholder.empty()
                    st.session_state.logged_in = True
                    st.session_state['username'] = username
                    st.success("Logged in successfully!")
                    st.experimental_rerun()
                    # Additional logic for handling a successful login (e.g., redirect to another page)
                else:
                    st.error('Invalid username or password. Please try again.')

    except Exception as e:
        print("In loginPage")
        raise Exception(e)


def execute_query(query, connection):
    try:
        # Establish a database connection
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    except pymysql.MySQLError as e:
        print(f"Error connecting to the MySQL Database: {e}")
        return None


def registerPage(connection):
    try:
        custom_css = """
                    <style>
                        /* Target the .stButton>button element for button adjustments */
                        .stButton>button {
                            margin: 1px 1px; /* Adjusts the margin around buttons */
                            padding: 0px 0px; /* Adjust padding inside buttons, if needed */
                            width: 110px; /* Set maximum width for each button */
                            height: 40px;
                            /* Optional: You might want to add this to ensure the text is centered if the button doesn't expand to max-width */
                            display: block;
                             margin-left: auto;
                             margin-right: auto;
                        }
                    </style>
                    """

        st.markdown(custom_css, unsafe_allow_html=True)
        homeCol, registerCol, loginCol = st.columns(3)
        with homeCol:
            navBarHomeInRegister = st.button('Home')
            if navBarHomeInRegister:
                st.session_state.current_page = 'home'
                st.session_state.page = 'home'
                st.experimental_rerun()

        with loginCol:
            navBarLoginInRegister = st.button('Login')
            if navBarLoginInRegister:
                st.session_state.current_page = 'login'
                st.session_state.page = 'login'
                st.experimental_rerun()
        register = 0
        placeholder = st.empty()
        with placeholder.form("register"):
            st.title('Register')
            f_name = st.text_input('First Name')
            l_name = st.text_input('Last Name')
            email = st.text_input('Email')
            userName = st.text_input('User Name')
            password = st.text_input('Password', type='password')
            confirm_password = st.text_input('Confirm Password', type='password')
            registerButton = st.form_submit_button("Register")

            if registerButton:

                existing_user = execute_query(f"SELECT * FROM login_users WHERE username = '{userName}'", connection)
                # Check if any of the required fields are empty
                if not (f_name or l_name or email or userName or password or confirm_password):
                    st.error('All fields are mandatory. Please fill in all required information.')
                    return

                # Check if the passwords match
                elif password != confirm_password:
                    st.error('Passwords do not match. Please enter matching passwords.')
                    return

                # Check if the username already exists
                elif existing_user:
                    st.error('Username already exists. Please choose a different username.')
                    return

                # Insert the new user into the database

                else:
                    sql = "INSERT INTO login_users (username, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)"
                    with connection.cursor() as cursor:
                        cursor.execute(sql, (userName, f_name, l_name, email, password))
                    connection.commit()
                    st.success('Registered successfully!')
                    register = 1
                    st.session_state['current_page'] = 'LoggedIn'
                    st.session_state['f_name'] = f_name
                    st.session_state['l_name'] = l_name
                    st.session_state['email'] = email
                    st.session_state['registered'] = True
                    placeholder.empty()

                    # if st.session_state['current_page'] == 'logged_in':
                    #     successful_login()
        if register == 1:
            successful_register(connection)
    except Exception as e:
        print("In registerPage")
        raise Exception(e)


def file_upload(connection):
    try:
        custom_css = """
                    <style>
                        /* Target the .stButton>button element for button adjustments */
                        .stButton>button {
                            margin: 1px 1px; /* Adjusts the margin around buttons */
                            padding: 0px 0px; /* Adjust padding inside buttons, if needed */
                            width: 110px; /* Set maximum width for each button */
                            height: 40px;
                            /* Optional: You might want to add this to ensure the text is centered if the button doesn't expand to max-width */
                            display: block;
                             margin-left: auto;
                             margin-right: auto;
                        }
                    </style>
                    """

        st.markdown(custom_css, unsafe_allow_html=True)
        homeColInFileUpload, registerColInFileUpload = st.columns(2)

        with homeColInFileUpload:
            navBarHomeInFileUpload = st.button('Home')
            if navBarHomeInFileUpload:
                st.session_state.current_page = 'home'
                st.session_state.page = 'home'
                st.experimental_rerun()

        with registerColInFileUpload:
            navBarRegisterInFileUpload = st.button('Register')
            if navBarRegisterInFileUpload:
                st.session_state.current_page = 'register'
                st.session_state.page = 'register'
                st.session_state.logged_in = False
                st.session_state.registered = False
                st.experimental_rerun()
        st.title("File Upload Page")
        fetchUserDetailsQuery = f"SELECT firstname, lastname, email FROM login_users WHERE username = '{st.session_state.username}'"
        getUserContentQuery = f"""SELECT 
        content.count_info
    FROM
        login_users user_tbl
    LEFT JOIN
        user_data content
    ON
        user_tbl.username=content.username
    WHERE
        user_tbl.username='{st.session_state.username}'
        """
        data = execute_query(fetchUserDetailsQuery, connection)
        contentData = execute_query(getUserContentQuery, connection)
        st.write("First Name: " + data[0]['firstname'])
        st.write("Last Name: " + data[0]['lastname'])
        st.write("Email: " + data[0]['email'])
        if contentData[0]['count_info'] is not None:
            st.write('Previously Uploaded Content: ')
            st.write(contentData[0]['count_info'])
            segments = contentData[0]['count_info'].split()
            remove_chars_pattern = r"[,?'':!]"
            cleaned_segments = [re.sub(remove_chars_pattern, '', segment) for segment in segments]
            cnt = Counter()
            for word in cleaned_segments:
                cnt[word] += 1
            data = list(cnt.items())
            df = pd.DataFrame(data, columns=['Word', 'Count'])
            st.markdown("Previously Uploaded Count: ")
            st.dataframe(df)
            st.bar_chart(df, x="Word", y="Count")

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

            # To read file as string:
            string_data = stringio.read()
            deleteExistingContent = f"""
                DELETE FROM user_data WHERE username='{st.session_state.username}'
            """
            insertUserContent = f"""
                INSERT INTO user_data (username, count_info) VALUES (%s, %s)
            """

            # st.write(string_data)
            st.markdown("Newly Uploaded Content: ")
            st.write(string_data)
            segments = string_data.split()
            remove_chars_pattern = r"[,?'':!]"
            cleaned_segments = [re.sub(remove_chars_pattern, '', segment) for segment in segments]
            cnt = Counter()
            for word in cleaned_segments:
                cnt[word] += 1
            data = list(cnt.items())
            df = pd.DataFrame(data, columns=['Word', 'Count'])

            # Display the DataFrame

            st.markdown("Newly Uploaded Content: ")
            st.dataframe(df)
            st.bar_chart(df, x="Word", y="Count")
            with connection.cursor() as cursor:
                cursor.execute(deleteExistingContent)
            connection.commit()
            with connection.cursor() as cursor:
                cursor.execute(insertUserContent, (st.session_state.username, uploaded_file.getvalue()))
            connection.commit()
        if st.button('Log out'):
            st.session_state.logged_in = False
            st.session_state.registered = False
            st.experimental_rerun()

    except Exception as e:
        raise Exception(e)


def successful_register(connection):
    st.title("Successfully Registered.")
    welcomeMessage = 'Welcome {}'.format(st.session_state.f_name)
    st.title(welcomeMessage)
    st.write("First Name: " + st.session_state.f_name)
    st.write("Last Name: " + st.session_state.l_name)
    st.write("Email: " + st.session_state.email)
    st.session_state['current_page'] = 'register'
    login_button_sr = st.button("Go to Login")
    # st.write(st.session_state)
    if login_button_sr:
        st.write(st.session_state)
        st.session_state.registered = True
        st.session_state.page = 'login'
        st.session_state.current_page = 'login'
        print("SESSSSSSSSIIIIIIIIIIOOOOONNNN::::::", st.session_state)
        st.experimental_rerun()


def databaseConnection():
    try:
        host = "*****************"  # e.g., "localhost" or an IP address
        user = "*****"  # the username, e.g., "root"
        password = "********"  # the password for the database
        db = "*********"  # the name of the database you want to connect to
        connection = pymysql.connect(host=host,
                                     user=user,
                                     password=password,
                                     database=db,
                                     cursorclass=pymysql.cursors.DictCursor)
        print("Successfully connected to the database.")
        return connection
    except Exception as e:
        print("In Database connection: ")
        raise Exception(e)


def buildStreamlit():
    try:
        connection = databaseConnection()
        if 'page' not in st.session_state:
            st.session_state.page = 'home'
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 'home'
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
        if 'registered' not in st.session_state:
            st.session_state['registered'] = False

        # if st.session_state.internalChange is False and
        # sideBarState = st.sidebar.selectbox('Choose a page:', ['home', 'login', 'register'])

        if st.session_state.page == 'home':
            st.session_state['current_page'] = 'home'
            homePage()
        elif st.session_state.page == 'login':
            st.session_state['current_page'] = 'login'
            # Check if logged in before showing the file upload page
            if not st.session_state.logged_in:
                loginPage(connection)
            else:
                file_upload(connection)
        elif st.session_state.page == 'register':
            st.session_state['current_page'] = 'register'
            if not st.session_state.registered:
                registerPage(connection)
            else:
                st.session_state['current_page'] = 'login'
                st.session_state['page'] = 'login'
                loginPage(connection)



        print("In buildStreamlit: ")
        print(st.session_state)
        print("-------------------------------")
    except Exception as e:
        raise e


if __name__ == '__main__':
    buildStreamlit()
