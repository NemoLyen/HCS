from datetime import datetime
from src.Models.payments import Payments  # Убедитесь, что путь к вашей модели правильный

# Функция для получения данных от пользователя
class PaymentController():
    @classmethod
    def get_payment_data(self):
        resident_id = input("Введите ID жильца: ")
        service_id = input("Введите ID услуги: ")
        amount = input("Введите сумму: ")
        status = input("Введите статус: ")
        Payments.create(residents_id=resident_id,
                        services_id=service_id,
                        payment_date=datetime.now(),  # Текущая дата и время
                        amount=amount,
                        status=status)


if __name__ == '__main__':
    # Получаем данные от пользователя
    # resident_id, service_id, amount, status = get_payment_data()
    PaymentController.get_payment_data()
    # Выполнение вставки



