from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.trainings.dao import TrainingDAO
from app.trainings.schemas import (STrainingInfo, STrainingAdd, STrainingFilter, STrainingUpd, 
                                   STrainingWithBookings)
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.dependencies.auth_dep import get_current_trainer_admin_user, get_current_trainer_user
from app.exceptions import TrainingNotFound, TrainingForbiddenException, TrainerNotFound, RoomNotFound
from app.users.models import User
from app.users.dao import UsersDAO


router = APIRouter(prefix="/trainings", tags=["Trainings"])

@router.get("/", summary="Получить все тренировки")
async def get_all_trainings(session: AsyncSession = Depends(get_session_without_commit)
                            ) -> list[STrainingInfo]:
    """
    Возвращает список всех существующих тренировок.
    Доступ у всех
    """
    return await TrainingDAO(session).find_all()

@router.post("/", summary="Создать тренировку")
async def create_training(training_data: STrainingAdd,
                          session: AsyncSession = Depends(get_session_with_commit),
                          user_data: User = Depends(get_current_trainer_admin_user)
                          ) -> STrainingInfo | dict:
    """
    Создает новую тренировку.
    Доступ только у администратора и тренера
    """
    training_dao = TrainingDAO(session)
    user_dao = UsersDAO(session)
    # Проверка, существует ли тренер
    trainer = await user_dao.find_one_or_none_by_id(training_data.trainer_id)
    if not trainer or trainer.role.name != "trainer":
        raise TrainerNotFound
    # Проверка, существует ли помещение
    room = await training_dao.find_one_or_none_by_id(training_data.room_id)
    if not room:
        raise RoomNotFound
    # Добавление тренировки
    new_training = await training_dao.add(values=training_data)
    if new_training:
        return STrainingInfo.model_validate(new_training)
    return {"message": "Ошибка при добавлении заметки"}

@router.delete("/{training_id}/", summary="Удалить тренировку по ID")
async def delete_training(training_id: int,
                          session: AsyncSession = Depends(get_session_with_commit),
                          user_data: User = Depends(get_current_trainer_admin_user)
                          ) -> dict:
    """
    Удаление конкретной тренировки по ID.
    Доступ только у администратора и тренера
    """
    training_dao = TrainingDAO(session)

    # Проверка существования тренировки
    training = await training_dao.find_one_or_none_by_id(training_id)
    if not training:
        raise TrainingNotFound
    # Проверка: удалить может админ или тренер, которому принадлежит тренировка
    if user_data.role.name != "admin" and training.trainer_id != user_data.id:
        raise TrainingForbiddenException
    # Удаление тренировки
    filters = STrainingFilter(id=training_id)
    deleted_count = await training_dao.delete(filters=filters)
    if deleted_count:
        return {"message": f"Тренировка {training.title} успешно удалена",
                "deleted_count": deleted_count,
                "deleted_training":{
                    "id": training.id,
                    "title": training.title,
                    "date": training.date
                }
            }
    return {"message": "Ошибка при удалении тренировки"}

@router.patch("/{training_id}/", summary="Редактировать тренировку")
async def update_training(training_id: int,
                          data: STrainingUpd,
                          session: AsyncSession = Depends(get_session_with_commit),
                          user_data: User = Depends(get_current_trainer_admin_user)
                          ) -> STrainingInfo:
    """
    Изменение информации о тренировке по ID.
    Доступ только у администратора и тренера
    """
    training_dao = TrainingDAO(session)

    # Проверка существования тренировки
    training = await training_dao.find_one_or_none_by_id(training_id)
    if not training:
        raise TrainingNotFound
    # Проверка: редактировать может админ или тренер, которому принадлежит тренировка
    if user_data.role.name != "admin" and training.trainer_id != user_data.id:
        raise TrainingForbiddenException
    # Обновление информации о тренировке
    filters = STrainingFilter(id=training_id)
    update_values = STrainingUpd(**data.model_dump(exclude_unset=True))
    updated_count = await training_dao.update(
        filters=filters,
        values=update_values
    )

    if updated_count == 0:
        raise HTTPException(status_code=400, detail="Обновление не выполнено")
    updated = await training_dao.find_one_or_none_by_id(training_id)
    return STrainingInfo.model_validate(updated)

@router.get("/my/", summary="Мои тренировки с участниками", response_model=list[STrainingWithBookings])
async def get_my_trainings(session: AsyncSession = Depends(get_session_without_commit),
                           user_data: User = Depends(get_current_trainer_user)):
    trainer_id = user_data.id
    trainings = await TrainingDAO(session).find_by_trainer_with_clients(trainer_id)
    return trainings
