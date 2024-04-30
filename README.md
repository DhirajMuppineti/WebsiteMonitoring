# Website Monitoring Application

This is a Flask-based web application for monitoring the status and response times of multiple websites.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python (>= 3.6)
- MongoDB
- Flask
- pymongo
- numpy
- requests
- openpyxl

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DhirajMuppineti/WebsiteMonitoring.git
    ```

2. Navigate to the project directory:

    ```bash
    cd website-monitoring
    ```

3. Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Set up MongoDB:

    - Create a MongoDB Atlas cluster or set up a local MongoDB instance.
    - Replace the MongoDB connection string in `app.py` with your own connection string.

## Running the Application

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open a web browser and go to `http://localhost:5000` to access the application.

## Running the Script

1. Run the script to continuously update the database with website status and response times:

    ```bash
    python script.py
    ```

## Usage

- The home page (`/`) displays a list of websites and their latest statuses.
- Clicking on a website name will take you to the dashboard for that website, displaying detailed information including response times.
- The application continuously updates the database with the status and response times of the configured websites.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
