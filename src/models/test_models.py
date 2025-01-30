from pydantic import BaseModel


class TestCase(BaseModel):
    prompt: str
    should_pass: bool


class TestResult(BaseModel):
    prompt: str
    should_pass: bool
    llm_response: str
    passed_judgment: bool | None = None
