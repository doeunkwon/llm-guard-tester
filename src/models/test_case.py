from pydantic import BaseModel
from typing import Optional


class TestCaseInput(BaseModel):
    """Model for creating a new test case"""
    test_name: str
    prompt: str
    offender_model: str
    enhanced: bool = False


class TestCase(BaseModel):
    """Model for test cases retrieved from the database"""
    id: int
    test_name: str
    prompt: str
    offender_model: str
    enhanced: bool = False
