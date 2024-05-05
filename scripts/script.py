import requests
import time
import openpyxl
from pymongo import MongoClient
import threading

# MongoDB connection
client = MongoClient(
    "mongodb+srv://dhirajmuppineti486:HlkvwJhB8VkMjL76@applications.eaxfxvs.mongodb.net/"
)
db = client["BAP"]  # Replace 'BAP' with your actual database name

# Lock for database access
lock = threading.Lock()


def check_website_status(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        response_time = end_time - start_time

        status_code = response.status_code
        if status_code == 200:
            if response_time < 1:
                return "Operational", response_time
            else:
                return "Operational (Slow Response)", response_time
        elif status_code >= 400 and status_code < 500:
            return "Partial Outage", response_time
        elif status_code >= 500:
            return "Major Outage", response_time
        else:
            return "Unknown Status", response_time
    except requests.exceptions.RequestException as e:
        return "Error: {}".format(e), None


def process_website(url):
    try:
        # Check website status
        status, response_time = check_website_status(url)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Extract domain name from URL
        domain_name = url.split("//")[1].split("/")[0]

        # Use domain name as collection name
        collection_name = domain_name.replace(".", "_")

        # Lock the database access
        with lock:
            # Check if the MongoDB collection already exists
            if collection_name not in db.list_collection_names():
                # Create the collection if it doesn't exist
                db.create_collection(collection_name)

            # Insert entry into MongoDB collection
            db[collection_name].insert_one(
                {
                    "timestamp": timestamp,
                    "status": status,
                    "responseTime": response_time,
                }
            )

            # Print status and response time
            if response_time is not None:
                print("Status of {}: {}".format(url, status))
                print("Response time: {:.2f} seconds".format(response_time))
            else:
                print("Status of {}: {}".format(url, status))
    except Exception as e:
        print("Error processing {}: {}".format(url, e))


def process_urls():
    # Open the Excel file and load the worksheet
    workbook = openpyxl.load_workbook("websites.xlsx")
    worksheet = workbook.active

    # Iterate over rows in the worksheet to read website URLs
    urls = [
        row[0] for row in worksheet.iter_rows(min_row=2, values_only=True) if row[0]
    ]

    # Start a thread for each URL
    threads = []
    for url in urls:
        thread = threading.Thread(target=process_website, args=(url,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    while True:
        process_urls()
        # Wait for 30 seconds before querying again
        time.sleep(1)
