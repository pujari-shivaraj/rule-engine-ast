from typing import Any, Dict
from app.utils.ast_utils import Node, tokenize, build_ast, evaluate_node
from app.db.database import get_rules_collection

import logging
from fastapi import HTTPException

# Initialize logger
logger = logging.getLogger("rule_engine")

def build_node_from_dict(node_dict: Dict[str, Any]) -> Node:
    """Recursively constructs a Node object from a dictionary."""
    if node_dict is None:
        return None
    
    node_type = node_dict.get("type")
    left = build_node_from_dict(node_dict.get("left")) if node_dict.get("left") else None
    right = build_node_from_dict(node_dict.get("right")) if node_dict.get("right") else None
    value = node_dict.get("value")
    
    return Node(node_type, left=left, right=right, value=value)




async def create_rule_service(rule_string: str):
    """
    Service to create a new rule.
    :param rule_string: The string representation of the rule.
    :return: The inserted rule's ID.
    """
    try:
        # Tokenize and build AST from the rule string
        tokens = tokenize(rule_string)
        ast = build_ast(tokens)
        rule_data = {"rule_string": rule_string, "ast": ast.to_dict()}

        # Access the 'rules' collection
        rules_collection = await get_rules_collection()

        # Insert the rule into the collection
        result = await rules_collection.insert_one(rule_data)
        return str(result.inserted_id)

    except Exception as e:
        logger.error(f"Error creating rule: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create rule")




def evaluate_rule_service(data: Dict[str, Any]) -> bool:
    """
    Evaluates the given JSON data containing the AST and user attributes.
    
    :param data: A dictionary containing 'ast' for the AST rule and user attributes.
    :return: True if the rule evaluates to True for the user data, False otherwise.
    """
    try:
        ast_dict = data.get("ast")
        user_data = data.get("user_data")

        if not ast_dict:
            logging.error("AST not provided in JSON data")
            raise ValueError("AST is required in the JSON data")
        if not user_data:
            logging.error("User data not provided in JSON data")
            raise ValueError("User data is required in the JSON data")

        logging.info(f"Evaluating rule with AST: {ast_dict} and user data: {user_data}")
        
        # Convert ast_dict to a Node object using the helper function
        ast_node = build_node_from_dict(ast_dict)

        # Use evaluate_node to evaluate the AST
        result = evaluate_node(ast_node, user_data)
        logging.info(f"Evaluation result: {result}")
        return bool(result)

    except KeyError as e:
        logger.error(f"Missing required field in user_data: {e}")
        raise ValueError(f"Missing required field: {str(e)}")
    except ValueError as e:
        logger.error(f"Value error during evaluation: {str(e)}")
        raise ValueError(f"Value error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error occurred during rule evaluation: {str(e)}")
        raise ValueError(f"Error evaluating rule: {str(e)}")




async def combine_rules_service(rules: list):
    """
    Service to combine multiple rules into one using OR operator.
    :param rules: A list of rule strings to combine.
    :return: The inserted combined rule's ID.
    """
    try:
        combined_tokens = []
        for rule in rules:
            tokens = tokenize(rule)
            combined_tokens.extend(tokens + ["OR"])

        combined_tokens.pop()  # Remove the last unnecessary OR

        # Build the combined AST
        combined_ast = build_ast(combined_tokens)
        combined_rule_data = {
            "rule_string": " OR ".join(rules),
            "ast": combined_ast.to_dict()  # Convert to dict here
        }

        # Access the 'rules' collection
        rules_collection = await get_rules_collection()

        # Insert the combined rule into the collection
        result = await rules_collection.insert_one(combined_rule_data)
        return str(result.inserted_id)

    except Exception as e:
        logger.error(f"Error combining rules: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to combine rules")
