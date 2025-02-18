from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.orm import Session
import bcrypt
from db import Base, engine, get_db
import model
from schemas import UserCreate, UserUpdate, User, UserProfile, UserPoint, TaskCreate, TaskUpdate, Task, BoardCreate, BoardUpdate, Board, UserResponse, UserQuest

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def read_root():
    return {"status": "UP"}

# User CRUD
@app.post("/users")
def create_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = model.User(email=user.email, password=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response.set_cookie(key="user_id", value=str(db_user.id))
    return db_user

@app.post("/login")
def login(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.email == user.email).first()
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    response.set_cookie(key="user_id", value=str(db_user.id))
    return db_user

@app.put("/profile")
def update_profile(user: UserProfile, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.icon = user.icon
    db_user.profile = user.profile
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.query(model.User).order_by(model.User.point.desc()).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

@app.post("/point")
def update_point(user: UserPoint, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.point += user.point
    db.commit()
    db.refresh(db_user)
    return db_user

# Task CRUD (Updated)
@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = model.Task(
        user_id=task.user_id,
        name=task.name,
        priority=task.priority,
        is_done=task.is_done
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}/done", response_model=Task)
def update_task_done(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.is_done = not db_task.is_done
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task

@app.get("/tasks/{user_id}", response_model=list[Task])
def read_tasks(user_id: int, db: Session = Depends(get_db)):
    return db.query(model.Task).filter(model.Task.user_id == user_id).all()

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# Board CRUD
@app.post("/boards", response_model=Board)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    db_board = Board(user_id=board.user_id, content=board.content)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

@app.get("/boards", response_model=list[Board])
def read_boards(db: Session = Depends(get_db)):
    return db.query(model.Board).all()

@app.put("/boards/{board_id}", response_model=Board)
def update_board(board_id: int, board: BoardUpdate, db: Session = Depends(get_db)):
    db_board = db.query(model.Board).filter(model.Board.id == board_id).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    for key, value in board.dict(exclude_unset=True).items():
        setattr(db_board, key, value)
    db.commit()
    db.refresh(db_board)
    return db_board

@app.delete("/boards/{board_id}", response_model=Board)
def delete_board(board_id: int, db: Session = Depends(get_db)):
    db_board = db.query(model.Board).filter(model.Board.id == board_id).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    db.delete(db_board)
    db.commit()
    return db_board

@app.get("/quests/{user_id}")
def read_quests(user_id: int, db: Session = Depends(get_db)):
    return db.query(model.UserQuest).join(model.Quest, model.UserQuest.quest_id == model.Quest.id).filter(model.UserQuest.user_id == user_id).all()





if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
