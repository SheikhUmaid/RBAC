
# File Management API Documentation

This API allows users to manage files, including creating, reading, updating, and deleting files. It also provides functionality to manage file permissions by adding and removing editors and viewers.

# How to Run

To run the server refer to [how_to_run.md](./how_to_run.me) file

## Authentication

### Registration

**Endpoint:** `/api/auth/register/`

**Method:** `POST`

**Request Body:**

```json
{
  "username": "your_username",
  "email": "[email address removed]",
  "password": "your_password"
}
```

**Response:**

```json
{
  "message": "User registered successfully!",
  "user": {
    "id": 123,
    "username": "your_username",
    "email": "[email address removed]"
  }
}
```

### Login

**Endpoint:** `/api/auth/login/`

**Method:** `POST`

**Request Body:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

### Logout

**Endpoint:** `/api/auth/logout/`

**Method:** `POST`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Response:**

```json
{
  "message": "success"
}
```

### Refresh Token

**Endpoint:** `/api/auth/token/refresh/`

**Method:** `POST`

**Request Body:**

```json
{
  "refresh": "your_refresh_token"
}
```

**Response:**

```json
{
  "access": "your_new_access_token"
}
```

## File Management

### List Files

**Endpoint:** `/api/file/`

**Method:** `GET`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Query Parameters:**

- `page`: Page number for pagination (default: 1)
- `page_size`: Number of items per page (default: 10)

**Response:**

```json
{
  "links": {
    "next": "next_page_url",
    "previous": "previous_page_url"
  },
  "total_pages": 5,
  "total_items": 48,
  "results": [
    {
      "id": 1,
      "name": "file_name.txt",
      "content": "file_content",
      "owner": {
        "id": 123,
        "username": "owner_username"
      },
      "editors": [
        {
          "id": 456,
          "username": "editor_username"
        }
      ],
      "viewers": [
        {
          "id": 789,
          "username": "viewer_username"
        }
      ],
      "created_at": "2024-11-28T10:00:00Z",
      "updated_at": "2024-11-28T11:00:00Z"
    }
  ]
}
```

### Create File

**Endpoint:** `/api/file/`

**Method:** `POST`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "name": "new_file.txt",
  "content": "new_file_content"
}
```

**Response:**

```json
{
  "id": 2,
  "name": "new_file.txt",
  "content": "new_file_content",
  "owner": {
    "id": 123,
    "username": "your_username"
  },
  "editors": [],
  "viewers": [],
  "created_at": "2024-11-28T12:00:00Z",
  "updated_at": "2024-11-28T12:00:00Z"
}
```

### Get File Details

**Endpoint:** `/api/file/{id}/`

**Method:** `GET`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Response:**

```json
{
  "id": 1,
  "name": "file_name.txt",
  "content": "file_content",
  "owner": {
    "id": 123,
    "username": "owner_username"
  },
  "editors": [
    {
      "id": 456,
      "username": "editor_username"
    }
  ],
  "viewers": [
    {
      "id": 789,
      "username": "viewer_username"
    }
  ],
  "created_at": "2024-11-28T10:00:00Z",
  "updated_at": "2024-11-28T11:00:00Z"
}
```

### Update File

**Endpoint:** `/api/file/{id}/`

**Method:** `PUT`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "name": "updated_file.txt",
  "content": "updated_file_content"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "updated_file.txt",
  "content": "updated_file_content",
  "owner": {
    "id": 123,
    "username": "owner_username"
  },
  "editors": [
    {
      "id": 456,
      "username": "editor_username"
    }
  ],
  "viewers": [
    {
      "id": 789,
      "username": "viewer_username"
    }
  ],
  "created_at": "2024-11-28T10:00:00Z",
  "updated_at": "2024-11-28T13:00:00Z"
}
```

### Partially Update File

**Endpoint:** `/api/file/{id}/`

**Method:** `PATCH`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "content": "partially_updated_content"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "updated_file.txt",
  "content": "partially_updated_content",
  "owner": {
    "id": 123,
    "username": "owner_username"
  },
  "editors": [
    {
      "id": 456,
      "username": "editor_username"
    }
  ],
  "viewers": [
    {
      "id": 789,
      "username": "viewer_username"
    }
  ],
  "created_at": "2024-11-28T10:00:00Z",
  "updated_at": "2024-11-28T14:00:00Z"
}
```

### Delete File

**Endpoint:** `/api/file/{id}/`

**Method:** `DELETE`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Response:**

```json
{
  "message": "File marked as deleted"
}
```

## File Permissions

### Add Editor

**Endpoint:** `/api/file/{id}/editors/`

**Method:** `POST`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "user_id": 456
}
```

**Response:**

```json
{
  "detail": "User editor_username added as an editor."
}
```

### Remove Editor

**Endpoint:** `/api/file/{id}/editors/`

**Method:** `DELETE`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "user_id": 456
}
```

**Response:**

```json
{
  "detail": "User editor_username removed from editors."
}
```

### Add Viewer

**Endpoint:** `/api/file/{id}/viewers/`

**Method:** `POST`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "user_id": 789
}
```

**Response:**

```json
{
  "detail": "User viewer_username added as a viewer."
}
```

### Remove Viewer

**Endpoint:** `/api/file/{id}/viewers/`

**Method:** `DELETE`

**Request Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "user_id": 789
}
```

**Response:**

```json
{
  "detail": "User viewer_username removed from viewers."
}
```

## Permissions

This API uses a custom permission class called `FilePermission` to control access to files. The permissions are as follows:

- **Owner:** Full access (read, write, delete)
- **Editors:** Read and write access
- **Viewers:** Read-only access

## Error Handling

The API includes comprehensive error handling and logging to provide informative error messages and track issues.

## Notes

- All endpoints require authentication, except for registration.
- The API uses pagination for listing files.
- The API supports both full and partial updates of files.
- File deletion is a "soft delete," meaning the file is marked as deleted but not permanently removed from the database.

This documentation provides a comprehensive overview of the File Management API. Please refer to the code for detailed implementation and any additional features.
