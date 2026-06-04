# Job Application Tracker - Technical Design Document (V1)

## 1. Project Overview

### Objective

A minimalist personal job application tracker that allows users to quickly record, manage, and monitor job applications with minimal effort.

The application focuses on simplicity and speed rather than complex ATS-style workflows.

---

## 2. Problem Statement

Job seekers apply through multiple sources:

* LinkedIn
* Wellfound
* Company Career Pages
* Referrals
* Naukri

Common issues:

* Forgetting where applications were submitted
* Losing job URLs
* Missing follow-up opportunities
* No centralized application history
* Difficulty tracking progress

The system provides a single dashboard for managing all applications.

---

## 3. MVP Features

### Application Management

* Add Application
* Edit Application
* Delete Application
* View Application Details
* Filter Applications

### Dashboard

* Total Applications
* Applied Count
* In Process Count
* Rejected Count
* Offer Accepted Count

### User Profile

* Registration
* Login
* Profile Management

### AI Integration (Optional MVP+)

Paste Job Description and generate:

* Key Skills
* Experience Requirements
* Important Keywords
* Application Summary

---

## 4. Functional Requirements

### User Module

Users should be able to:

* Register
* Login
* View Profile
* Update Profile

---

### Application Module

Users should be able to:

* Create application
* Update application
* Delete application
* View application list
* Filter applications

---

## 5. Status Lifecycle

The application follows a simplified workflow.

```text
Applied
    |
    v
In Process
    |
    +------> Rejected
    |
    +------> Offer Accepted
```

### Status Enum

```python
class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    IN_PROCESS = "In Process"
    REJECTED = "Rejected"
    OFFER_ACCEPTED = "Offer Accepted"
```

---

## 6. Technology Stack

### Frontend

* React
* Tailwind CSS
* Axios

### Backend

* FastAPI
* Pydantic

### Database

* MongoDB

### Authentication

* JWT Authentication

### Deployment

* Frontend: Vercel
* Backend: Railway / Render
* Database: MongoDB Atlas

### AI Services

* OpenAI API

---

## 7. High-Level Architecture

```text
+-------------------+
|   React Frontend  |
+-------------------+
          |
          |
       REST API
          |
          v
+-------------------+
|      FastAPI      |
+-------------------+
          |
          |
     Mongo Driver
          |
          v
+-------------------+
|     MongoDB       |
+-------------------+
```

---

## 8. Database Design

### Collection: Users

```json
{
  "_id": "uuid",
  "name": "Hrithik",
  "email": "hrithik@gmail.com",
  "phone_number": "9999999999",
  "password_hash": "...",
  "resume_url": "resume.pdf",
  "created_at": "2025-08-20",
  "updated_at": "2025-08-20"
}
```

---

### Collection: Applications

```json
{
  "_id": "uuid",

  "user_id": "uuid",

  "company_name": "Google",

  "company_link":
  "https://google.com",

  "role":
  "Software Engineer",

  "job_url":
  "https://careers.google.com",

  "status":
  "Applied",

  "applied_date":
  "2025-08-20",

  "follow_up_date":
  "2025-08-27",

  "hr_email":
  "recruiter@google.com",

  "notes":
  "Applied through referral",

  "created_at":
  "2025-08-20",

  "updated_at":
  "2025-08-20"
}
```

---

## 9. Field Definitions

### Required Fields

| Field        | Type   |
| ------------ | ------ |
| company_name | String |
| role         | String |
| applied_date | Date   |
| status       | Enum   |

---

### Optional Fields

| Field          | Type   |
| -------------- | ------ |
| company_link   | URL    |
| job_url        | URL    |
| hr_email       | String |
| notes          | Text   |
| follow_up_date | Date   |

---

## 10. Indexing Strategy

### Applications Collection

Indexes:

```javascript
status
```

Reason:

Frequently used for filtering.

---

```javascript
applied_date
```

Reason:

Frequently used for sorting.

---

```javascript
user_id
```

Reason:

Every query is user-specific.

---

Compound Index:

```javascript
{
  user_id: 1,
  status: 1
}
```

Reason:

Optimizes:

```http
GET /applications?status=Applied
```

---

## 11. API Design

### Authentication APIs

#### Register

```http
POST /api/auth/register
```

---

#### Login

```http
POST /api/auth/login
```

Returns JWT token.

---

#### Get Profile

```http
GET /api/profile
```

---

#### Update Profile

```http
PATCH /api/profile
```

---

## Application APIs

### Create Application

```http
POST /api/applications
```

---

### Get Applications

```http
GET /api/applications
```

---

### Get Single Application

```http
GET /api/applications/{id}
```

---

### Update Application

```http
PATCH /api/applications/{id}
```

---

### Delete Application

```http
DELETE /api/applications/{id}
```

---

## 12. Filtering

### Filter By Status

```http
GET /api/applications?status=Applied
```

---

### Filter By Date

```http
GET /api/applications?from=2025-01-01&to=2025-12-31
```

---

### Search By Company

```http
GET /api/applications?company=Google
```

---

## 13. Pagination

Cursor-based pagination.

Request:

```http
GET /api/applications?cursor=abc123&limit=20
```

Response:

```json
{
  "data": [],
  "next_cursor": "xyz123"
}
```

Benefits:

* Faster than offset pagination
* Better scalability
* Consistent results

---

## 14. Validation Rules

### Company Name

* Required
* Maximum 100 characters

### Role

* Required
* Maximum 100 characters

### Email

* Must be valid email format

### URLs

* Must be valid URL format

### Status

Allowed values:

```text
Applied
In Process
Rejected
Offer Accepted
```

---

## 15. Error Handling

### Example

```json
{
  "success": false,
  "message": "Application not found"
}
```

HTTP Code:

```http
404 NOT FOUND
```

---

## 16. Edge Cases

### Multiple Applications To Same Company

Allowed.

Reason:

Users may apply for multiple roles.

Example:

```text
Google - Backend Engineer

Google - Full Stack Engineer
```

---

### Empty Optional Fields

Allowed.

Store as null.

---

### Missing Required Fields

Reject request.

```http
400 BAD REQUEST
```

---

### Default Status

When a new application is created:

```text
Applied
```

---

## 17. Dashboard Metrics

### Total Applications

```python
count(applications)
```

---

### Applied

```python
status == Applied
```

---

### In Process

```python
status == In Process
```

---

### Rejected

```python
status == Rejected
```

---

### Offer Accepted

```python
status == Offer Accepted
```

---

### Success Rate

```python
offer_accepted / total_applications
```

---

## 18. Backend Folder Structure

```text
backend/

├── app/
│
├── api/
│   ├── auth.py
│   ├── applications.py
│
├── models/
│   ├── user.py
│   ├── application.py
│
├── schemas/
│   ├── user.py
│   ├── application.py
│
├── services/
│   ├── auth_service.py
│   ├── application_service.py
│
├── repositories/
│   ├── user_repository.py
│   ├── application_repository.py
│
├── database/
│   └── mongodb.py
│
├── utils/
│   ├── jwt.py
│   └── validators.py
│
└── main.py
```

---

## 19. Future Enhancements

### V2

* Follow-up reminders
* Kanban board
* Resume version tracking
* Dark mode
* Mobile responsive improvements

### V3

* Chrome Extension
* LinkedIn one-click save
* Job Description Analyzer
* AI-generated interview questions
* Resume match scoring

---

## 20. Engineering Decisions

### Why FastAPI?

* High performance
* Built-in validation with Pydantic
* Easy OpenAPI documentation
* Python ecosystem support

### Why MongoDB?

* Fast MVP development
* Flexible schema evolution
* Easy integration with FastAPI

### Why UUID?

* Non-sequential IDs
* Better security
* Easier future scalability

### Why Cursor Pagination?

* Better performance than page-based pagination
* Suitable for growing datasets
* Avoids duplicate records during updates


# DEVELOPEMENT ORDER

1. MongoDB Connection
2. User Schema
3. JWT Authentication
4. Register API
5. Login API
6. Application Schema
7. CRUD APIs
8. Dashboard APIs
9. React Authentication
10. Dashboard UI
11. Application Table
12. Add/Edit/Delete Forms
13. Filters
14. Deployment