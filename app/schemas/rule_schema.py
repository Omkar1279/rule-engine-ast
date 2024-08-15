from pydantic import BaseModel


class RuleBase(BaseModel):
    rule_string: str


class RuleCreate(RuleBase):
    pass


class RuleUpdate(RuleBase):
    pass


class RuleInDB(RuleBase):
    id: int
    ast: str

    class Config:
        from_attributes = True


class RuleEvaluate(BaseModel):
    rule_id: int
    data: dict


class RuleList(BaseModel):
    id: int
    rule_string: str


class RuleDelete(BaseModel):
    message: str
