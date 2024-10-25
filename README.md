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


    For Creating a Rule, enter:
json
Copy code
{
    "rule_string": "(age > 30 AND department = 'Sales') OR (salary < 50000)"
}
For Evaluating a Rule, enter:
json
Copy code
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
For Combining Rules, enter:
json
Copy code
[
    "rule_id_1",
    "rule_id_2"
]
Send the Request:

Click the Send button to send your request to the API.
View the Response:

Postman will display the response received from the server in the section below. You can view the status code, response body, and headers.
Example Requests in Postman
Create a Rule:

Request Type: POST
URL: http://localhost:8000/rules
Body:
json
Copy code
{
    "rule_string": "(age > 30 AND department = 'Sales') OR (salary < 50000)"
}
Evaluate a Rule:

Request Type: POST
URL: http://localhost:8000/rules/evaluate
Body:
json
Copy code
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
Combine Rules:

Request Type: POST
URL: http://localhost:8000/rules/combine
Body:
json
Copy code
[
    "rule_id_1",
    "rule_id_2"
]
