from pydantic import BaseModel


class TestCase(BaseModel):
    prompt: str
