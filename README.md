# Project Setup Instructions

Follow these steps to set up and run the project.

## 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository_url>
cd ZastiSL_LCA_Capstone_Project/backend
```


## 2. Set Up the Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- For Linux/MacOS:

```bash
source venv/bin/activate
```

- For Windows:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

Install all required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
## 4. Create the .env File

### Inside the backend directory, create a .env file and fill in the following values:

```bash
MONGODB_URI=""
MONGODB_NAME=""
OPENAI_API_KEY=""
```

## 5. Run the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

## 6. Access the Frontend

Navigate to the frontend directory and open `index.html` in your browser:

```bash
cd ../frontend
open index.html  # For MacOS
# OR
xdg-open index.html  # For Linux
# OR
start index.html  # For Windows
```

Now, you can use the application!
