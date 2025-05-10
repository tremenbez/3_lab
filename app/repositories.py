from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Student, Group


class StudentRepository:
    @staticmethod
    async def create(db: AsyncSession, name: str, age: int):
        db_student = Student(name=name, age=age)
        db.add(db_student)
        await db.flush()
        return db_student

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Student))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, student_id: int):
        return await db.get(Student, student_id)

    @staticmethod
    async def delete(db: AsyncSession, student):
        await db.delete(student)

    @staticmethod
    async def add_to_group(db: AsyncSession, student, group_id: int):
        student.group_id = group_id

    @staticmethod
    async def remove_from_group(db: AsyncSession, student):
        student.group_id = None


class GroupRepository:
    @staticmethod
    async def create(db: AsyncSession, name: str):
        db_group = Group(name=name)
        db.add(db_group)
        await db.flush()
        return db_group

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Group))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, group_id: int):
        return await db.get(Group, group_id)

    @staticmethod
    async def delete(db: AsyncSession, group):
        await db.delete(group)

    @staticmethod
    async def get_students(db: AsyncSession, group_id: int):
        result = await db.execute(
            select(Student).where(Student.group_id == group_id)
        )
        return result.scalars().all()

    @staticmethod
    async def transfer_student(db: AsyncSession, student, target_group_id: int):
        student.group_id = target_group_id