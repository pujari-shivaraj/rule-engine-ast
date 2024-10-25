import logging
import re
from typing import List, Dict, Any,Tuple

from fastapi import logger


logger = logging.getLogger("rule_engine")
logger.setLevel(logging.INFO)

# Configure logging format and output (e.g., console output)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class Node:
    def __init__(self, node_type: str, left=None, right=None, value=None):
        self.type = node_type 
        self.left = left
        self.right = right
        self.value = value
    
    def to_dict(self):
        # Convert Node to a serializable dictionary
        return {
            "type": self.type,  # 'type' maps to the 'node_type' in __init__
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }



# Tokenizer for rule strings
def tokenize(rule_string: str) -> List[str]:
    token_pattern = r"\(|\)|AND|OR|>|<|=|[\w']+"
    return re.findall(token_pattern, rule_string)



# Builds an AST from tokens
def build_ast(tokens: List[str]) -> Node:
    def parse_expression(tokens: List[str], index: int = 0) -> Tuple[Node, int]:
        node_stack = []
        operator_stack = []

        def apply_operator():
            right = node_stack.pop()
            left = node_stack.pop()
            operator = operator_stack.pop()
            node_stack.append(Node("operator", left, right, operator))

        while index < len(tokens):
            token = tokens[index]
            if token == '(':
                sub_node, index = parse_expression(tokens, index + 1)
                node_stack.append(sub_node)
            elif token == ')':
                break
            elif token in {"AND", "OR"}:
                while (operator_stack and operator_stack[-1] == "AND" and token == "OR"):
                    apply_operator()
                operator_stack.append(token)
            elif token in {">", "<", "="}:
                left_operand = node_stack.pop()
                right_operand = tokens[index + 1]
                node_stack.append(Node("operand", None, None, {"attribute": left_operand, "operator": token, "value": right_operand}))
                index += 1
            else:
                node_stack.append(token)
            index += 1

        while operator_stack:
            apply_operator()

        return node_stack[0], index

    ast_root, _ = parse_expression(tokens)
    return ast_root




# Evaluates an AST
def evaluate_node(node: Node, data: Dict[str, Any]) -> bool:
    try:
        logger.info(f"Evaluating node: {node.to_dict()}, with data: {data}")
        
        if node.type == "operator":
            left_val = evaluate_node(node.left, data)
            right_val = evaluate_node(node.right, data)
            logger.info(f"Evaluated left: {left_val}, right: {right_val} for operator {node.value}")

            if node.value == "AND":
                return left_val and right_val
            elif node.value == "OR":
                return left_val or right_val

        if node.type == "operand":
            attribute = node.value["attribute"]
            operator = node.value["operator"]
            value = node.value["value"]

            if attribute not in data:
                logger.error(f"Attribute '{attribute}' not found in user_data: {data}")
                raise ValueError(f"Attribute '{attribute}' not found in user_data.")

            data_value = data[attribute]
            logger.info(f"Comparing data_value: {data_value} with value: {value} using operator: {operator}")

            try:
                if operator == ">":
                    return float(data_value) > float(value)
                elif operator == "<":
                    return float(data_value) < float(value)
                elif operator == "=":
                    return str(data_value) == str(value)
            except ValueError as e:
                logger.error(f"Error in comparison: {e}")
                raise ValueError(f"Error comparing values: {data_value} {operator} {value}")

    except Exception as ex:
        logger.error(f"Error while evaluating node: {ex}")
        raise ValueError("Evaluation failed due to unexpected error")

    logger.error("Invalid node type or structure")
    raise ValueError("Invalid node type or structure")





if __name__ == "__main__":
    rule = "(age > 30 AND department = 'Sales') OR (salary < 50000)"
    tokens = tokenize(rule)
    print(f"Tokens: {tokens}")

    try:
        ast = build_ast(tokens)
        print(f"AST: {ast.to_dict()}")  # Make sure AST is converted to a dictionary

        # Test evaluation
        user_data = {"age": 35, "department": "Sales", "salary": 40000}
        result = evaluate_node(ast, user_data)
        print(f"Evaluation Result: {result}")

    except Exception as e:
        print(f"Error during testing: {e}")


