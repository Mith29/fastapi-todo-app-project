from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TodoRequest(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    class config:
        orm_mode = True
