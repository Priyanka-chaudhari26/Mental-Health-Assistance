# Mental Health Assistant - Web Application

### Link to Documentation: [Click here to view the file](https://drive.google.com/file/d/1pBvLReqIYXV7kCSPzNm6oYOgWo2OeepF/view?usp=sharing)
### Link to Video: [Click here to view the Video walkthrough](https://drive.google.com/file/d/1D29Wx3SXrGEYszWQ4E5vbf_Xk93PUXyp/view?usp=sharing)

## Overview

The **Mental Health Assistant** project is a comprehensive web application designed to provide a platform for users to engage with mental health-related content, share experiences, and discuss coping strategies. The platform includes features such as post creation, commenting, liking, and filtering based on various tags. It also facilitates user interaction through posts and comments, fostering a supportive community for mental health and wellness.

---

## Features

- **User Authentication**:
  - Anonymous User Registration and login using JWT (JSON Web Token) for secure authentication to reduce social stigma.
  - Optional Email Field for account recovery.

- **Post Management**:
  - Users can create posts on mental health-related topics.
  - Posts can be tagged with relevant topics for easy categorization (e.g., `Mental Health`, `Breathing Exercises`, `Anxiety`).
  - Users can like and comment on posts to interact with the content.
  
- **Dashboard**:
  - A central hub where users can view and interact with posts.
  
- **Comments and Likes**:
  - Users can post comments under a post to share their thoughts or provide support.
  - Posts can be liked, which helps indicate their popularity and enhance user engagement.

- **Post Details Page**:
  - A detailed view of a post, showing its title, content, creation date, likes, comments, and associated tags.

---
## UI/UX Design

**Sidebar**:
- Display a list of tags like Anxiety, Coping Mechanisms, etc. Users can click on a tag to see the posts.
**Post List**:
- Display a list of posts with the title, user, tags, and view details.
**Post Details**:
- View a specific post with its content, comments, likes count, and tags.
**Like & Comment**:
- Users can interact with the post by liking or commenting. Sharing their own experiences, coping strategies, etc.

---

## Technology Stack

# Frontend:
- JavaScript for building the user interface.
- Fetch API for making HTTP requests to the backend API.
# Backend:
- Django for backend development.
- Django Rest Framework (DRF) for creating REST APIs.
- SQLite for data storage.
- Authentication: JWT (JSON Web Token) for handling user authentication.


### Prerequisites

- **Node.js** (for frontend)

- **Python** (for backend)

- **Django** (Backend Framework)
  - Install using pip:
    ```bash
    pip install django
    ```

- **Django Rest Framework**
  - Install using pip:
    ```bash
    pip install djangorestframework
    ```

- **SQLite** (for the database)
  - Use Django's default database.

---

# API Endpoints

## 1. POST /api/register
**Description:** Register User.

**Request Body:**
```json
{
    "email" : "some598@gmail.com",
    "anon_username":"HappySoul2656",
    "password": "12345678"
}
```
**Response Body:**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": "3d2ae5eb-6cbf-42de-955d-1913f76f271b",
        "anon_username": "HappySoul2656",
        "email": "some598@gmail.com",
        "total_score": 0,
        "streak": 0,
        "level": 1,
        "is_active": true,
        "is_staff": false,
        "date_joined": "2025-02-22T17:56:01.244891Z",
        "last_login": null
    },
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDg1MTc2MiwiaWF0IjoxNzQwMjQ2OTYyLCJqdGkiOiIzMDc5Y2NkMDhmZDk0MzA1YWY5NTJlMDM4ODY3YTRjOCIsInVzZXJfaWQiOiIzZDJhZTVlYi02Y2JmLTQyZGUtOTU1ZC0xOTEzZjc2ZjI3MWIifQ.RyvNZxDVNoXU8-xsYt48QPXtfTbTlydJSnAJhxxrDiI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMjQ3ODYyLCJpYXQiOjE3NDAyNDY5NjIsImp0aSI6IjM2ZTYyZGQ4N2NiMTQ4ODA4NDU5OGQ1MjEzMjU5NDQ5IiwidXNlcl9pZCI6IjNkMmFlNWViLTZjYmYtNDJkZS05NTVkLTE5MTNmNzZmMjcxYiJ9.4fL8J6zTTsLO7tsMvJAqWLdknZ8huWY3Sl2lLiVH0TE"
}
```
Error Response (if username already exists):
```json
{
  "error": "A user with this anon_username already exists.",
  "suggestion": "Try this username instead: HappyLion23777f"
}
```
## 2. POST /api/login/
**Description**: Login User.

**Request Body**:
```json
{
    "anon_username": "PeacefulFox847e88",
    "password": "12345678"
}
```
**Response Body**:
```json
{
    "message": "User logged in successfully",
    "user": {
        "id": "31592fd9-7748-415b-9f8a-5df9b24d3798",
        "anon_username": "PeacefulFox847e88",
        "email": "some24@gmail.com",
        "total_score": 0,
        "streak": 0,
        "level": 1,
        "is_active": true,
        "is_staff": false,
        "date_joined": "2025-02-22T13:11:15.709972Z",
        "last_login": "2025-02-22T13:46:20.596005Z"
    },
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDgzNjc4MCwiaWF0IjoxNzQwMjMxOTgwLCJqdGkiOiI2YmFjNGE3ZjA2ZjU0YzI0OWI5MTU2ZjNiYmE0MGRkNiIsInVzZXJfaWQiOiIzMTU5MmZkOS03NzQ4LTQxNWItOWY4YS01ZGY5YjI0ZDM3OTgifQ.Rhw5nJihKMRkPsQKaH5rv-PeGeMbdhH3LER_GzVuOUQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMjMyODgwLCJpYXQiOjE3NDAyMzE5ODAsImp0aSI6IjdiNWU1ZTAzMTdmYzQ1ZDBiZmQ5ZWQ5MjU3MDU0NmJjIiwidXNlcl9pZCI6IjMxNTkyZmQ5LTc3NDgtNDE1Yi05ZjhhLTVkZjliMjRkMzc5OCJ9.944Ew6tLH6GYlauHfR7rp-gQZb5k7zxibzUF-e5y7QE"
}
```
## 3. POST /api/posts/
**Description**: Create a new post.

**Request Body**:
{
  "title": "Title of the Post",
  "content": "Content of the post...",
  "tags": ["Mental Health", "Anxiety"]
}
**Response Body**:
```json
{
  "id": "new-post-id",
  "user": "user-uuid",
  "title": "Title of the Post",
  "content": "Content of the post...",
  "tags": ["Mental Health", "Anxiety"],
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```
## 4. GET /api/posts/
**Description**: Retrieve a list of all posts.

**Response**:
```json
[
  {
    "id": "post-id",
    "user": "user-uuid",
    "title": "Post Title",
    "content": "Post content...",
    "tags": ["tag1", "tag2"],
    "likes_count": 5,
    "comments": [
      {
        "user": "user-uuid",
        "content": "This is a comment",
        "created_at": "timestamp"
      }
    ]
  },
  ...
]
```
## 5. POST /api/posts/<uuid:pk>/like/
**Description**: Like a post.

**Request Body**: None

**Response**:
```json
{
  "detail": "Post liked"
}
```

## 6. POST /api/posts/<uuid:pk>/comment/
**Description**: Post a comment on a specific post.

**Request Body**:
```json
{
  "content": "This is a comment on the post."
}
```
**Response Body**:
```json
{
  "id": "new-comment-id",
  "user": "user-uuid",
  "content": "This is a comment on the post.",
  "created_at": "timestamp"
}
```
## 7. GET /api/posts/uuid:pk/
**Description**: Retrieve the details of a specific post.

**Response**:
```json
{
  "id": "0953e82c-98a9-4f15-9010-20fb4c14e0fd",
  "user": "PeacefulFox847e88",
  "title": "How do you manage daily anxiety?",
  "content": "I've been struggling with anxiety and looking for tips that worked for others.",
  "created_at": "2025-02-22T13:24:37.127338Z",
  "updated_at": "2025-02-22T13:24:37.127338Z",
  "comments": [
    {
      "id": 1,
      "user": "PeacefulFox847e88",
      "content": "Breathing exercises really help me manage anxiety.",
      "created_at": "2025-02-22T13:34:51.071384Z"
    }
  ],
  "likes_count": 1,
  "tags": [
    {"id": 1, "name": "Anxiety"},
    {"id": 13, "name": "Coping Mechanisms"}
  ]
}
```

---
# Conclusion
## The Mental Health Assistant is a comprehensive web application designed to foster a community around mental health awareness and coping strategies. By offering an interactive space for sharing and discussing experiences, this platform promotes mental well-being and support.
