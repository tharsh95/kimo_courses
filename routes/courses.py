from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from bson.json_util import dumps
from pymongo import ReturnDocument
from db.database import courses_collection
import json
from pymongo import ASCENDING, DESCENDING


router = APIRouter()

@router.get("/courses/")
def get_courses(sort_by: Optional[str] = Query(None), domain: Optional[str] = None):
    query = {}
    if domain:
        query['domain'] = domain
    sort_options = {
        "name": ("name", ASCENDING),
        "date": ("date", DESCENDING),
        "rating": ("rating", DESCENDING)
    }
    sort_field, sort_order = sort_options.get(sort_by, ("name", ASCENDING))
    courses = courses_collection.find(query).sort(sort_field, sort_order)
    return json.loads(dumps(list(courses)))


@router.get("/courses/{course_name}")
def get_courses_by_name(course_name: str):
    query = {"name": {"$regex": course_name, "$options": "i"}}
    courses = list(courses_collection.find(query))
    return json.loads(dumps(courses)) if courses else {"error": "No courses found matching the name"}

@router.get("/courses/{course_name}/chapters/{chapter_name}")
def get_chapter_info(course_name: str, chapter_name: str):
    course = courses_collection.find_one({"name": course_name})
    if course:
        chapters = course.get("chapters", [])
        for chapter in chapters:
            if chapter['name'] == chapter_name:
                return chapter
    return {"error": "Chapter not found"}


@router.post("/courses/{course_name}/chapters/{chapter_name}/rate/")
def rate_chapter(course_name: str, chapter_name: str, rating: int):
    if not 1 <= rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
    course = courses_collection.find_one({"name": {"$regex": course_name, "$options": "i"}})
    if course:
        for chapter in course.get("chapters", []):
            if chapter_name.lower() in chapter['name'].lower():
                chapter.setdefault("ratings", []).append(rating)
                chapter["average_rating"] = sum(chapter["ratings"]) / len(chapter["ratings"])
                updated_course = courses_collection.find_one_and_update(
                    {"_id": course["_id"], "chapters.name": chapter["name"]},
                    {"$set": {"chapters.$": chapter}},
                    return_document=ReturnDocument.AFTER
                )
                # return json.loads(dumps(updated_course))
                return {"message":"Rating added successfully"}
    raise HTTPException(status_code=404, detail="Course/Chapter not found")
