from pydantic import BaseModel
from typing import Dict, Any

class RuleCreateRequest(BaseModel):
    rule_string: str

class RuleEvaluateRequest(BaseModel):
    ast: Dict[str, Any]  # Include the AST representation of the rule
    user_data: Dict[str, Any]

class RuleResponse(BaseModel):
    rule_id: str

class EvaluationResponse(BaseModel):
    is_eligible: bool
