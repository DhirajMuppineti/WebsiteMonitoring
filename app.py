from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import numpy as np
from collections import Counter
from statistics import median

app = Flask(__name__)

# MongoDB connection
client = MongoClient(
    "mongodb+srv://dhirajmuppineti486:HlkvwJhB8VkMjL76@applications.eaxfxvs.mongodb.net/"
)
db = client["BAP"]  # Replace 'BAP' with your actual database name


@app.route("/")
def index():
    # Fetch list of websites and their latest statuses
    website_statuses = []
    collections = db.list_collection_names()
    # print(collections)
    for collection_name in collections:
        # Exclude internal collections
        if not collection_name.startswith("system."):
            last_entry = db[collection_name].find_one({}, sort=[("_id", -1)])
            if last_entry:
                # Fetch last 10 entries for the website
                data = (
                    db[collection_name]
                    .find({}, {"_id": 0, "responseTime": 1})
                    .sort("_id", -1)
                    .limit(10)
                )
                response_times = [
                    entry["responseTime"] if entry["responseTime"] else 0
                    for entry in data
                ]

                # print(collection_name, response_times)
                # Calculate average response time
                avg_response_time = round(np.mean(response_times), 2) if response_times else 0

                website_statuses.append(
                    {
                        "website": collection_name,
                        "status": last_entry["status"],
                        "avg_response_time": avg_response_time,
                    }
                )

    # Sort website_statuses based on status severity
    status_order = {
        "Major Outage": 0,
        "Partial Outage": 1,
        "Operational (Slow Response)": 2,
        "Operational": 3,
        "Unknown Status": 4,
    }
    website_statuses.sort(key=lambda x: status_order.get(x["status"], 4))

    return render_template("index.html", website_statuses=website_statuses)



@app.route("/website/<website>")
def website_details(website):
    # Fetch last 100 entries for the selected website
    website_collection = db[website]
    data = (
        website_collection.find({}, {"_id": 0, "timestamp": 1, "responseTime": 1})
        .sort("_id", -1)
        .limit(100)
    )
    status_colours = {
        "Major Outage": "#dc3545",
        "Partial Outage": "#dc3545",
        "Operational (Slow Response)": "#ffc107",
        "Operational": "#28a745",
        "Unknown Status": "#6c757d",
    }

    # Extract timestamps and response times
    timestamps = []
    response_times = []
    for entry in data:
        timestamps.append(entry["timestamp"])
        response_times.append(entry["responseTime"])

    # Get the name of the website
    website_name = website

    # Get the current status of the website
    last_entry = website_collection.find_one({}, sort=[("_id", -1)])
    website_status = last_entry["status"] if last_entry else "Unknown"

    # Calculate maximum, minimum, and median response times
    max_response_time = max(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0
    median_response_time = median(response_times) if response_times else 0

    # Calculate average response time of the last 10 entries
    last_10_response_times = response_times[:10]  # Consider only the last 10 entries
    avg_response_time = (
        round(np.mean(last_10_response_times), 2) if last_10_response_times else 0
    )

    # Calculate status counts for pie chart
    status_counts = Counter(entry["status"] for entry in website_collection.find())
    statuses = list(status_counts.keys())

    # Calculate moving window average
    window_size = 25  # Specify the size of the moving window
    moving_window_average = calculate_moving_window_average(response_times, window_size)

    return render_template(
        "dashboard.html",
        website_name=website_name,
        website_status=website_status,
        max_response_time=max_response_time,
        min_response_time=min_response_time,
        median_response_time=median_response_time,
        avg_response_time=avg_response_time,
        moving_window_average=moving_window_average,
        timestamps=timestamps,
        response_times=response_times,
        statuses=statuses,
        status_counts=status_counts,
        status_colours=status_colours,
    )


def calculate_moving_window_average(response_times, window_size):
    moving_window_average = []
    for i in range(len(response_times)):
        start_index = max(0, i - window_size + 1)
        window = response_times[start_index : i + 1]
        moving_window_average.append(np.mean(window))
    return moving_window_average


if __name__ == "__main__":
    app.run(debug=True)
