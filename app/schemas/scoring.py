from datetime import date
from typing import List

from pydantic import BaseModel, Field


class Loan(BaseModel):
    amount: int
    date: date
    flag: bool


class Score(BaseModel):
    income_level: int = Field(description='уровень дохода')
    loan_history: List[Loan] = Field(description='история займов: сумма, дата, флаг закрытия')
