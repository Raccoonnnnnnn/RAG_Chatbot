from pydantic import BaseModel


class DeleteRequest(BaseModel):
    doc_id: str