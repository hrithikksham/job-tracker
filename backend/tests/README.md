# Job Application Tracker - API Testing Guide

## Base URL

http://localhost:8000

---

# Authentication Testing

## Register User

POST /auth/register

Request:

{
"name": "Hrithik",
"email": "[hrithik@test.com](mailto:hrithik@test.com)",
"phone_number": "9876543210",
"password": "Password123"
}

Expected:

Status: 200

{
"success": true
}

---

## Duplicate Email

POST /auth/register

Use existing email.

Expected:

Status: 400

{
"detail": "Email already exists"
}

---

## Duplicate Phone Number

POST /auth/register

Use existing phone number.

Expected:

Status: 400

{
"detail": "Phone number already exists"
}

---

## Login Using Email

POST /auth/login

{
"identifier": "[hrithik@test.com](mailto:hrithik@test.com)",
"password": "Password123"
}

Expected:

Status: 200

{
"access_token": "...",
"refresh_token": "..."
}

---

## Login Using Phone Number

POST /auth/login

{
"identifier": "9876543210",
"password": "Password123"
}

Expected:

Status: 200

{
"access_token": "...",
"refresh_token": "..."
}

---

## Invalid Password

Expected:

Status: 401

{
"detail": "Invalid credentials"
}

---

## Refresh Token

POST /auth/refresh

{
"refresh_token": "..."
}

Expected:

Status: 200

{
"access_token": "..."
}

---

# Profile Testing

GET /profile

Authorization:

Bearer ACCESS_TOKEN

Expected:

Status: 200

{
"data": {
"name": "...",
"email": "...",
"phone_number": "..."
}
}

---

# Resume Testing

POST /resume/upload

Upload:

resume.pdf

Expected:

Status: 200

{
"file_id": "...",
"filename": "resume.pdf"
}
