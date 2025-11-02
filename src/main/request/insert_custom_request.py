from pydantic import BaseModel


class InsertCustomRequest(BaseModel):
    path: str
    batch_size: int = 100