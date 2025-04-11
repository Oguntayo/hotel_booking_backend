# Hotel Booking Backend

This is the backend API for a hotel booking platform, built using Django and Django REST Framework. The project allows hotel owners to manage their hotels, rooms, and bookings, while guests can book rooms without registering.

## Features

- User authentication with JWT tokens.
- Hotel and Room management for hotel owners.
- Booking management for guests.
- Email notifications for new bookings.

## Tech Stack

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework**: A powerful toolkit for building Web APIs in Django.
- **PostgreSQL** (or any other database you're using).
- **JWT Authentication**: For secure API access.
- **Mailtrap API**: For sending email notifications.

## Requirements

- Python 3.8 or higher
- PostgreSQL (or any other database you're using)
- pip (Python package installer)

## Setup Instructions

Follow these steps to run the project locally:

### 1. Clone the Repository

Clone the repository to your local machine:
```bash
git clone https://github.com/Oguntayo/hotel_booking_backend.git
cd hotel_booking_backend
 Create a Virtual Environment

Create a virtual environment to keep dependencies isolated:

python3 -m venv venv

Activate the virtual environment:

    On macOS/Linux:

source venv/bin/activate

On Windows:

    .\venv\Scripts\activate

3. Install Dependencies

Install the required dependencies using pip:

pip install -r requirements.txt

4. Set Up the Database

Ensure PostgreSQL is installed and set up on your machine, or configure your project to use any other database.

Create the necessary database and run migrations:

python manage.py migrate

5. Configure Environment Variables

Create a .env file by copying the example configuration file:

cp .env.example .env

Then, open the .env file and replace the placeholder values with your actual values:

    DJANGO_SECRET_KEY: Generate a secret key for your Django project.

    DATABASE_URL: Provide your database connection URL (e.g., PostgreSQL).

    MAILTRAP_API_TOKEN: Get your Mailtrap API token from your Mailtrap account.

    MAILTRAP_SENDER_EMAIL: The email address you want to use to send test emails.

Ensure that the .env file is not tracked by Git (it shouldn't be pushed to the repository). It should be listed in .gitignore.
6. Run the Development Server

Start the Django development server:

python manage.py runserver

The API should now be running locally at http://127.0.0.1:8000/.
7. API Endpoints

    POST /api/register/: Register a new user.

    POST /api/login/: Login with email and password to get JWT tokens.

    GET /api/hotels/: List all hotels (authenticated users).

    POST /api/rooms/: Create a new room (authenticated hotel owners).

    GET /api/bookings/: View all bookings (authenticated users).


