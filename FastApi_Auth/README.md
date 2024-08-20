# FastAPI CRUD Application

This FastAPI application provides a basic setup for a CRUD (Create, Read, Update, Delete) API with user authentication using JWT tokens. The application is structured to handle user authentication, create and manage items in a database, and ensure secure access to these resources.

## Features

### User Authentication
- The `/login` endpoint allows users to log in with their credentials and receive a JWT token, which is required to access other endpoints.

### CRUD Operations on Items:
- **Create Item**: The `/items/` POST endpoint allows authenticated users to create new items.
- **Read Item**: The `/items/{item_id}` GET endpoint fetches a specific item by its ID.
- **Read Items**: The `/items/` GET endpoint lists items with optional pagination.
- **Update Item**: The `/items/{item_id}` PUT endpoint updates an existing item.
- **Delete Item**: The `/items/{item_id}` DELETE endpoint deletes an item by its ID.

## Authentication Flow
- Users are authenticated via a simple dictionary-based user database.
- After successful authentication through the `/login` endpoint, a JWT token is issued, which is required to access the protected CRUD endpoints.
- The token expires after 30 minutes, after which the user needs to log in again to receive a new token.

## Database Integration
- The application uses SQLAlchemy for ORM (Object-Relational Mapping).
- `SessionLocal` is used to create and manage database sessions.
- The `get_db` dependency ensures that a database session is available to each request, and it is properly closed after the request is handled.

## Endpoints

### Login
- **POST /login**: Authenticates a user and returns a JWT token.

### Items
- **POST /items/**: Creates a new item.
- **GET /items/{item_id}**: Retrieves an item by its ID.
- **GET /items/**: Retrieves a list of items with pagination.
- **PUT /items/{item_id}**: Updates an existing item.
- **DELETE /items/{item_id}**: Deletes an item by its ID.

## Usage

### Setup:
- Ensure all dependencies are installed.
- Configure your database connection in `database.py`.

### Run the Application:
```bash
uvicorn main:app --reload
```
### Test the Endpoints:
- Use tools like curl, Postman, or any other API testing tools to interact with the API.
- Authenticate using the /login endpoint and include the Authorization: Bearer <token> header in your requests to the CRUD endpoints.

## Dependencies
- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for database operations.
- **Pydantic**: Data validation and settings management.
- **JWT**: For handling JSON Web Tokens.

