# FastAPI Basic Authentication Example

This FastAPI application provides a simple example of basic authentication using HTTP Basic credentials. It includes a single endpoint that requires authentication to access.

## Features

### Basic Authentication
- The application uses HTTP Basic authentication to secure the `/basic-auth` endpoint.

### Authentication Check
- The `authentication_user` function verifies if the provided username and password match the hardcoded credentials.

## Authentication Flow

### Credentials
- The application uses the username `testuser` and password `testpass` for authentication.

### Access Control
- If the provided credentials are correct, the user receives a successful authentication message.
- Otherwise, a 401 Unauthorized error is returned.

## Endpoints

### Basic Auth Endpoint
- **GET /basic-auth**: Requires valid credentials (`testuser` / `testpass`) to access. Returns a message indicating successful authentication.

## Usage

### Setup:
- Ensure all dependencies are installed.

### Run the Application:
```bash
uvicorn main:app --reload
```

## Test the Endpoint

- Use tools like `curl`, Postman, or any other API testing tool to interact with the API.
- Access the `/basic-auth` endpoint and provide the basic authentication credentials (`testuser` / `testpass`).

## Dependencies

- **FastAPI**: Web framework for building APIs.
- **HTTPBasic**: FastAPI's implementation of HTTP Basic authentication.

## Security

- This example uses hardcoded credentials. For production use, consider integrating a more secure authentication mechanism and managing credentials securely.

