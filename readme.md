# Recipe API

A simple API for managing recipes, ratings, and comments. 

---

## Features
- **Authentication**
  - Register and login
- **Recipes**
  - Add, update, retrieve, and delete recipes.
- **Ratings**
  - Rate recipes (1-5 stars).
- **Comments**
  - Add and retrieve comments for recipes.


---

## Technologies Used
- **Framework**: Flask
- **Database**: MSSQL
- **Containerization**: Docker
- **Dependencies**: Python libraries listed in `requirements.txt`

---

## Getting Started

### Prerequisites
1. Install **Docker** and **Docker Compose**:
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

2. Clone the repository:
   ```bash
   git clone <repo-url-here>
   cd recipe_api
   ```

---

## Running the application
1. Run and Start Containers
   ```bash
    docker-compose up --build
   ```
   
   This will:

   - Build the API Container    
   - Build the DB Container & Set it up
   - Start the API at localhost port 5000

2. Verify API

    - Open your browser or client (e.g Postman).
    - Run healthcheck at: http://localhost:5000/health
        - should output something like this
            ```json
            { "healthy": true }
            ``` 
3. Stopping the application
    ```bash
    docker-compose down
    ```

---

## API Endpoints

### Authentication Endpoints
These endpoints allow user registration and login.

- **POST /auth/register**
  - Registers a new user.
  - **Request Body**:
    ```json
    {
      "username": "username",
      "password": "password"
    }
    ```
  - **Responses**:
    - **201 Created**: User successfully registered.
    - **400 Bad Request**: Missing or invalid input.

- **POST /auth/login**
  - Logs in a user and generates an **access token**.
  - **Request Body**:
    ```json
    {
      "username": "username",
      "password": "password"
    }
    ```
  - **Responses**:
    - **200 OK**: Returns the access token.
    - **401 Unauthorized**: Invalid credentials.

---

### Recipe Endpoints
Endpoints for managing recipes.  
**JWT authentication required** for creating, updating, and deleting recipes.

- **POST /recipes/**
  - Adds a new recipe.
  - **Authentication**: Requires a valid JWT in the `Authorization` header.
    ```
    Authorization: Bearer <your-token>
    ```
  - **Request Body**:
    ```json
    {
      "name": "Recipe name",
      "ingredients": [
        {
          "ingredient": "ingredient",
          "quantity": "quantity",
          "unit": "unit"
        }
      ],
      "steps": ["Step 1", "Step 2", "Step 3"],
      "prep_time": 20
    }
    ```
  - **Responses**:
    - **201 Created**: Recipe successfully added.
    - **400 Bad Request**: Missing or invalid fields.
    - **500 Internal Server Error**: If something goes wrong.

- **GET /recipes/**
  - Retrieves all recipes (sorted by most recent).
  - **Responses**:
    - **200 OK**: Returns a list of recipes.

- **GET /recipes/{id}/**
  - Retrieves a recipe by its ID.
  - **Responses**:
    - **200 OK**: Returns the recipe details.
    - **404 Not Found**: If the recipe does not exist.

- **PUT /recipes/{id}/**
  - **Authentication**: Requires a valid JWT.
    ```
    Authorization: Bearer <your-token>
    ```
  - Updates a recipe by its ID.
  - **Request Body**: Same as **POST /recipes/**.
  - **Responses**:
    - **200 OK**: Recipe successfully updated.
    - **403 Forbidden**: User does not have permission to update the recipe.
    - **404 Not Found**: If the recipe does not exist.
    - **400 Bad Request**: Missing or invalid fields.

- **DELETE /recipes/{id}/**
  - **Authentication**: Requires a valid JWT.
    ```
    Authorization: Bearer <your-token>
    ```
  - Deletes a recipe by its ID.
  - **Responses**:
    - **200 OK**: Recipe successfully deleted.
    - **403 Forbidden**: User does not have permission to delete the recipe.
    - **404 Not Found**: If the recipe does not exist.

---

### Rating Endpoints
Endpoints for rating recipes.  
**JWT authentication required** to rate a recipe.

- **POST /recipes/{id}/ratings/**
  - **Authentication**: Requires a valid JWT.
    ```
    Authorization: Bearer <your-token>
    ```
  - Adds a rating (1-5) to a recipe.
  - **Request Body**:
    ```json
    {
      "rating": 5
    }
    ```
  - **Responses**:
    - **201 Created**: Rating successfully submitted.
    - **400 Bad Request**: Missing or invalid fields.
    - **404 Not Found**: If the recipe does not exist.

---

### Comment Endpoints
Endpoints for commenting on recipes.  
**JWT authentication required** to add a comment.

- **POST /recipes/{id}/comments/**
  - **Authentication**: Requires a valid JWT.
    ```
    Authorization: Bearer <your-token>
    ```
  - Adds a comment to a recipe.
  - **Request Body**:
    ```json
    {
      "comment": "This is a great recipe!"
    }
    ```
  - **Responses**:
    - **201 Created**: Comment successfully added.
    - **400 Bad Request**: Missing or invalid fields.
    - **404 Not Found**: If the recipe does not exist.

- **GET /recipes/{id}/comments/**
  - Retrieves all comments for a recipe.
  - **Responses**:
    - **200 OK**: Returns a list of comments.
    - **404 Not Found**: If the recipe does not exist.
