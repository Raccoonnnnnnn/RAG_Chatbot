from pydantic import BaseModel

class InsertRequest(BaseModel):
    content: str