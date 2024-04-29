import requests
import time
import openpyxl
from pymongo import MongoClient

# MongoDB connection
client = MongoClient(
    "mongodb+srv://dhirajmuppineti486:HlkvwJhB8VkMjL76@applications.eaxfxvs.mongodb.net/"
)
db = client["BAP"]  # Replace 'BAP' with your actual database name


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


if __name__ == "__main__":
    while True:
        # Open the Excel file and load the worksheet
        workbook = openpyxl.load_workbook("websites.xlsx")
        worksheet = workbook.active

        # Iterate over rows in the worksheet to read website URLs
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            url = row[0]  # Get the URL from the first column of the row
            if url:
                # Extract domain name from URL
                domain_name = url.split("//")[1].split("/")[0]

                # Check if the MongoDB collection already exists
                collection_name = domain_name.replace(
                    ".", "_"
                )  # Use domain name as collection name
                if collection_name not in db.list_collection_names():
                    # Create the collection if it doesn't exist
                    db.create_collection(collection_name)

                # Check website status
                status, response_time = check_website_status(url)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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

        # Wait for 30 seconds before querying again
        time.sleep(30)
