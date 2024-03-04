# Proyecto de bases de Datos 2
- Angel Castellanos
- Alejandro Azurdia
- Diego Morales

`ChaChatGT` - MongoDb proyect

[ChaChatGT Project](http://chachatgt.netlify.app)

[![Video](https://img.youtube.com/vi/MCCjDr3qZoo/0.jpg)](https://youtu.be/MCCjDr3qZoo)


## Overview

This documentation outlines the API endpoints, data models, and functionalities for a messaging application. The application supports user management (creation, update, deletion), handling user profiles (including profile pictures), authentication, conversation management, and message handling within conversations.

## API Endpoints

### User Management

#### Create User (`POST /users`)

- **Description**: Registers a new user with a profile picture.
- **Body**:
  - `user`: `User` model (without `id`)
  - `profile_pic`: File (profile picture)
- **Response**: JSON with status code and message.
- **Errors**:
  - `400` if the user already exists.

#### Update User (`PUT /users`)

- **Description**: Updates an existing user's information.
- **Body**: `UserUpdate` model.
- **Response**: JSON with status code and message.
- **Errors**:
  - `404` if the user does not exist.

#### Delete User (`POST /users/delete`)

- **Description**: Deletes an existing user and their associated data.
- **Body**: `UserDelete` model.
- **Response**: JSON with status code and message.
- **Errors**:
  - `404` if the user does not exist.

### Authentication

#### Login (`POST /login`)

- **Description**: Authenticates a user by their ID and password.
- **Body**: `LoginData` model.
- **Response**: JSON with status code and message.
- **Errors**:
  - `404` if the user does not exist.
  - `401` if credentials are invalid.

### Conversation Management

#### Create Conversation (`POST /conversations/`)

- **Description**: Creates a new conversation between two users.
- **Body**: `members_conversation` model.
- **Response**: JSON with status code, message, and conversation ID.
- **Errors**:
  - `404` if any user does not exist.
  - `400` if the conversation already exists.

#### Retrieve Conversations (`POST /conversations/retrieve/`)

- **Description**: Retrieves all conversations for a user.
- **Body**: `RetrieveConversationsRequest` model.
- **Response**: JSON with status code, message, number of conversations, and conversation details.
- **Errors**:
  - `404` if the user does not exist.

### Message Handling

#### Add Message (`POST /messages/`)

- **Description**: Adds a message to an existing conversation.
- **Body**: `message` model.
- **Response**: JSON with status code and message.
- **Errors**:
  - `404` if the user or conversation does not exist.

#### Retrieve Messages (`POST /messages/retrieve/`)

- **Description**: Retrieves all messages from a conversation.
- **Body**: `RetrieveMessagesRequest` model.
- **Response**: JSON with status code, message, and messages data.
- **Errors**:
  - `404` if the conversation does not exist.

## Data Models

### `User`

- Represents a user with fields for ID, password, name, surname, birthdate, and gender.

### `UserUpdate`

- Used for updating user information, excluding the password and profile picture.

### `UserDelete`

- Represents a simple model with an `id` field for user deletion.

### `LoginData`

- Contains `id` and `password` fields for user authentication.

### `members_conversation`

- Defines the members of a conversation with `id_usuario1` and `id_usuario2`.

### `message`

- Represents a message within a conversation, including sender ID, message content, and whether it's a file.

### `RetrieveConversationsRequest`

- Contains a single `user_id` field to specify the user whose conversations to retrieve.

## Additional Features

- **CORS Middleware**: Allows cross-origin requests from any source.
- **GridFS**: Used for storing and retrieving large files, such as profile pictures and file messages.
- **Password Hashing**: Utilizes bcrypt for secure password storage and verification.

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

This documentation provides an overview of your FastAPI application's endpoints, models, and functionalities. It's essential to maintain and update this documentation as your project evolves.