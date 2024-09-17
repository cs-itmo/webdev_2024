# Authentication

This lesson explains how to implement JWT-based authentication in FastAPI. It covers user schema design, utilities for password hashing, and database integration for storing user information.

## Files and Descriptions

| File Name                                      | Description                                                       |
|------------------------------------------------|-------------------------------------------------------------------|
| [auth.py](auth.py)                             | Main authentication logic and routes.                             |
| [database.py](database.py)                     | SQLite database setup and user table definition.                  |
| [schemas.py](schemas.py)                       | Pydantic models for user schema.                                  |
| [utils.py](utils.py)                           | Utility functions for password hashing and token generation.      |
| [main.py](main.py)                             | FastAPI application entry point.                                  |
| [0-jwt.py](0-jwt.py)                           | Example of JWT token generation and validation.                   |
