import logging
from fastapi import APIRouter, HTTPException, logger
from app.models.rule_models import RuleCreateRequest, RuleEvaluateRequest, RuleResponse, EvaluationResponse
from app.services.rule_service import create_rule_service, evaluate_rule_service, combine_rules_service

router = APIRouter()


logger = logging.getLogger("rule_engine")
logger.setLevel(logging.INFO)


@router.post("/rules", response_model=RuleResponse)
async def create_rule(rule_request: RuleCreateRequest):
    try:
        rule_id = await create_rule_service(rule_request.rule_string)
        return RuleResponse(rule_id=rule_id)
    except ValueError as e:
        # Handle validation errors (e.g., invalid rule format)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log the error and return a 500 status for internal server errors
        raise HTTPException(status_code=500, detail="Failed to create rule")



@router.post("/rules/evaluate", response_model=EvaluationResponse)
async def evaluate_rule(evaluate_request: RuleEvaluateRequest):
    try:
        logger.info(f"Received evaluate request: {evaluate_request.dict()}")

        # Call the evaluate_rule function with JSON data
        is_eligible = evaluate_rule_service(evaluate_request.dict())

        logger.info(f"Evaluation result: {is_eligible}")
        return EvaluationResponse(is_eligible=is_eligible)

    except ValueError as e:
        logger.error(f"ValueError during evaluation: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except KeyError as e:
        logger.error(f"KeyError: Missing required field in user_data: {e}")
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        logger.exception("Unexpected error occurred during rule evaluation")
        raise HTTPException(status_code=500, detail="Error evaluating rule")




@router.post("/rules/combine", response_model=RuleResponse)
async def combine_rules(rules: list):
    try:
        rule_id = await combine_rules_service(rules)
        return RuleResponse(rule_id=rule_id)
    except ValueError as e:
        # Handle invalid rule formats
        raise HTTPException(status_code=400, detail="Invalid rule format")
    except Exception as e:
        # Catch unexpected errors
        raise HTTPException(status_code=500, detail="Failed to combine rules")
