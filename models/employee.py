from pydantic import BaseModel, Field
from typing import Annotated


class Employee(BaseModel):
    employee_id: Annotated[str, Field(min_length=2, example="E123", description="Unique employee ID")]
    name: Annotated[str, Field(min_length=3, example="John Doe", description="Full name of the employee")]
    department: Annotated[str, Field(min_length=1, example="Engineering", description="Department name")]
    salary: Annotated[float, Field(gt=0, example=75000, description="Salary of the employee")]
    joining_date: Annotated[
        str,
        Field(pattern=r"^\d{4}-\d{2}-\d{2}$", example="2023-01-15", description="Joining date in YYYY-MM-DD format")
    ]
    skills: Annotated[list[str], Field(min_items=1, example=["Python", "MongoDB", "APIs"], description="List of skills")]
