**InShort**

#Overview
This project is a simple API inspired by the InShorts platform. It allows users to register, log in, and read news summaries, called "shorts." Admin users can add new shorts, while regular users can view and filter them. The API is built with Flask, using JWT for secure authentication and role-based access control.

#Features
1.User Registration and Authentication: Users can sign up and log in securely with JWT-based authentication.
2.Role Management: There are two types of users—regular users and admins. Admins have special permissions, like adding new shorts.
3/Shorts Management: Admin users can create news summaries (shorts), which include details like category, title, author, publish date, and more. All users can view and filter these shorts.


#Prerequisites
Before you begin, make sure you have the following installed:
1. Python 3.7 or higher
2. pip (Python package manager)
3. SQLite (default database used in this project)

   
#Setup Instructions
1. Clone the Repository
  First, you'll need to clone the project repository to your local machine:
  git clone https://github.com/sinha-diksha/workIndiaAPI.git
  cd workIndiaAPI

3. Make sure python3 is installed in your local machine
   
4. Install the Required Packages
    Install the necessary Python packages:
    pip install -r requirements.txt
   
5. Set Up Environment Variables
    Create a .env file in the project directory to store environment variables. For example:
    JWT_SECRET_KEY=<your_jwt_secret_key_here>
    Replace your_jwt_secret_key_here with a strong secret key of your choice. This key is used for JWT token generation.

6. Initialize the Database
    You'll need to set up the database and apply the necessary migrations:
    flask db init
    flask db migrate
    flask db upgrade
This will create the SQLite database and set up the required tables.

7. Run the Application
    Now, you can start the Flask server:
    python main.py
    The server will start running on http://127.0.0.1:5000/.

8. Run Tests
    In a separate terminal window, while the server is still running, you can run the test script:
    python test.py
    This script will execute a series of tests to check the functionality of the API endpoints. Ensure main.py is running when you do this.

#Project Structure
1. main.py: The main application file that contains the API endpoints and logic.
2. test.py: A script with basic tests to validate the API's functionality.
3. requirements.txt: Lists all the Python packages required to run this project.
4. migrations/: Contains the migration files for setting up the database schema.
5. inshorts.db: The SQLite database file that gets created after running the application.
   
#Important Notes
1. Run the Server First: Make sure that the Flask server (main.py) is running before you execute the test script (test.py).
2. JWT Authentication: The API uses JWT for secure authentication. Be sure that your environment variables, particularly the JWT secret key, are set correctly.
3. Also, once you have used 'db.create_all()' command, make sure to remove or comment it so that database is not overwritten everytime. When you start the flask application, run it only for the first time.
