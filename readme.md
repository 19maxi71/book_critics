# Book Critics Blog (OC-project-LITRevu)

## Project Description

This is a Django-based blog application where users can ask for book critiques, read critiques, and publish their own critiques. Users can follow other users to see their posts and critiques in their feed.

## Features

- **User Authentication**: Users can register, log in, and log out.
- **User Profiles**: Users can follow and unfollow other users.
- **Posts and Critiques**: Users can create posts asking for critiques and publish critiques in response to posts.
- **Feed**: Users can see a feed of posts and critiques from users they follow, as well as their own posts and critiques.
- **CRUD Operations**: Users can create, read, update, and delete their own posts and critiques.

## Project Structure

```
book_critics/
├── .DS_Store
├── .flake8
├── .gitignore
├── blog/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── static/
│   ├── templates/
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── book_critics/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── db.sqlite3
├── manage.py
├── media/
├── requirements.txt
└── venv/
    ├── bin/
    ├── include/
    ├── lib/
    └── pyvenv.cfg
```

## Setup Instructions

### Prerequisites

- Python 3.12
- Django 5.1.1
- Virtualenv

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/book_critics.git
    cd book_critics
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations**:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

7. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

### User Registration and Login

- Users can register by navigating to `/register/`.
- Users can log in by navigating to `/login/`.

### Creating Posts and Critiques

- After logging in, users can create posts asking for critiques.
- Users can also publish critiques in response to posts.

### Following Users

- Users can follow other users to see their posts and critiques in their feed.
- Users can unfollow users from their profile page.

### Viewing the Feed

- The feed displays posts and critiques from users that the logged-in user follows, as well as their own posts and critiques.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```sh
    git commit -m 'Add some feature'
    ```
5. **Push to the branch**:
    ```sh
    git push origin feature/your-feature-name
    ```
6. **Open a pull request**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- Jinja2 Documentation: [https://jinja.palletsprojects.com/en/stable/] (https://jinja.palletsprojects.com/en/stable/)
