from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory store — this companion exists for tests, not production.
users: dict[int, dict] = {}
_next_id = 1


class UserIn(BaseModel):
    name: str
    email: str


@app.post("/api/users", status_code=201)
def create_user(payload: UserIn):
    global _next_id
    if not payload.name:
        raise HTTPException(
            status_code=400,
            detail={"code": "VALIDATION_ERROR", "details": ["name is required"]},
        )
    for user in users.values():
        if user["email"] == payload.email:
            raise HTTPException(
                status_code=409,
                detail={"code": "EMAIL_CONFLICT", "details": ["email already registered"]},
            )
    user = {"id": _next_id, "name": payload.name, "email": payload.email}
    users[_next_id] = user
    _next_id += 1
    return user


@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND"})
    return users[user_id]


@app.put("/api/users/{user_id}")
def update_user(user_id: int, payload: dict):
    if user_id not in users:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND"})
    users[user_id].update(payload)
    return users[user_id]


@app.delete("/api/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND"})
    del users[user_id]
