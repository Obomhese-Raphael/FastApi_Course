# Importing the FastAPI class from the fastapi module
from typing import Optional  # Or just use | None
from fastapi import FastAPI, Path
from pydantic import BaseModel

# Creating an instance of the FastAPI class
app = FastAPI()

students = {
    1: {"name": "John", "age": 20, "year": "Year 12"},
    2: {"name": "Jane", "age": 22, "year": "Year 12"},
    3: {"name": "Doe", "age": 21, "year": "Year 11"},
    4: {"name": "Smith", "age": 19, "year": "Year 10"},
    5: {"name": "Emily", "age": 23, "year": "Year 12"},
    6: {"name": "Michael", "age": 18, "year": "Year 10"},
    7: {"name": "Sarah", "age": 20, "year": "Year 11"},
    8: {"name": "David", "age": 22, "year": "Year 12"},
    9: {"name": "Anna", "age": 21, "year": "Year 11"},
    10: {"name": "Tom", "age": 19, "year": "Year 10"},
}


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

# Creating an endpoint for the root URL


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Creating an endpoint to get a student by ID


@app.get("/get-students")
def get_students():
    return students


# Creating an endpoint to get a student by their ID, using a path parameter to specify the student ID
@app.get("/get-students/{student_id}")
# Defining a function that takes the student_id as a parameter, which is extracted from the URL path.
# The Path function is used to provide additional metadata about the parameter, such as a description.
def get_student(student_id: int = Path(..., description="The ID of the student to retrieve")):
    return students.get(student_id, {"error": "Student not found"})


@app.get("/get-by-name")
def get_by_name(name: Optional[str] = None):
    if not name:
        return {"message": "No name provided, showing all students", "data": students}

    for student_id, student in students.items():
        if student["name"].lower() == name.lower():
            return {student_id: student}

    return {"error": "Student not found"}


# Getting a user id and the name of the user using query parameters
@app.get("/get-by-name/{student_id}")
def get_by_name(student_id: int, name: Optional[str] = None):
    student = students.get(student_id)
    if not student:
        return {"error": "Student not found"}

    if name and student["name"].lower() != name.lower():
        return {"error": "Name does not match the student ID"}

    return {student_id: student}


# Creating an endpoint to create a new student using a POST request
@app.post("/create-student/{student_id}")
# Defining a function that takes the student_id as a path parameter and a student object in the request body.
# The student object is defined using the Student model, which is a Pydantic model that validates the input data.
def create_student(student_id: int, student: Student):
    # Checking if the student ID already exists in the students dictionary.
    # If it does, return an error message.
    if student_id in students:
        return {"error": "Student ID already exists"}

    # If the student ID does not exist, add the new student to the students dictionary using the student_id as the key and the student data as the value.
    students[student_id] = student.model_dump()
    return {"message": "Student created successfully", "student": students[student_id]}


# PUT METHOD TO UPDATE A STUDENT
@app.put("/update-student/{student_id}")
# Defining a function that takes the student_id as a path parameter and an UpdateStudent object in the request body.
def update_student(student_id: int, student: UpdateStudent):
    # Checking if the student ID exists in the students dictionary. If it does not, return an error message.
    if student_id not in students:
        return {"error": "Student not found"}

    # Update only the fields that were actually provided in the request
    update_data = student.model_dump(exclude_unset=True)  # Key change here

    # Iterating over the update_data dictionary and updating the corresponding fields in the students dictionary for the specified student_id.
    for field, value in update_data.items():
        students[student_id][field] = value

    return {"message": "Student updated successfully", "student": students[student_id]}
