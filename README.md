# Project Description: Adding `Course` Class and Relevant Endpoints

This project extends the existing Teacher Management API by adding a `Course` class, creating a one-to-many relationship where one teacher can be associated with multiple courses. The API will include CRUD operations for both `Teacher` and `Course`, allowing clients to manage teachers and their associated courses. For an example implementation for a one-to-many relationship, you can refer to this section in the documentation: https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship

---

## Step 1: Define the `Course` Model

Add the `Course` class to the `models.py` file. The `Course` model should include the following attributes:
- `id` - Integer (Primary Key)
- `title` - String (Course title)
- `description` - String (Course description)
- `teacher_id` - Integer (Foreign Key referencing the `Teacher` model)

The `teacher_id` field establishes a relationship between `Teacher` and `Course`, representing that each course is assigned to one teacher.

## Step 2: Update the Teacher Class

Update the Teacher class to include a relationship with Course. Add a courses attribute to represent all the courses assigned to a teacher.

## Step 3: Add the Following Endpoints
- Endpoint to Create a New Course for a Teacher: POST /teachers/{teacher_id}/courses/
- Endpoint to Get All Courses of a Teacher: GET /teachers/{teacher_id}/courses/
- Endpoint to Get a Specific Course by ID: GET /courses/{course_id}
- Endpoint to Update a Course: PUT /courses/{course_id}
- Endpoint to Delete a Course: DELETE /courses/{course_id}

# NOTE:
Make sure the courses assigned to a teacher are deleted when the teacher is deleted. For this feature you can check this section in the documentation: https://docs.sqlalchemy.org/en/14/orm/tutorial.html#deleting



