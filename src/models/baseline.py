from pydantic import BaseModel


class Baseline(BaseModel):
    prompt: str
    should_pass: bool
