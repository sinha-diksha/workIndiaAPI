InShorts-Like News Platform API
Overview
This project is a simple API inspired by the InShorts platform. It allows users to register, log in, and read news summaries, called "shorts." Admin users can add new shorts, while regular users can view and filter them. The API is built with Flask, using JWT for secure authentication and role-based access control.

Features
User Registration and Authentication: Users can sign up and log in securely with JWT-based authentication.
Role Management: There are two types of users—regular users and admins. Admins have special permissions, like adding new shorts.
Shorts Management: Admin users can create news summaries (shorts), which include details like category, title, author, publish date, and more. All users can view and filter these shorts.
Prerequisites
Before you begin, make sure you have the following installed:

Python 3.7 or higher
pip (Python package manager)
SQLite (default database used in this project)
Setup Instructions
1. Clone the Repository
First, you'll need to clone the project repository to your local machine:

bash
Copy code
git clone https://github.com/sinha-diksha/workIndiaAPI.git
cd workIndiaAPI
2. Create and Activate a Virtual Environment
To keep your dependencies organized, it's best to use a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install the Required Packages
With your virtual environment activated, install the necessary Python packages:

bash
Copy code
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the project directory to store environment variables. For example:

bash
Copy code
JWT_SECRET_KEY=your_jwt_secret_key_here
Replace your_jwt_secret_key_here with a strong secret key of your choice. This key is used for JWT token generation.

5. Initialize the Database
You'll need to set up the database and apply the necessary migrations:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
This will create the SQLite database and set up the required tables.

6. Run the Application
Now, you can start the Flask server:

bash
Copy code
python main.py
The server will start running on http://127.0.0.1:5000/.

7. Run Tests
In a separate terminal window, while the server is still running, you can run the test script:

bash
Copy code
python test.py
This script will execute a series of tests to check the functionality of the API endpoints. Ensure main.py is running when you do this.

Project Structure
main.py: The main application file that contains the API endpoints and logic.
test.py: A script with basic tests to validate the API's functionality.
requirements.txt: Lists all the Python packages required to run this project.
migrations/: Contains the migration files for setting up the database schema.
inshorts.db: The SQLite database file that gets created after running the application.
Important Notes
Run the Server First: Make sure that the Flask server (main.py) is running before you execute the test script (test.py).
JWT Authentication: The API uses JWT for secure authentication. Be sure that your environment variables, particularly the JWT secret key, are set correctly.
