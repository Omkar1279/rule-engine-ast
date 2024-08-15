from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rule import Rule
from app.schemas.rule_schema import RuleCreate, RuleUpdate
from app.services.ast_service import ASTService


class RuleService:
    """
    Service class for managing rules in the database.

    This class provides methods for creating, modifying, combining, evaluating,
    and deleting rules. Each rule is associated with an Abstract Syntax Tree (AST)
    that is used for evaluating the rule against provided data.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the RuleService with an asynchronous database session.

        Args:
            session (AsyncSession): The async database session to be used for
            database operations.
        """
        self.session = session
        self.ast_service = ASTService()

    async def create_rule(self, rule: RuleCreate):
        """
        Create a new rule in the database.

        Args:
            rule (RuleCreate): The rule data to be created.

        Returns:
            Rule: The newly created Rule object.
        """
        ast = self.ast_service.parse_rule_string(rule.rule_string)
        db_rule = Rule(rule_string=rule.rule_string, ast=ast)
        self.session.add(db_rule)
        await self.session.commit()
        await self.session.refresh(db_rule)
        return db_rule

    async def combine_rules(self, rule_ids: List[int]):
        """
        Combine multiple rules into a single rule.

        Args:
            rule_ids (List[int]): The list of rule IDs to be combined.

        Returns:
            Rule: The newly created combined Rule object.
        """
        query = select(Rule).where(Rule.id.in_(rule_ids))
        result = await self.session.execute(query)
        rules = result.scalars().all()

        combined_ast = self.ast_service.combine_asts([rule.ast for rule in rules])
        combined_rule_string = " AND ".join([rule.rule_string for rule in rules])

        db_rule = Rule(rule_string=combined_rule_string, ast=combined_ast)
        self.session.add(db_rule)
        await self.session.commit()
        await self.session.refresh(db_rule)

        return db_rule

    async def evaluate_rule(self, rule_id: int, data: dict):
        """
        Evaluate a rule against provided data.

        Args:
            rule_id (int): The ID of the rule to be evaluated.
            data (dict): The data against which the rule is to be evaluated.

        Returns:
            dict: The result of the rule evaluation.
        """
        query = select(Rule).filter(Rule.id == rule_id)
        result = await self.session.execute(query)
        rule = result.scalars().first()

        if not rule:
            raise ValueError("Rule not found")

        result = self.ast_service.evaluate_ast(rule.ast, data)
        return {"result": result}

    async def modify_rule(self, rule_id: int, rule: RuleUpdate):
        """
        Modify an existing rule in the database.

        Args:
            rule_id (int): The ID of the rule to be modified.
            rule (RuleUpdate): The updated rule data.

        Returns:
            Rule: The modified Rule object.
        """
        query = select(Rule).filter(Rule.id == rule_id)
        result = await self.session.execute(query)
        db_rule = result.scalars().first()

        if not db_rule:
            raise ValueError("Rule not found")

        db_rule.rule_string = rule.rule_string
        db_rule.ast = self.ast_service.parse_rule_string(rule.rule_string)
        await self.session.commit()
        return db_rule

    async def get_all_rules(self):
        """
        Retrieve all rules from the database.

        Returns:
            List[dict]: A list of dictionaries containing rule IDs and rule strings.
        """
        query = select(Rule)
        result = await self.session.execute(query)
        rules = result.scalars().all()
        return [{"id": rule.id, "rule_string": rule.rule_string} for rule in rules]

    async def delete_rule(self, rule_id: int):
        """
        Delete a rule from the database.

        Args:
            rule_id (int): The ID of the rule to be deleted.

        Returns:
            dict: A message indicating the deletion status.
        """
        query = delete(Rule).where(Rule.id == rule_id)
        result = await self.session.execute(query)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Rule with id {rule_id} not found")
        return {"message": f"Rule with id {rule_id} deleted successfully"}

    async def delete_all_rules(self):
        """
        Delete all rules from the database.

        Returns:
            dict: A message indicating the number of rules deleted.
        """
        query = delete(Rule)
        result = await self.session.execute(query)
        await self.session.commit()
        return {"message": f"{result.rowcount} rules deleted successfully"}
