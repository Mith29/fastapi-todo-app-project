from fastapi import FastAPI, Depends, HTTPException
from schemas import TodoResponse, TodoRequest
from sqlalchemy.orm import session
from database import SessionLocal, Base, engine
from models import Todo

Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# POST - create TODO
@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoRequest, db: session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# GET -alL tODOS
@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: session = Depends(get_db)):
    return db.query(Todo).all()


# GET- get single todo
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found!")
    return todo


# PUT - up;date todo
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updated: TodoRequest, db: session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found!")
    for key, value in updated.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


# DELETE- delete a todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found!")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully!"}
