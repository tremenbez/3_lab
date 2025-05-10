# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session, init_db
from app.schemas import StudentCreate, StudentResponse, GroupCreate, GroupResponse
from app.services import StudentService, GroupService
from typing import List
from http import HTTPStatus

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


# === STUDENTS ===

@app.post("/students/", response_model=StudentResponse)
async def create_student(student: StudentCreate, session: AsyncSession = Depends(get_session)):
    return await StudentService.create(session, student)


@app.get("/students/", response_model=List[StudentResponse])
async def get_students(session: AsyncSession = Depends(get_session)):
    return await StudentService.get_all(session)


@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)):
    return await StudentService.get_by_id(session, student_id)


@app.delete("/students/{student_id}")
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)):
    return await StudentService.delete(session, student_id)


@app.post("/groups/{group_id}/add_student/{student_id}")
async def add_student_to_group(group_id: int, student_id: int, session: AsyncSession = Depends(get_session)):
    return await StudentService.add_to_group(session, student_id, group_id)


@app.delete("/groups/{group_id}/remove_student/{student_id}")
async def remove_student_from_group(group_id: int, student_id: int, session: AsyncSession = Depends(get_session)):
    return await StudentService.remove_from_group(session, student_id)


# === GROUPS ===

@app.post("/groups/", response_model=GroupResponse)
async def create_group(group: GroupCreate, session: AsyncSession = Depends(get_session)):
    return await GroupService.create(session, group)


@app.get("/groups/", response_model=List[GroupResponse])
async def get_groups(session: AsyncSession = Depends(get_session)):
    return await GroupService.get_all(session)


@app.get("/groups/{group_id}", response_model=GroupResponse)
async def get_group(group_id: int, session: AsyncSession = Depends(get_session)):
    return await GroupService.get_by_id(session, group_id)


@app.delete("/groups/{group_id}")
async def delete_group(group_id: int, session: AsyncSession = Depends(get_session)):
    return await GroupService.delete(session, group_id)


@app.get("/groups/{group_id}/students", response_model=List[StudentResponse])
async def get_students_in_group(group_id: int, session: AsyncSession = Depends(get_session)):
    return await GroupService.get_students(session, group_id)


@app.post("/transfer_student/{student_id}/from/{group_a_id}/to/{group_b_id}")
async def transfer_student(student_id: int, group_a_id: int, group_b_id: int, session: AsyncSession = Depends(get_session)):
    return await GroupService.transfer_student(session, student_id, group_a_id, group_b_id)