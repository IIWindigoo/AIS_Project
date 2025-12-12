from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.trainings.dao import TrainingDAO
from app.trainings.schemas import (STrainingInfo, STrainingAdd, STrainingFilter, STrainingUpd, 
                                   STrainingWithBookings)
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.dependencies.auth_dep import get_current_trainer_admin_user, get_current_trainer_user
from app.exceptions import (TrainingNotFound, TrainingForbiddenException, TrainerNotFound,
                            RoomNotFound, RoomTimeConflictException, TrainerTimeConflictException)
from app.users.models import User
from app.users.dao import UsersDAO
from app.rooms.dao import RoomDAO


router = APIRouter(prefix="/trainings", tags=["Trainings"])

@router.get("/", summary="Получить все тренировки")
async def get_all_trainings(session: AsyncSession = Depends(get_session_without_commit)
                            ) -> list[STrainingInfo]:
    """
    Возвращает список всех существующих тренировок.
    Доступ у всех
    """
    trainings = await TrainingDAO(session).find_all()
    today = date.today()

    # Фильтруем тренировки: показываем только будущие и сегодняшние
    # Добавляем booking_count для каждой тренировки
    result = []
    for training in trainings:
        if training.date >= today:  # Только будущие тренировки
            training_dict = STrainingInfo.model_validate(training).model_dump()
            training_dict['booking_count'] = len(training.bookings)
            result.append(STrainingInfo(**training_dict))
    return result

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
    room_dao = RoomDAO(session)
    # Проверка, существует ли тренер
    trainer = await user_dao.find_one_or_none_by_id(training_data.trainer_id)
    if not trainer or trainer.role.name != "trainer":
        raise TrainerNotFound
    # Проверка, существует ли помещение
    room = await room_dao.find_one_or_none_by_id(training_data.room_id)
    if not room:
        raise RoomNotFound

    # Проверка конфликтов времени для помещения И тренера (один запрос)
    has_conflict, conflict_type = await training_dao.check_time_conflicts(
        room_id=training_data.room_id,
        trainer_id=training_data.trainer_id,
        training_date=training_data.date,
        start_time=training_data.start_time,
        end_time=training_data.end_time
    )
    if has_conflict:
        if conflict_type == "room":
            raise RoomTimeConflictException
        elif conflict_type == "trainer":
            raise TrainerTimeConflictException
    # Добавление тренировки
    new_training = await training_dao.add(values=training_data)
    if new_training:
        # Перезагружаем тренировку с relationships
        training_full = await training_dao.find_one_or_none_by_id(new_training.id)
        training_dict = STrainingInfo.model_validate(training_full).model_dump()
        training_dict['booking_count'] = len(training_full.bookings)
        return STrainingInfo(**training_dict)
    return {"message": "Ошибка при добавлении тренировки"}

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

    # Проверка конфликта времени, если изменяются дата, время, помещение или тренер
    update_data = data.model_dump(exclude_unset=True)
    if any(field in update_data for field in ['date', 'start_time', 'end_time', 'room_id', 'trainer_id']):
        # Используем новые значения или старые, если не изменялись
        check_room_id = update_data.get('room_id', training.room_id)
        check_trainer_id = update_data.get('trainer_id', training.trainer_id)
        check_date = update_data.get('date', training.date)
        check_start_time = update_data.get('start_time', training.start_time)
        check_end_time = update_data.get('end_time', training.end_time)

        # Проверка конфликтов времени для помещения И тренера (один запрос)
        has_conflict, conflict_type = await training_dao.check_time_conflicts(
            room_id=check_room_id,
            trainer_id=check_trainer_id,
            training_date=check_date,
            start_time=check_start_time,
            end_time=check_end_time,
            exclude_training_id=training_id  # Исключаем текущую тренировку
        )
        if has_conflict:
            if conflict_type == "room":
                raise RoomTimeConflictException
            elif conflict_type == "trainer":
                raise TrainerTimeConflictException

    # Обновление информации о тренировке
    filters = STrainingFilter(id=training_id)
    update_values = STrainingUpd(**update_data)
    updated_count = await training_dao.update(
        filters=filters,
        values=update_values
    )

    if updated_count == 0:
        raise HTTPException(status_code=400, detail="Обновление не выполнено")
    updated = await training_dao.find_one_or_none_by_id(training_id)
    # Добавляем booking_count
    updated_dict = STrainingInfo.model_validate(updated).model_dump()
    updated_dict['booking_count'] = len(updated.bookings)
    return STrainingInfo(**updated_dict)

@router.get("/my/", summary="Мои тренировки с участниками", response_model=list[STrainingWithBookings])
async def get_my_trainings(session: AsyncSession = Depends(get_session_without_commit),
                           user_data: User = Depends(get_current_trainer_user)):
    trainer_id = user_data.id
    trainings = await TrainingDAO(session).find_by_trainer_with_clients(trainer_id)
    return trainings
