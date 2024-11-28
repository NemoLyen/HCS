from werkzeug.security import check_password_hash, generate_password_hash
from src.Models.residents import Residents
from datetime import datetime


class ResidentsController:

    # Метод авторизации
    @staticmethod
    def login():
        login = input("Введите логин: ").strip()
        password = input("Введите пароль: ").strip()

        if not login or not password:
            print("Ошибка: Логин и пароль обязательны.")
            return

        # Пытаемся найти жителя по логину
        resident = Residents.get_or_none(Residents.login == login)

        # Добавим отладочные сообщения
        if resident:
            print(f"Житель с логином {login} найден.")
        else:
            print(f"Житель с логином {login} не найден.")

        if resident and check_password_hash(resident.password, password):
            print(f"Авторизация успешна! ID жителя: {resident.resident_id}")
        else:
            print("Ошибка: Неверный логин или пароль.")

    # Метод обновления данных жителя
    @staticmethod
    def update_resident():
        resident_id = input("Введите ID жителя для обновления: ").strip()

        # Получаем жителя по ID
        try:
            resident = Residents.get(Residents.resident_id == int(resident_id))  # Преобразуем в int
        except Residents.DoesNotExist:
            print(f"Житель с ID {resident_id} не найден.")
            return

        # Запрашиваем новые данные
        print("Введите новые данные для обновления (оставьте пустым, чтобы не менять):")
        surname = input(f"Фамилия ({resident.surname}): ").strip() or resident.surname
        name = input(f"Имя ({resident.name}): ").strip() or resident.name
        birthdate = input(f"Дата рождения ({resident.birthdate}): ").strip() or str(resident.birthdate)
        apartment_number = input(f"Номер квартиры ({resident.apartment_number}): ").strip() or resident.apartment_number
        telephone = input(f"Телефон ({resident.telephone}): ").strip() or resident.telephone
        roles_id = input(f"Роль ID ({resident.roles_id}): ").strip() or resident.roles_id
        login = input(f"Логин ({resident.login}): ").strip() or resident.login
        password = input(f"Пароль (оставьте пустым, чтобы не менять): ").strip()

        if password:
            password = generate_password_hash(password)
        else:
            password = resident.password

        # Обновляем данные
        resident.surname = surname
        resident.name = name
        resident.birthdate = datetime.strptime(birthdate, "%Y-%m-%d")  # Преобразуем строку в дату
        resident.apartment_number = apartment_number
        resident.telephone = telephone
        resident.roles_id = roles_id
        resident.login = login
        resident.password = password

        resident.save()

        print(f"Данные жителя с ID {resident_id} успешно обновлены.")

    # Метод добавления нового жителя
    @staticmethod
    def add_resident():
        print("Введите данные для нового жителя:")

        surname = input("Фамилия: ").strip()
        name = input("Имя: ").strip()
        birthdate = input("Дата рождения (YYYY-MM-DD): ").strip()
        apartment_number = input("Номер квартиры: ").strip()
        telephone = input("Телефон: ").strip()
        roles_id = input("Роль ID: ").strip()
        login = input("Логин: ").strip()
        password = input("Пароль: ").strip()

        if not all([surname, name, birthdate, apartment_number, telephone, roles_id, login, password]):
            print("Ошибка: Все поля обязательны для заполнения.")
            return

        # Хешируем пароль
        password_hash = generate_password_hash(password)

        # Создаем нового жителя
        resident = Residents.create(
            surname=surname,
            name=name,
            birthdate=datetime.strptime(birthdate, "%Y-%m-%d"),  # Преобразуем строку в дату
            apartment_number=apartment_number,
            telephone=telephone,
            roles_id=roles_id,
            login=login,
            password=password_hash
        )

        print(f"Житель с ID {resident.resident_id} успешно добавлен.")


# Пример вызова методов из командной строки
if __name__ == '__main__':
    while True:
        print("\n1. Авторизация")
        print("2. Обновление данных")
        print("3. Добавить нового жителя")
        print("4. Выход")

        choice = input("Выберите опцию: ").strip()

        if choice == '1':
            ResidentsController.login()
        elif choice == '2':
            ResidentsController.update_resident()
        elif choice == '3':
            ResidentsController.add_resident()
        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите правильный номер.")
