from pymongo import MongoClient

# MongoDB connection
client = MongoClient(
    "mongodb+srv://dhirajmuppineti486:HlkvwJhB8VkMjL76@applications.eaxfxvs.mongodb.net/"
)
db = client["BAP"]  # Replace 'BAP' with your actual database name


def delete_entries():
    # Get a list of all collections in the database
    collections = db.list_collection_names()

    # Iterate over collections and delete all entries
    for collection_name in collections:
        # Delete all documents in the collection
        db[collection_name].delete_many({})
        print("Deleted all entries in collection:", collection_name)


if __name__ == "__main__":
    delete_entries()
