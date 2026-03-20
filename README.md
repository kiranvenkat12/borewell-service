Borewell Repair & Stuck Motor Service – Backend

Overview

This backend handles the complete workflow of borewell repair operations — starting from customer request creation to job completion.

The system is designed to solve a real problem: managing borewell issues like stuck motors, assigning field workers, tracking progress, and storing work-related data in a structured way.

Built using FastAPI with PostgreSQL as the database.

Tech Stack

FastAPI

PostgreSQL

SQLAlchemy

JWT Authentication

Pydantic

File Upload (images)

Features
1. Customer Request Handling

Customers can create a repair request by providing:

Name

Address

Borewell depth

Motor stuck status

Optional image upload

Each request is stored in the database and initialized with pending status.

2. Job Assignment

Admin can assign a worker to a specific request.

Once assigned:

Status changes from pending → assigned

Assignment is stored separately for tracking

3. Work Tracking

Workers can:

View assigned jobs

Update job status (in_progress, completed)

Upload images after completing the work

Add details like time spent and cost

4. Status Flow

Every request follows a fixed lifecycle:

pending → assigned → in_progress → completed
5. File Upload

Images can be uploaded during request creation and after work completion

Files are stored locally in an /uploads folder

File paths are stored in the database

6. Authentication & Authorization

JWT-based authentication is implemented.

There are two roles:

Admin

Can assign jobs

Can view all requests

Full access

Worker

Can view only assigned jobs

Can update status and upload work details

API Endpoints
Auth

POST /auth/login
Login for admin/worker and returns JWT token.

Requests

POST /requests/
Create a new repair request (supports file upload)

GET /requests/
Get all requests (Admin only, supports filters)

GET /requests/{id}
Get details of a specific request

Assignment

POST /assign/
Assign a worker to a request (Admin only)

Status Update

PUT /requests/{id}/status
Update request status

Work Logs

POST /work-log/
Add work details (time spent, cost, notes)

File Upload

POST /upload/
Upload images related to a request

GET /files/{request_id}
Get all files for a request

Worker APIs

GET /worker/jobs
Get all jobs assigned to the logged-in worker

Database Design

Main tables used:

users → stores admin and worker accounts

requests → customer repair requests

assignments → worker-job mapping

work_logs → work completion details

files → uploaded images

Relationships are maintained using foreign keys.

Project Structure
app/
 |── main.py
 ├── models/
 ├── schemas/
 ├── routes/
 ├── db/
 ├── core/
 ├── uploads/
How to Run

Clone the repository

Create a virtual environment

Install dependencies

pip install -r requirements.txt

Configure PostgreSQL in .env

Run the server

uvicorn main:app --reload

Open Swagger UI

http://127.0.0.1:8000/docs
Notes

Passwords are stored in hashed format

JWT is required for protected routes

File handling is currently local (can be extended to cloud storage later)

Future Improvements

SMS/email notifications

Map-based request tracking

Analytics dashboard

Cloud storage for files