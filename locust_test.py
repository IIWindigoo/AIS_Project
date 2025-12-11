from locust import HttpUser, task, between, tag
import random


class ClientUser(HttpUser):
    """
    Сценарий тестирования для пользователя с ролью "client"

    Клиенты могут:
    - Просматривать тренировки и абонементы (GET)
    - Создавать бронирования (POST /bookings/)

    Вес: 3 (будет запущено 75% клиентов от общего числа пользователей)
    """
    weight = 3
    wait_time = between(1.0, 5.0)

    def on_start(self):
        """Авторизация как клиент"""
        login_payload = {
            "email": "client@example.com",
            "password": "client"
        }
        response = self.client.post("/users/login/", json=login_payload)
        if response.status_code == 200:
            print(f"✅ Клиент авторизован: {login_payload['email']}")
        else:
            print(f"⚠️  Авторизация клиента не удалась (статус {response.status_code})")

    @task(5)
    @tag("get_task")
    def get_trainings(self):
        """
        GET запрос - получение списка всех тренировок
        Вес: 5 (наиболее частый запрос)
        """
        with self.client.get("/trainings/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Ошибка получения тренировок: {response.status_code}")

    @task(3)
    @tag("get_task")
    def get_subscriptions(self):
        """
        GET запрос - получение списка абонементов
        Вес: 3
        """
        with self.client.get("/subscriptions/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Ошибка получения абонементов: {response.status_code}")

    @task(2)
    @tag("post_task")
    def create_booking(self):
        """
        POST запрос - создание бронирования на тренировку
        Вес: 2
        """
        # Используем конкретные ID тренировок
        training_id = random.choice([1, 2, 4, 8, 9, 10])
        payload = {
            "training_id": training_id
        }
        with self.client.post("/bookings/", json=payload, catch_response=True) as response:
            if response.status_code in [200, 201]:
                response.success()
            elif response.status_code in [400, 409]:
                # 400 - валидационная ошибка
                # 409 - конфликт (уже забронировано или нет мест)
                response.success()
            else:
                response.failure(f"Ошибка создания бронирования: {response.status_code}")


class TrainerUser(HttpUser):
    """
    Сценарий тестирования для пользователя с ролью "trainer"

    Тренеры могут:
    - Просматривать тренировки и абонементы (GET)
    - Изменять свои тренировки (PATCH /trainings/{id}/)

    Вес: 1 (будет запущено 25% тренеров от общего числа пользователей)
    """
    weight = 1
    wait_time = between(1.0, 5.0)

    def on_start(self):
        """Авторизация как тренер"""
        login_payload = {
            "email": "trainer@example.com",
            "password": "trainer"
        }
        response = self.client.post("/users/login/", json=login_payload)
        if response.status_code == 200:
            print(f"✅ Тренер авторизован: {login_payload['email']}")
        else:
            print(f"⚠️  Авторизация тренера не удалась (статус {response.status_code})")

    @task(5)
    @tag("get_task")
    def get_trainings(self):
        """
        GET запрос - получение списка всех тренировок
        Вес: 5
        """
        with self.client.get("/trainings/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Ошибка получения тренировок: {response.status_code}")

    @task(3)
    @tag("get_task")
    def get_subscriptions(self):
        """
        GET запрос - получение списка абонементов
        Вес: 3
        """
        with self.client.get("/subscriptions/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Ошибка получения абонементов: {response.status_code}")

    @task(2)
    @tag("put_task")
    def update_training(self):
        """
        PATCH запрос - обновление информации о тренировке
        Вес: 2 (более частая операция для тренера)
        """
        # Выбираем случайный ID тренировки для обновления
        training_id = random.choice([8, 9, 10])
        payload = {
            "title": f"Обновленная тренировка {random.randint(1, 100)}",
            "description": f"Тестовое описание для нагрузочного теста №{random.randint(1, 1000)}"
        }
        with self.client.patch(f"/trainings/{training_id}/", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # 404 - тренировка не найдена (нормально, если ID не существует)
                response.success()
            else:
                response.failure(f"Ошибка обновления тренировки: {response.status_code}")
