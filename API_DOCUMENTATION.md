# 📚 Family Tree API Documentation

## Overview

This document provides detailed API documentation for the Family Tree application endpoints.

## Base URL

```
Development: http://localhost:5000
Production: https://your-domain.com
```

## Authentication

All protected endpoints require user to be logged in. Authentication is session-based using Flask-Login.

### Login Flow
1. User registers: `POST /auth/register`
2. User logs in: `POST /auth/login`
3. Session cookie is set automatically
4. User can access protected endpoints

---

## Endpoints

### Authentication Endpoints

#### Register New User
```http
POST /auth/register
Content-Type: application/x-www-form-urlencoded

Parameters:
  username        (required) - Unique username (string)
  email           (required) - Valid email address (string)
  password        (required) - Minimum 6 characters (string)
  confirm_password (required) - Must match password (string)
  first_name      (optional) - User's first name (string)
  last_name       (optional) - User's last name (string)

Response (Success - 302 Redirect):
  Redirects to login page
  Flash message: "Registration successful! Please log in."

Response (Error - 302 Redirect):
  Redirects back to registration page
  Flash message with error details
```

**Example:**
```bash
curl -X POST http://localhost:5000/auth/register \
  -d "username=john_doe" \
  -d "email=john@example.com" \
  -d "password=password123" \
  -d "confirm_password=password123" \
  -d "first_name=John" \
  -d "last_name=Doe"
```

#### Login User
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

Parameters:
  username (required) - Username (string)
  password (required) - Password (string)

Response (Success - 302 Redirect):
  Sets session cookie
  Redirects to dashboard
  Flash message: "Login successful"

Response (Error - 302 Redirect):
  Redirects back to login page
  Flash message: "Invalid username or password"
```

**Example:**
```bash
curl -X POST http://localhost:5000/auth/login \
  -c cookies.txt \
  -d "username=john_doe" \
  -d "password=password123"
```

#### Logout User
```http
GET /auth/logout
Authorization: Session Cookie

Response (Success - 302 Redirect):
  Clears session
  Redirects to login page
  Flash message: "You have been logged out successfully"
```

---

### Dashboard Endpoints

#### Get Dashboard
```http
GET /dashboard
Authorization: Session Cookie (Required)

Query Parameters:
  page (optional) - Page number (default: 1, integer)

Response (200 OK):
  Returns HTML dashboard with:
  - Family statistics (total, male, female count)
  - Paginated list of family members
  - Search bar
  - Quick action buttons

Response (401 Unauthorized):
  Redirects to login page
```

#### Get User Profile
```http
GET /profile
Authorization: Session Cookie (Required)

Response (200 OK):
  Returns HTML profile page with:
  - User information (username, email, name)
  - Account creation date
  - Member since information

Response (401 Unauthorized):
  Redirects to login page
```

#### Search Family Members
```http
GET /search
Authorization: Session Cookie (Required)

Query Parameters:
  q (required) - Search query (string, minimum 1 character)

Response (200 OK):
  Returns HTML search results page with:
  - List of matching members
  - Member cards with details
  - Quick action links

Response (400 Bad Request):
  Missing or invalid search query

Example:
  /search?q=John
  /search?q=john@example.com
  /search?q=555-1234
```

---

### Family Member Endpoints

#### Add Family Member
```http
GET /family/add
Authorization: Session Cookie (Required)

Response (200 OK):
  Returns HTML form for adding new family member
  Includes dropdown lists for:
  - Father (optional)
  - Mother (optional)
  - Spouse (optional)

---

POST /family/add
Authorization: Session Cookie (Required)
Content-Type: application/x-www-form-urlencoded

Parameters:
  first_name    (required) - String, max 100 chars
  last_name     (required) - String, max 100 chars
  gender        (required) - Enum: "Male", "Female", "Other"
  dob           (optional) - Date (YYYY-MM-DD format)
  phone         (optional) - String, max 20 chars
  email         (optional) - Valid email address
  address       (optional) - Text
  biography     (optional) - Text
  father_id     (optional) - Integer (family member ID)
  mother_id     (optional) - Integer (family member ID)
  spouse_id     (optional) - Integer (family member ID)

Response (Success - 302 Redirect):
  Creates new family member
  Redirects to member profile
  Flash message: "John Doe added successfully!"

Response (Error - 302 Redirect):
  Redirects back to form
  Flash message with error details

Example:
  first_name=John&last_name=Doe&gender=Male&dob=1990-01-15
```

#### View Family Member
```http
GET /family/<id>
Authorization: Session Cookie (Required)

URL Parameters:
  id (required) - Family member ID (integer)

Response (200 OK):
  Returns HTML profile page with:
  - Member photo (if available)
  - Personal information
  - Contact details
  - Family relationships
  - Children list
  - Edit and delete buttons (if owner)

Response (401 Unauthorized):
  Flash message: "You do not have permission"
  Redirects to dashboard

Response (404 Not Found):
  Member not found

Example:
  /family/1
  /family/42
```

#### Edit Family Member
```http
GET /family/<id>/edit
Authorization: Session Cookie (Required)

URL Parameters:
  id (required) - Family member ID (integer)

Response (200 OK):
  Returns HTML form with current member data
  Pre-filled with all fields

Response (401 Unauthorized):
  Redirects to dashboard

---

POST /family/<id>/edit
Authorization: Session Cookie (Required)
Content-Type: application/x-www-form-urlencoded

URL Parameters:
  id (required) - Family member ID (integer)

Parameters:
  (Same as POST /family/add)

Response (Success - 302 Redirect):
  Updates family member
  Redirects to member profile
  Flash message: "John Doe updated successfully!"

Response (Error - 302 Redirect):
  Redirects back to form
  Flash message with error details
```

#### Delete Family Member
```http
POST /family/<id>/delete
Authorization: Session Cookie (Required)

URL Parameters:
  id (required) - Family member ID (integer)

Response (Success - 302 Redirect):
  Deletes family member
  Redirects to dashboard
  Flash message: "John Doe has been deleted"

Response (401 Unauthorized):
  Flash message: "You do not have permission"
  Redirects to dashboard

Response (404 Not Found):
  Member not found
```

#### View Family Tree
```http
GET /family/tree
Authorization: Session Cookie (Required)

Response (200 OK):
  Returns HTML page with:
  - Interactive family tree visualization
  - Family statistics
  - List of all family members
  - Member cards with quick links

Response (401 Unauthorized):
  Redirects to login page
```

---

### File Upload Endpoints

#### Upload Member Photo
```http
POST /upload/photo/<id>
Authorization: Session Cookie (Required)
Content-Type: multipart/form-data

URL Parameters:
  id (required) - Family member ID (integer)

Form Data:
  photo (required) - Image file (PNG, JPG, JPEG, GIF)
                    Maximum 16 MB

Response (Success - 302 Redirect):
  Saves photo
  Resizes to max 300x300px
  Redirects to member profile
  Flash message: "Photo uploaded successfully!"

Response (Error - 302 Redirect):
  Redirects to member profile
  Flash message with error details

Allowed Formats:
  - PNG (.png)
  - JPG (.jpg)
  - JPEG (.jpeg)
  - GIF (.gif)

Maximum Size: 16 MB

Example:
  curl -X POST http://localhost:5000/upload/photo/1 \
    -c cookies.txt \
    -F "photo=@family_photo.jpg"
```

#### Delete Member Photo
```http
POST /upload/photo/<id>/delete
Authorization: Session Cookie (Required)

URL Parameters:
  id (required) - Family member ID (integer)

Response (Success - 302 Redirect):
  Deletes photo from server
  Redirects to member profile
  Flash message: "Photo deleted successfully!"

Response (Error - 302 Redirect):
  Redirects to member profile
  Flash message with error details
```

---

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful, returning page/data |
| 302 | Found | Redirect (common for form submissions) |
| 400 | Bad Request | Invalid parameters or missing required fields |
| 401 | Unauthorized | User not logged in or session expired |
| 403 | Forbidden | User lacks permission for this action |
| 404 | Not Found | Resource (member, photo, etc.) not found |
| 500 | Server Error | Internal server error |

---

## Error Handling

### Common Error Messages

```
Registration Errors:
- "Username already exists"
- "Email already registered"
- "Passwords do not match"
- "Password must be at least 6 characters"

Login Errors:
- "Invalid username or password"

Permission Errors:
- "You do not have permission to view this member"
- "You do not have permission to edit this member"
- "You do not have permission to delete this member"

Upload Errors:
- "No file selected"
- "Only PNG, JPG, JPEG, and GIF files are allowed"
- "File too large (maximum 16 MB)"

Member Errors:
- "First name, last name, and gender are required"
- "Member not found"
```

---

## Data Models

### User Object
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### FamilyMember Object
```json
{
  "id": 1,
  "user_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "gender": "Male",
  "dob": "1990-01-15",
  "phone": "555-1234",
  "email": "john@example.com",
  "address": "123 Main St, City, State",
  "biography": "Family member biography...",
  "photo": "1_john_doe_photo.jpg",
  "father_id": null,
  "mother_id": null,
  "spouse_id": 2,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Relationship Object
```json
{
  "id": 1,
  "member_id": 1,
  "related_member_id": 2,
  "relationship_type": "sibling",
  "notes": "Relationship notes...",
  "created_at": "2024-01-15T10:30:00"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider:
- Limit login attempts: 5 attempts per 15 minutes
- Limit photo uploads: 10 per hour per user
- Limit searches: 100 per hour per user

---

## Security

### HTTPS
Use HTTPS in production to encrypt all data in transit.

### Session Security
- Sessions expire after browser close (configurable)
- Secure cookies in production
- CSRF protection on all form submissions

### File Upload Security
- File type validation
- File size limits
- Filename sanitization
- Virus scanning recommended

### SQL Injection
SQLAlchemy ORM prevents SQL injection by default.

### XSS Protection
Jinja2 templates auto-escape HTML by default.

---

## Pagination

When results are paginated:

```
GET /dashboard?page=1
GET /dashboard?page=2
```

Response includes:
- Current page
- Total pages
- Has previous/next page
- Page items (10 per page)

---

## Sorting

Currently supports sorting by:
- Name (A-Z)
- Date Added (Newest First)
- Gender (Male, Female, Other)

---

## Filtering

Search supports:
- First name (partial match)
- Last name (partial match)
- Email (partial match)
- Gender
- Birth year

---

## Webhooks

Not currently implemented. Planned for future versions.

---

## Versioning

Current API Version: **1.0.0**

Breaking changes will increment major version.
New features will increment minor version.
Bug fixes will increment patch version.

---

## Examples

### Complete User Journey

```bash
# 1. Register
curl -X POST http://localhost:5000/auth/register \
  -d "username=jane_doe" \
  -d "email=jane@example.com" \
  -d "password=secure_password_123" \
  -d "confirm_password=secure_password_123" \
  -d "first_name=Jane" \
  -d "last_name=Doe"

# 2. Login
curl -X POST http://localhost:5000/auth/login \
  -c cookies.txt \
  -d "username=jane_doe" \
  -d "password=secure_password_123"

# 3. Add family member
curl -X POST http://localhost:5000/family/add \
  -b cookies.txt \
  -d "first_name=John" \
  -d "last_name=Doe" \
  -d "gender=Male" \
  -d "dob=1960-06-15"

# 4. Upload photo
curl -X POST http://localhost:5000/upload/photo/1 \
  -b cookies.txt \
  -F "photo=@john_photo.jpg"

# 5. Search members
curl -X GET "http://localhost:5000/search?q=John" \
  -b cookies.txt

# 6. Logout
curl -X GET http://localhost:5000/auth/logout \
  -b cookies.txt
```

---

## Testing with cURL

### Using Cookie Jar
```bash
# Save cookies
curl -X POST http://localhost:5000/auth/login \
  -c cookies.txt \
  -d "username=john_doe" \
  -d "password=password123"

# Use saved cookies
curl -X GET http://localhost:5000/dashboard \
  -b cookies.txt

# Clear cookies
rm cookies.txt
```

---

## Testing with Postman

1. Create new Postman collection
2. Add requests for each endpoint
3. Use Postman's cookie jar to manage sessions
4. Save collection for team use

---

## Future API Enhancements

- [ ] REST API endpoints
- [ ] JSON responses
- [ ] API key authentication
- [ ] OAuth 2.0 support
- [ ] GraphQL endpoint
- [ ] Rate limiting
- [ ] Webhooks
- [ ] API versioning
- [ ] SDK/Library support

---

## Support

For API support:
1. Check this documentation
2. Review error messages
3. Check GitHub issues
4. Contact support team

---

**Last Updated**: January 2024
**Version**: 1.0.0
