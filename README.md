# Rule Engine API

## Overview

The Rule Engine API is a service designed to manage and evaluate business rules using an abstract syntax tree (AST). This API allows for the creation, modification, evaluation, combination, and deletion of rules. It is built with FastAPI and SQLAlchemy for asynchronous operations and uses a simple JSON-based AST representation.

## Project Structure

- `app/`: Contains the main application code.
  - `services/`: Contains business logic and AST processing services.
    - `ast_service.py`: Provides AST parsing, combination, and evaluation functionalities.
    - `rule_service.py`: Handles rule management operations.
  - `models/`: Defines the database schema.
    - `rule.py`: Contains the `Rule` model.
  - `core/`: Contains core application configurations and database setup.
    - `config.py`: Configuration settings.
    - `database.py`: Database session and engine setup.
  - `main.py`: Entry point for the application, sets up FastAPI and mounts static files.
  - `schemas/`: Contains Pydantic schemas for data validation.
    - `rule_schema.py`: Defines schemas for creating, updating, evaluating, and listing rules.
  - `api/`: Contains API routes and endpoint definitions.
    - `endpoints.py`: Defines the API endpoints for rule operations.

- `static/`: Directory for static files.
  - `index.html`: A static HTML file.
- `tests/`: Contains unit tests for the application.
  - `test_rule_engine.py`: Tests for the rule engine functionalities.
- `requirements.txt`: Lists the dependencies for the project.

## API Endpoints

### Create a New Rule

- **Endpoint**: `/api/rules/create`
- **Method**: `POST`
- **Request Body**: `RuleCreate` (rule_string: str)
- **Description**: Creates a new rule in the database.

### Combine Multiple Rules

- **Endpoint**: `/api/rules/combine`
- **Method**: `POST`
- **Request Body**: `List[int]` (list of rule IDs)
- **Description**: Combines multiple rules by IDs into a single rule.

### Evaluate a Specific Rule

- **Endpoint**: `/api/rules/evaluate`
- **Method**: `POST`
- **Request Body**: `RuleEvaluate` (rule_id: int, data: dict)
- **Description**: Evaluates a specific rule against the provided data.

### Modify a Rule

- **Endpoint**: `/api/rules/{rule_id}/modify`
- **Method**: `PUT`
- **Request Body**: `RuleUpdate` (rule_string: str)
- **Description**: Modifies an existing rule by ID.

### Get a List of All Rules

- **Endpoint**: `/api/rules/list`
- **Method**: `GET`
- **Response**: `List[RuleList]`
- **Description**: Retrieves a list of all rules.

### Delete a Specific Rule

- **Endpoint**: `/api/rules/{rule_id}/delete`
- **Method**: `DELETE`
- **Response**: `RuleDelete` (message: str)
- **Description**: Deletes a specific rule by ID.

### Delete All Rules

- **Endpoint**: `/api/rules/delete_all`
- **Method**: `DELETE`
- **Response**: `RuleDelete` (message: str)
- **Description**: Deletes all rules in the database.

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Omkar1279/rule-engine-ast.git
   ```

2. Navigate to the project directory:

   ```bash
   cd rule-engine-ast
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

5. Access the API at `http://localhost:8000`.

## Running Tests

To run the tests, use the following command:

```bash
pytest
```
