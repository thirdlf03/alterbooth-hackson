from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.orm import Session, joinedload
import bcrypt
from db import Base, engine, get_db
import model
import math
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

@app.post("/boards")
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    db_board = model.Board(user_id=board.user_id, content=board.content)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

@app.get("/boards")
def read_boards(db: Session = Depends(get_db)):
    boards = db.query(model.Board).options(joinedload(model.Board.user)).order_by(model.Board.created_at.desc()).all()
    return [{"username": board.user.name, "content": board.content} for board in boards]

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
    user_quests = db.query(model.UserQuest).filter(model.UserQuest.user_id == user_id).all()
    if not user_quests:
        return db.query(model.Quest).all()
    return db.query(model.Quest).filter(~model.Quest.id.in_(db.query(model.UserQuest.quest_id).filter(model.UserQuest.user_id == user_id))).all()

@app.get("/quests")
def read_all_quests(db: Session = Depends(get_db)):
    return db.query(model.Quest).all()

@app.get("/checkquests/{user_id}")
def check_quests(user_id: int, db: Session = Depends(get_db)):
    # Check if the user has at least 3 tasks
    task_count = db.query(model.Task).filter(model.Task.user_id == user_id).count()
    has_three_tasks = task_count >= 3

    # Check if the user has at least 3 completed tasks
    completed_task_count = db.query(model.Task).filter(model.Task.user_id == user_id, model.Task.is_done == True).count()
    has_three_completed_tasks = completed_task_count >= 3

    # Check if the user has at least one message on the board
    board_message_count = db.query(model.Board).filter(model.Board.user_id == user_id).count()
    has_board_message = board_message_count > 0

    # Record the completion status in the user_quests table and update user points
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if has_three_tasks:
        existing_quest = db.query(model.UserQuest).filter(model.UserQuest.user_id == user_id, model.UserQuest.quest_id == 1).first()
        if not existing_quest:
            db_user_quest = model.UserQuest(user_id=user_id, quest_id=1, is_done=True)
            db.add(db_user_quest)
            user.point += 100

    if has_three_completed_tasks:
        existing_quest = db.query(model.UserQuest).filter(model.UserQuest.user_id == user_id, model.UserQuest.quest_id == 2).first()
        if not existing_quest:
            db_user_quest = model.UserQuest(user_id=user_id, quest_id=2, is_done=True)
            db.add(db_user_quest)
            user.point += 100

    if has_board_message:
        existing_quest = db.query(model.UserQuest).filter(model.UserQuest.user_id == user_id, model.UserQuest.quest_id == 3).first()
        if not existing_quest:
            db_user_quest = model.UserQuest(user_id=user_id, quest_id=3, is_done=True)
            db.add(db_user_quest)
            user.point += 100

    db.commit()

    return {
        "has_three_tasks": has_three_tasks,
        "has_three_completed_tasks": has_three_completed_tasks,
        "has_board_message": has_board_message
    }

@app.get("/rate/{user_id}")
def rate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_tasks = db.query(model.Task).filter(model.Task.user_id == user_id).count()
    completed_tasks = db.query(model.Task).filter(model.Task.user_id == user_id, model.Task.is_done == True).count()

    if total_tasks == 0:
        completion_percentage = 0
    else:
        completion_percentage = math.floor((completed_tasks / total_tasks) * 100)

    db.commit()

    return {
        "completion_percentage": completion_percentage
    }

@app.get("/rate")
def rate_overall(db: Session = Depends(get_db)):
    total_tasks = db.query(model.Task).count()
    completed_tasks = db.query(model.Task).filter(model.Task.is_done == True).count()

    if total_tasks == 0:
        completion_percentage = 0
    else:
        completion_percentage = math.floor((completed_tasks / total_tasks) * 100)

    return {
        "completion_percentage": completion_percentage
    }

@app.post("/init")
def init(db: Session = Depends(get_db)):
    quests = [
        {"title": "Quest 1", "content": "目標を3つ設定しよう"},
        {"title": "Quest 2", "content": "目標を3つ完了しよう"},
        {"title": "Quest 3", "content": "掲示板にメッセージを投稿しよう"}
    ]

    for quest in quests:
        existing_quest = db.query(model.Quest).filter_by(title=quest["title"]).first()
        if not existing_quest:
            db_quest = model.Quest(title=quest["title"], content=quest["content"])
            db.add(db_quest)

    db.commit()
    return {"message": "Initialization complete"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
