# VerdeSpace Backend

    VerdeSpace is a backend platform designed with Django to manage plant data, comments, wishlists, and other
    functionalities. It features integration with a Telegram bot for notifications and provides comprehensive API
    documentation through Swagger and ReDoc.

## Introduction

    VerdeSpace empowers plant enthusiasts and businesses with a scalable and efficient backend solution for managing
    plant-related data. Whether you're tracking plant information, user comments, or wishlists, this system provides the
    functionality you need with ease.

## Features

    Core Features
    Plants Management: Full CRUD operations for plant data.

## Comment System: Add, reply, and manage comments with support for media attachments.

## Wishlists: Track favorite plants with validation to prevent duplicate entries.

## Custom Features

    Image Upload: Attach multiple images to plants.

## Filters: Filter plants by attributes such as size, water needs, and light requirements.

## Integrations

    Telegram Notifications: Automatic updates when new plants are added.

    AWS S3: Store images securely in the cloud.

## API Documentation

    Swagger UI: Interactive API available at /swagger/.

    ReDoc: Clean and detailed API documentation at /redoc/.

## Authentication

    JWT Support: Secure token-based authentication system.

## Quick Start

    Follow these steps to quickly set up and run the backend locally.

    1. Clone the Repository:
    ```bash
    git clone https://github.com/jyjuk/py-verdespace-backend.git
    cd py_verdespace_backend
    ```

    2. Set Up the Environment
    Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/MacOS
    venv\Scripts\activate     # For Windows
    ```

    Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    3. Configure Environment Variables
    Create a .env file in the root directory and add:

    ```bash
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    AWS_ACCESS_KEY_ID=your_aws_access_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret_key
    AWS_STORAGE_BUCKET_NAME=your_bucket_name
    AWS_S3_REGION_NAME=your_aws_region
    CORS_ALLOWED_ORIGINS=http://127.0.0.1,http://localhost
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    ```

    4. Prepare the Database
    Apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

    (Optional) Import fixtures:

    ```bash
    python manage.py loaddata plantsdata_cleaned.json
    ```

    5. Create Superuser
    Set up an admin account:

    ```bash
    python manage.py createsuperuser
    ```

    6. Start the Development Server
    Run the project locally:

    ```bash
    python manage.py runserver
    ```

    Visit http://127.0.0.1:8000/swagger/ to interact with the API.

## Telegram Bot Integration

    The Telegram bot sends notifications when new plants are added.

    Obtain a Telegram bot token and chat ID.

    Add them to your .env file:

    ```bash
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    ```

    Ensure the bot is active and has access to the specified chat.

## Deployment

    To deploy this project in a production environment:

    Server: Use AWS EC2, Heroku, or any other server to host the application.

    Media Storage: Configure AWS S3 for storing media files.

    Database: Switch to PostgreSQL or AWS RDS for better scalability.

    Environment Variables: Update .env settings for the production environment:

    ```bash
    DEBUG=False
    ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
    ```

    Ensure everything works as expected with the test suite:

    Run all tests:

    ```bash
    coverage run --source='verdespace,users' manage.py test
    ```

    Verify outputs, for example:

    Found 28 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ........
    Installed 100 object(s) from 1 fixture(s).
    ..............
     ----------------------------------------------------------------------
    Ran 28 tests in 6.169s

    OK
    Destroying test database for alias 'default'...
    Generate an HTML coverage report:

    ```bash
    coverage html
    ```
    Open the report in your browser:

    ```bash
    start htmlcov/index.html  # Windows
    open htmlcov/index.html   # MacOS/Linux
    ```

    Coverage Report
    An example of the test coverage results can be added here to showcase the reliability of the project. For instance:

    Coverage: 85% overall

    Detailed Analysis:

    users: 90% covered

    verdespace: 80% covered

    You can explore more detailed results in the generated HTML report (htmlcov/index.html).
    Apply pending migrations:

    ```bash
    python manage.py migrate
    ```

## AWS S3 Configuration:

    Verify AWS credentials in .env.

## Telegram Bot:

    Ensure the bot token and chat ID are valid.

## License

    This project is licensed under the MIT License. See the LICENSE file for more details.