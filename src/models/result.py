from pydantic import BaseModel


class Result(BaseModel):
    prompt: str
    should_pass: bool
    llm_response: str
