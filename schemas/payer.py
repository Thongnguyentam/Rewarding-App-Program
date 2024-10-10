from pydantic import BaseModel


class NewPayerDTO(BaseModel):
    name: str