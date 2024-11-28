from src.Models.house_maintenance import House_maintenance  # Импорт модели
from src.Models.house import House
from datetime import datetime  # Импортируем для получения текущей даты и времени


class HouseMaintenanceController:

    @staticmethod
    def create_maintenance_record(house_id, service_type, status, notes):
        """Создает новую запись в таблице house_maintenance."""
        try:
            # Вставка новой записи с использованием текущего времени
            maintenance_record = House_maintenance.create(
                house_id=house_id,
                service_type=service_type,
                maintenance_date=datetime.now(),  # Получаем текущую дату и время
                status=status,
                notes=notes
            )
            print(f"Запись успешно добавлена: {maintenance_record}")
            return maintenance_record
        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")
            return None

    @staticmethod
    def update_maintenance_record(house_id, new_service_type, new_status, new_notes):
        try:
            # Находим запись по ID дома
            maintenance_record = House_maintenance.get(House_maintenance.house_id == house_id)

            # Обновляем запись
            maintenance_record.service_type = new_service_type
            maintenance_record.status = new_status
            maintenance_record.notes = new_notes
            maintenance_record.save()  # Сохраняем изменения

        except House_maintenance.DoesNotExist:
            raise ValueError(f"Запись обслуживания с ID {house_id} не найдена.")

    @staticmethod
    def delete_maintenance_record(house_id):
        """Deletes a maintenance record based on house_id."""
        try:
            # Assuming House_maintenance is the model handling maintenance records
            maintenance_record = House_maintenance.get(House_maintenance.house_id == house_id)
            maintenance_record.delete_instance()  # Delete the record
            print(f"Maintenance record for house ID {house_id} has been deleted.")
        except House_maintenance.DoesNotExist:
            raise ValueError(
                f"Record for house ID {house_id} not found.")  # Handling the case where the record doesn't exist

# Главная функция с меню для выбора операции
def main():
    controller = HouseMaintenanceController()

    while True:
        print("\nВыберите операцию:")
        print("1. Создать новую запись обслуживания")
        print("2. Обновить существующую запись обслуживания")
        print("3. Выход")

        choice = input("Введите номер операции: ").strip()

        if choice == '1':
            # Запрашиваем данные для создания новой записи
            try:
                house_id = int(input("Введите ID дома: "))  # Запрашиваем house_id как целое число
            except ValueError:
                print("Ошибка: ID дома должен быть числом.")
                continue

            service_type = input("Введите тип услуги (например, '666'): ")  # Запрашиваем service_type как строку
            status = input("Введите статус работы (например, 'Готово'): ")  # Запрашиваем статус
            notes = input("Введите примечания (например, 'Работа выполнена по графику'): ")  # Запрашиваем примечания

            # Создаем запись в базе данных
            controller.create_maintenance_record(house_id, service_type, status, notes)

        elif choice == '2':
            # Запрашиваем данные для обновления существующей записи
            try:
                maintenance_id = int(input("Введите ID записи для обновления: "))  # Запрашиваем ID записи
                new_status = input("Введите новый статус работы: ")
                new_notes = input("Введите новые примечания: ")

                # Обновляем запись в базе данных
                controller.update_maintenance_record(maintenance_id, new_status, new_notes)

            except ValueError:
                print("Ошибка: ID записи должен быть числом.")
                continue

        elif choice == '3':
            # Выход из программы
            print("Выход из программы.")
            break

        else:
            print("Ошибка: Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")


# Запуск программы
if __name__ == "__main__":
    main()
