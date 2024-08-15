from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.rule_schema import RuleCreate, RuleUpdate, RuleEvaluate, RuleList, RuleDelete
from app.services.rule_service import RuleService

router = APIRouter()


# Create a new rule
@router.post("/rules/create")
async def create_rule(rule: RuleCreate, session: AsyncSession = Depends(get_session)):
    rule_service = RuleService(session)
    return await rule_service.create_rule(rule)


# Combine multiple rules by IDs
@router.post("/rules/combine")
async def combine_rules(rule_ids: List[int], session: AsyncSession = Depends(get_session)):
    rule_service = RuleService(session)
    return await rule_service.combine_rules(rule_ids)


# Evaluate a specific rule
@router.post("/rules/evaluate")
async def evaluate_rule(rule_eval: RuleEvaluate, session: AsyncSession = Depends(get_session)):
    rule_service = RuleService(session)
    return await rule_service.evaluate_rule(rule_eval.rule_id, rule_eval.data)


# Modify a rule by ID
@router.put("/rules/{rule_id}/modify")
async def modify_rule(rule_id: int, rule: RuleUpdate, session: AsyncSession = Depends(get_session)):
    rule_service = RuleService(session)
    return await rule_service.modify_rule(rule_id, rule)


# Get a list of all rules
@router.get("/rules/list", response_model=List[RuleList])
async def get_rules(session: AsyncSession = Depends(get_session)):
    rule_service = RuleService(session)
    return await rule_service.get_all_rules()


# Delete a specific rule by ID or delete all rules
@router.delete("/rules/{rule_id}/delete", response_model=RuleDelete)
async def delete_rule(rule_id: int, session: AsyncSession = Depends(get_session)):
    rule_service = RuleService(session)
    try:
        return await rule_service.delete_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/rules/delete_all", response_model=RuleDelete)
async def delete_all_rules(session: AsyncSession = Depends(get_session)):
    rule_service = RuleService(session)
    return await rule_service.delete_all_rules()
