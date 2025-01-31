from pydantic import BaseModel
from typing import Optional


class TestCase(BaseModel):
    """Model for test cases"""
    id: Optional[int] = None
    test_name: str
    prompt: str
    offender_model: str
    set_id: Optional[str] = None
    enhanced: Optional[bool] = False
    should_pass: Optional[bool] = None
    created_at: Optional[str] = None
