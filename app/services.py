from http import HTTPStatus
from fastapi import HTTPException
from app.repositories import StudentRepository, GroupRepository
from app.schemas import StudentCreate, GroupCreate
from sqlalchemy.ext.asyncio import AsyncSession


class StudentService:
    @staticmethod
    async def create(db: AsyncSession, data: StudentCreate):
        return await StudentRepository.create(db, data.name, data.age)

    @staticmethod
    async def get_all(db: AsyncSession):
        return await StudentRepository.get_all(db)

    @staticmethod
    async def get_by_id(db: AsyncSession, student_id: int):
        student = await StudentRepository.get_by_id(db, student_id)
        if not student:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Student not found")
        return student

    @staticmethod
    async def delete(db: AsyncSession, student_id: int):
        student = await StudentService.get_by_id(db, student_id)
        await StudentRepository.delete(db, student)
        return {"message": "Student deleted"}

    @staticmethod
    async def add_to_group(db: AsyncSession, student_id: int, group_id: int):
        student = await StudentService.get_by_id(db, student_id)
        group = await GroupService.get_by_id(db, group_id)
        if not group:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Group not found")

        if student.group_id == group_id:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Student already in this group")
        if student.group_id is not None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Student already in another group")

        await StudentRepository.add_to_group(db, student, group_id)
        return {"message": "Student added to group"}

    @staticmethod
    async def remove_from_group(db: AsyncSession, student_id: int):
        student = await StudentService.get_by_id(db, student_id)
        if student.group_id is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Student not in any group")

        await StudentRepository.remove_from_group(db, student)
        return {"message": "Student removed from group"}


class GroupService:
    @staticmethod
    async def create(db: AsyncSession, data: GroupCreate):
        return await GroupRepository.create(db, data.name)

    @staticmethod
    async def get_all(db: AsyncSession):
        return await GroupRepository.get_all(db)

    @staticmethod
    async def get_by_id(db: AsyncSession, group_id: int):
        group = await GroupRepository.get_by_id(db, group_id)
        if not group:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Group not found")
        return group

    @staticmethod
    async def delete(db: AsyncSession, group_id: int):
        group = await GroupService.get_by_id(db, group_id)
        await GroupRepository.delete(db, group)
        return {"message": "Group deleted"}

    @staticmethod
    async def get_students(db: AsyncSession, group_id: int):
        return await GroupRepository.get_students(db, group_id)

    @staticmethod
    async def transfer_student(db: AsyncSession, student_id: int, source_group_id: int, target_group_id: int):
        student = await StudentService.get_by_id(db, student_id)

        if student.group_id != source_group_id:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Student not in source group")

        await GroupRepository.transfer_student(db, student, target_group_id)
        return {"message": "Student transferred"}