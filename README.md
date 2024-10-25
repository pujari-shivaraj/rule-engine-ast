# Rule Engine API

## Features
- Rule Management: Create and combine rules with customizable conditions
- User Evaluation: Evaluate user eligibility based on defined rules.
- AST-Based Processing: Efficiently parses and evaluates rules using an Abstract Syntax Tree.
- Docker Support: The application is containerized for easy setup and deployment.


## Setup Instructions

### Prerequisite
- Docker (required for containerized deployment)
- Docker Compose (optional, if you choose to use it for managing containers)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YOUR_GITHUB_HANDLE/rule-engine-api.git
   cd rule-engine-api

2. **Build the Docker image:**:
    docker-compose build

3. **Build the Docker image:**:
    docker-compose up

4. **Build the Docker image:**:
    http://localhost:8000
    
    http://localhost:8000/docs



   **  API Endpoints :**
     POST /rules: Create a new rule.
     POST /rules/evaluate: Evaluate user eligibility based on a rule.
     POST /rules/combine: Combine multiple rules into a single rule.


    
## Creating a Rule

To create a rule, send a POST request to the `/rules` endpoint with the following JSON body:

### Request
- **Request Type**: `POST`
- **URL**: `http://localhost:8000/rules`
- **Body**:
    ```json
    {
        "rule_string": "(age > 30 AND department = 'Sales') OR (salary < 50000)"
    }
    ```

## Evaluating a Rule

To evaluate a rule, send a POST request to the `/rules/evaluate` endpoint with the following JSON body:

### Request
- **Request Type**: `POST`
- **URL**: `http://localhost:8000/rules/evaluate`
- **Body**:
    ```json
    {
        "ast": {
            "type": "operator",
            "left": {
                "type": "operand",
                "value": {
                    "attribute": "age",
                    "operator": ">",
                    "value": "30"
                }
            },
            "right": {
                "type": "operand",
                "value": {
                    "attribute": "department",
                    "operator": "=",
                    "value": "Sales"
                }
            }
        },
        "user_data": {
            "age": 35,
            "department": "Sales",
            "salary": 40000
        }
    }
    ```

## Combining Rules

To combine rules, send a POST request to the `/rules/combine` endpoint with an array of rule IDs.

### Request
- **Request Type**: `POST`
- **URL**: `http://localhost:8000/rules/combine`
- **Body**:
    ```json
    [
        "rule_id_1",
        "rule_id_2"
    ]
    ```

## Example Requests in Postman

### Create a Rule
1. **Click** the **Send** button to send your request to the API.
2. **View** the response received from the server in the section below. You can view the status code, response body, and headers.

### Evaluate a Rule
1. **Click** the **Send** button to send your request to the API.
2. **View** the response received from the server in the section below. You can view the status code, response body, and headers.

### Combine Rules
1. **Click** the **Send** button to send your request to the API.
2. **View** the response received from the server in the section below. You can view the status code, response body, and headers.
