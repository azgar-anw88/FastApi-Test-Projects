# FastAPI Basic Authentication CRUD Application

This FastAPI application demonstrates a CRUD (Create, Read, Update, Delete) API with basic authentication. The application manages items in a database, ensuring that only authenticated users can access the CRUD operations.

## Features

### Basic Authentication
- The application uses HTTP Basic authentication to secure the endpoints. Only users with valid credentials can perform CRUD operations.

### CRUD Operations on Items:
- **Create Item**: The `/items/` POST endpoint allows authenticated users to create new items.
- **Read Item**: The `/items/{item_id}` GET endpoint fetches a specific item by its ID.
- **Read Items**: The `/items/` GET endpoint lists items with optional pagination.
- **Update Item**: The `/items/{item_id}` PUT endpoint updates an existing item.
- **Delete Item**: The `/items/{item_id}` DELETE endpoint deletes an item by its ID.

## Authentication Flow
- Basic authentication is implemented using the `HTTPBasic` class from FastAPI.
- The `authentication_user` function checks the provided username and password.
- Currently, the application uses a simple hardcoded user credential check. In this case, the username is `"azgar"` and the password is `"azgar123"`.
- If the credentials are valid, the user is allowed to access the CRUD endpoints; otherwise, a 401 Unauthorized error is returned.

## Database Integration
- The application uses SQLAlchemy for ORM (Object-Relational Mapping).
- `SessionLocal` is used to create and manage database sessions.
- The `get_db` dependency ensures that a database session is available to each request, and it is properly closed after the request is handled.

## Endpoints

### Items
- **POST /items/**: Creates a new item. Requires valid credentials.
- **GET /items/{item_id}**: Retrieves an item by its ID. Requires valid credentials.
- **GET /items/**: Retrieves a list of items with pagination. Requires valid credentials.
- **PUT /items/{item_id}**: Updates an existing item. Requires valid credentials.
- **DELETE /items/{item_id}**: Deletes an item by its ID. Requires valid credentials.

## Usage

### Setup:
- Ensure all dependencies are installed.
- Configure your database connection in `database.py`.

### Run the Application:
```bash
uvicorn main:app --reload
```
## Test the Endpoints

- Use tools like `curl`, Postman, or any other API testing tools to interact with the API.
- Provide the basic authentication credentials (`azgar` / `azgar123`) when accessing the CRUD endpoints.

## Dependencies

- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for database operations.
- **HTTPBasic**: FastAPI's implementation of HTTP Basic authentication.

## Security

- Ensure that the hardcoded credentials are replaced with a more secure authentication mechanism for production use.
- Consider integrating a database-backed user authentication system for better security.
