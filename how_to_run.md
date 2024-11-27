To run the **RBAC** project locally using SQLite, follow these steps:

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/SheikhUmaid/RBAC.git
```

### 2. Navigate to Project Directory

Go into the project directory:

```bash
cd RBAC
```

### 3. Set Up a Virtual Environment

It's a good practice to set up a virtual environment to manage dependencies.

* **For Windows:**

```bash
python -m venv venv
```

* **For macOS/Linux:**

```bash
python3 -m venv venv
```

Activate the virtual environment:

* **For Windows:**

```bash
venv\Scripts\activate
```

* **For macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

Install the required dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Set Up SQLite Database

The project is configured to use SQLite by default, so you don’t need to change any database settings.

Run the following command to create the SQLite database and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional)

If you want to access the Django admin, you’ll need to create a superuser account:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter your username, email, and password.

### 7. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

This will start the server on `http://127.0.0.1:8000/` by default.

### 8. Access the Application

* Open a browser and go to `http://127.0.0.1:8000/` to access the endpoints.
* For admin access, go to `http://127.0.0.1:8000/admin/` and log in using the superuser credentials you created.

### 9. Testing the API

* You can test the API using tools like [Postman](https://www.postman.com/) or `curl` to interact with the endpoints like `/auth/register/`, `/auth/login/`, `/file/`, etc.
* For convenience Posman Collections are given in [testing](./testing/) directory
* You can test the API endpoints using Postman and all endpoints are provided in the [readme.md](https://chatgpt.com/c/readme.md) file with detailed descriptions of request methods, parameters, and expected responses.

---

### Additional Notes:

* **Static Files** : For local development, the static files (like CSS, JS, images) are handled by Django's `runserver` command. However, for production, you will need to configure static files handling.
* **Environment Variables** : Make sure that you don't expose sensitive information like secret keys in version control. You may want to configure environment variables for production settings.
