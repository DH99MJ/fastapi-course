
# **Backend Clone of Social Media App Using FastAPI**

This project is a backend API for a social media application, built using **FastAPI**. It consists of 4 main routes:

## **1. Post Route**
This route handles the following functionalities:
- Creating a new post
- Deleting an existing post
- Updating a post
- Checking a post's details

## **2. Users Route**
This route manages user-related operations:
- Creating a new user
- Searching for a user by ID

## **3. Auth Route**
This route is responsible for user authentication:
- User login system

## **4. Vote Route**
This route manages the voting system (likes):
- Handles upvotes or retraction of votes
- Note: There is no logic implemented for downvotes

---

## **How to Run Locally**

### Step 1: Clone the repository
Use the following command to clone the repository:

\`\`\`bash
git clone https://github.com/DH99MJ/fastapi-course.git
\`\`\`

### Step 2: Navigate to the project directory
\`\`\`bash
cd fastapi-course
\`\`\`

### Step 3: Install FastAPI
Install FastAPI along with all necessary dependencies:

\`\`\`bash
pip install fastapi[all]
\`\`\`

### Step 4: Run the FastAPI server
Once you're in the project directory, run the following command to start the FastAPI server:

\`\`\`bash
uvicorn main:app --reload
\`\`\`

### Step 5: Access the API documentation
After running the API, you can access the interactive documentation using the following link:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## **Database Setup**
To run this API, you'll need a PostgreSQL database. Follow these steps to configure it:

1. Create a PostgreSQL database.
2. In the root directory of your project, create a `.env` file with the following details:

\`\`\`bash
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password_here
DATABASE_NAME=your_database_name_here
DATABASE_USERNAME=your_username_here
SECRET_KEY=09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

---

