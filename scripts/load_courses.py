import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['CourseCatalog']
courses_collection = db['courses']

courses_collection.create_index([('name', 1)])  
courses_collection.create_index([('date', -1)])  
courses_collection.create_index([('domain', 1)]) 

with open('scripts/courses.json') as file:
    courses_data = json.load(file)
    courses_collection.insert_many(courses_data)

print("Courses inserted successfully!")
