import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Импортируем нужные контроллеры и модели
from src.Models.residents import Residents
from src.Models.payments import Payments
from src.Models.services import Services
from src.Models.house_maintenance import House_maintenance
from src.Models.house import House
from src.Controllers.ResidentsController import ResidentsController
from src.Controllers.HouseController import HouseMaintenanceController
from src.Models.roles import Roles


class LoginPanel:
    def __init__(self, master):
        self.master = master

        # Заголовок
        tk.Label(master, text="Авторизация", font=("Helvetica", 16)).pack(pady=10)

        # Поле для ввода логина
        tk.Label(master, text="Введите логин:").pack()
        self.login_entry = tk.Entry(master)
        self.login_entry.pack(pady=5)

        # Поле для ввода пароля
        tk.Label(master, text="Введите пароль:").pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        # Кнопка для авторизации
        self.login_button = tk.Button(master, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if not login or not password:
            messagebox.showerror("Ошибка", "Логин и пароль обязательны.")
            return

        try:
            # Попытка найти пользователя в базе данных
            resident = Residents.get_or_none(Residents.login == login)

            # Проверим, был ли найден пользователь
            if not resident:
                messagebox.showerror("Ошибка", "Пользователь с таким логином не найден.")
                return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при подключении к базе данных: {e}")
            return

        # Если житель найден, проверяем пароль
        if resident:
            print(f"Найден пользователь: {resident.login}")  # Для отладки

            # Сравниваем введённый пароль с тем, который хранится в базе данных
            if resident.password == password:  # Прямое сравнение паролей
                messagebox.showinfo("Успех", f"Авторизация успешна! ID жителя: {resident.resident_id}")

                # Загружаем роль пользователя
                role = Roles.get_or_none(Roles.role_id == resident.roles_id)  # Пример поиска по role_id

                if role:
                    print(f"Роль пользователя: {role.role_name}")  # Для отладки

                    # В зависимости от роли пользователя перенаправляем на нужную панель
                    if role.role_name == "Admin":  # Пример роли администратора
                        self.master.destroy()  # Закрываем окно авторизации
                        self.open_house_maintenance_panel(resident.resident_id)
                    elif role.role_name == "Resident":  # Пример роли жителя
                        self.master.destroy()  # Закрываем окно авторизации
                        self.open_payment_panel(resident.resident_id)
                    else:
                        messagebox.showerror("Ошибка", "У вас нет прав для входа в систему.")
                else:
                    messagebox.showerror("Ошибка", "Роль пользователя не найдена.")
            else:
                messagebox.showerror("Ошибка", "Неверный пароль.")
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким логином не найден.")

    def open_house_maintenance_panel(self, resident_id):
        root = tk.Tk()
        root.title("Панель обслуживания домов")

        # Создаем панель обслуживания с передачей ID жителя
        maintenance_panel = HouseMaintenancePanel(root, resident_id)
        root.mainloop()

    def open_payment_panel(self, resident_id):
        root = tk.Tk()
        root.title("Панель оплаты услуг")

        # Создаем панель оплаты с передачей ID жителя
        payment_panel = PaymentController(root, resident_id)
        root.mainloop()


class PaymentController:
    def __init__(self, master, resident_id):
        self.master = master
        self.resident_id = resident_id
        self.selected_status = "В процессе"  # Значение по умолчанию для статуса

        # Удаляем поле для ввода ID жильца, так как оно больше не нужно
        # tk.Label(master, text="Введите ID жильца:").pack()
        # self.resident_entry = tk.Entry(master, textvariable=self.resident_id)
        # self.resident_entry.pack()

        # Кнопка для отображения услуг
        self.show_services_button = tk.Button(master, text="Показать услуги", command=self.display_services)
        self.show_services_button.pack()

        # Список услуг с прокруткой
        self.services_frame = tk.Frame(master)
        self.services_frame.pack(pady=10)

        self.services_listbox = tk.Listbox(self.services_frame, width=50, height=15)
        self.services_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.services_frame, orient="vertical", command=self.services_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.services_listbox.config(yscrollcommand=self.scrollbar.set)

        # Удаляем выпадающий список для статуса, так как статус теперь всегда "В процессе"

        # Кнопка для оплаты услуги
        self.pay_button = tk.Button(master, text="Оплатить услугу", command=self.pay_service)
        self.pay_button.pack()

    def display_services(self):
        # Очищаем список перед отображением
        self.services_listbox.delete(0, tk.END)

        # Получаем все доступные услуги
        services = Services.select()
        for service in services:
            service_info = f"ID: {service.service_id}, Услуга: {service.service_name}, Стоимость: {service.cost}"
            self.services_listbox.insert(tk.END, service_info)

    def pay_service(self):
        # Получаем выбранный элемент из списка
        selected_service = self.services_listbox.curselection()
        if not selected_service:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите услугу.")
            return

        service_index = selected_service[0]
        service_info = self.services_listbox.get(service_index)
        service_id = int(service_info.split(",")[0].split(":")[1].strip())  # Извлекаем ID услуги
        amount = float(service_info.split(",")[2].split(":")[1].strip())  # Извлекаем стоимость

        # Статус всегда "В процессе"
        status = "В процессе"

        try:
            # Выполнение вставки в базу данных
            payment = Payments.create(
                residents_id=self.resident_id,
                services_id=service_id,
                payment_date=datetime.now(),
                amount=amount,
                status=status
            )
            messagebox.showinfo("Успех", f"Оплата успешно проведена. Payment ID: {payment.id}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при оплате: {e}")



class HouseMaintenancePanel:
    def __init__(self, master, resident_id):
        self.master = master
        self.resident_id = resident_id  # Получаем ID жителя
        self.setup_ui()

    def setup_ui(self):
        # Панель для отображения уже обслуживаемых домов
        tk.Label(self.master, text="Все обслуживаемые дома:").pack()

        # Список домов с прокруткой
        self.houses_frame = tk.Frame(self.master)
        self.houses_frame.pack(pady=10)

        self.houses_listbox = tk.Listbox(self.houses_frame, width=80, height=15)
        self.houses_listbox.pack(side="left", fill="both", expand=True)

        self.houses_scrollbar = tk.Scrollbar(self.houses_frame, orient="vertical", command=self.houses_listbox.yview)
        self.houses_scrollbar.pack(side="right", fill="y")

        self.houses_listbox.config(yscrollcommand=self.houses_scrollbar.set)

        # Кнопка для обновления списка домов
        self.refresh_button = tk.Button(self.master, text="Обновить список домов", command=self.display_houses)
        self.refresh_button.pack()

        # Кнопка для удаления записи обслуживания
        self.delete_button = tk.Button(self.master, text="Удалить запись обслуживания", command=self.delete_maintenance_record)
        self.delete_button.pack(pady=10)

        # Кнопка для отображения оплаченных услуг
        self.view_paid_services_button = tk.Button(self.master, text="Показать оплаченные услуги", command=self.open_paid_services_window)
        self.view_paid_services_button.pack(pady=10)

        # Поле для выбора дома из выпадающего списка
        tk.Label(self.master, text="Выберите дом:").pack()

        # Выпадающий список для выбора дома
        self.house_id_var = tk.StringVar()
        self.house_id_menu = tk.OptionMenu(self.master, self.house_id_var, *self.get_all_house_ids())
        self.house_id_menu.pack()

        tk.Label(self.master, text="Введите тип услуги:").pack()
        self.service_type_entry = tk.Entry(self.master)
        self.service_type_entry.pack()

        tk.Label(self.master, text="Введите статус работы:").pack()
        self.status_entry = tk.Entry(self.master)
        self.status_entry.pack()

        tk.Label(self.master, text="Введите примечания:").pack()
        self.notes_entry = tk.Entry(self.master)
        self.notes_entry.pack()

        # Кнопка для добавления новой записи обслуживания
        self.add_button = tk.Button(self.master, text="Добавить запись обслуживания", command=self.add_maintenance_record)
        self.add_button.pack()

        # Кнопка для обновления записи обслуживания
        self.update_button = tk.Button(self.master, text="Обновить запись обслуживания", command=self.update_maintenance_record)
        self.update_button.pack()

        self.display_houses()  # Загрузим все дома при старте

    def get_all_house_ids(self):
        """Получаем все ID домов для выпадающего списка."""
        try:
            houses = House.select()
            return [str(house.id) for house in houses]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении данных о домах: {e}")
            return []

    def display_houses(self):
        """Отображает все обслуживаемые дома в списке."""
        self.houses_listbox.delete(0, tk.END)
        houses = House_maintenance.select()
        for house in houses:
            try:
                # Проверим, существует ли дом с указанным house_id
                house_data = House.get(House.id == house.house_id)
                house_info = f"ID: {house_data.id}, Услуга: {house.service_type}, Статус: {house.status}, Примечания: {house.notes}"
                self.houses_listbox.insert(tk.END, house_info)
            except House.DoesNotExist:
                house_info = f"ID: {house.house_id} - Дом не найден"
                self.houses_listbox.insert(tk.END, house_info)

    def add_maintenance_record(self):
        """Добавляет новую запись обслуживания."""
        house_id = self.house_id_var.get()
        if not house_id:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите дом.")
            return

        service_type = self.service_type_entry.get()
        status = self.status_entry.get()
        notes = self.notes_entry.get()

        if not service_type or not status or not notes:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Создаем новую запись обслуживания
        try:
            HouseMaintenanceController.create_maintenance_record(
                house_id=house_id,
                service_type=service_type,
                status=status,
                notes=notes
            )
            messagebox.showinfo("Успех", "Запись обслуживания добавлена.")
            self.display_houses()  # Обновляем список домов
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении записи: {e}")

    def update_maintenance_record(self):
        """Обновляет выбранную запись обслуживания."""
        selected_house = self.houses_listbox.curselection()  # Получаем выбранный элемент
        if not selected_house:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите дом для обновления.")
            return

        # Извлекаем данные о выбранном доме из списка
        house_index = selected_house[0]
        house_info = self.houses_listbox.get(house_index)

        # Извлекаем ID дома из строки
        try:
            house_id = int(house_info.split(",")[0].split(":")[1].strip())  # Извлекаем ID дома
        except ValueError:
            messagebox.showerror("Ошибка", "Не удалось извлечь ID дома из строки.")
            return

        # Получаем новые данные для обновления из полей ввода
        new_service_type = self.service_type_entry.get().strip()
        new_status = self.status_entry.get().strip()
        new_notes = self.notes_entry.get().strip()

        # Проверяем, что все поля заполнены
        if not new_service_type or not new_status or not new_notes:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля для обновления.")
            return

        # Пытаемся обновить запись в базе данных
        try:
            # Используем контроллер для обновления записи
            HouseMaintenanceController.update_maintenance_record(house_id, new_service_type, new_status, new_notes)
            messagebox.showinfo("Успех", f"Запись с ID {house_id} успешно обновлена.")
            self.display_houses()  # Обновляем список домов
        except House_maintenance.DoesNotExist:
            messagebox.showerror("Ошибка", f"Запись обслуживания с ID {house_id} не найдена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обновлении записи: {e}")
    # In your HouseMaintenancePanel class

    def delete_maintenance_record(self):
        """Удаляет выбранную запись обслуживания."""
        selected_house = self.houses_listbox.curselection()
        if not selected_house:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите дом для удаления.")
            return

        house_index = selected_house[0]
        house_info = self.houses_listbox.get(house_index)
        house_id = int(house_info.split(",")[0].split(":")[1].strip())

        # Подтверждение удаления
        confirm = messagebox.askyesno("Подтверждение удаления",
                                      f"Вы уверены, что хотите удалить запись обслуживания для дома с ID {house_id}?")
        if confirm:
            try:
                # Вызываем метод контроллера для удаления
                HouseMaintenanceController.delete_maintenance_record(house_id)
                messagebox.showinfo("Успех", f"Запись обслуживания с ID {house_id} удалена.")
                self.display_houses()  # Обновляем список домов
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

    def open_paid_services_window(self):
        """Открывает окно для отображения всех оплаченных услуг."""
        paid_services_window = tk.Toplevel(self.master)
        paid_services_window.title("Оплаченные услуги")

        # Создаем список с прокруткой для отображения оплаченных услуг
        paid_services_frame = tk.Frame(paid_services_window)
        paid_services_frame.pack(pady=10)

        paid_services_listbox = tk.Listbox(paid_services_frame, width=80, height=15)
        paid_services_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(paid_services_frame, orient="vertical", command=paid_services_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        paid_services_listbox.config(yscrollcommand=scrollbar.set)

        # Добавляем выпадающий список для выбора нового статуса
        tk.Label(paid_services_window, text="Выберите новый статус:").pack(pady=10)
        self.status_var = tk.StringVar(value="Готово")
        status_menu = tk.OptionMenu(paid_services_window, self.status_var, "Готово", "Отклонено")
        status_menu.pack(pady=5)

        # Кнопка для изменения статуса
        self.change_status_button = tk.Button(paid_services_window, text="Изменить статус", command=lambda: self.change_payment_status(paid_services_listbox))
        self.change_status_button.pack(pady=10)

        # Заполняем список оплаченных услуг
        self.display_paid_services(paid_services_listbox)


    def display_paid_services(self, listbox):
        """Отображает все оплаченные услуги."""
        listbox.delete(0, tk.END)

        try:
            # Получаем все оплаченные услуги из базы данных
            payments = Payments.select()

            if not payments:
                listbox.insert(tk.END, "Нет оплаченных услуг.")
                return

            for payment in payments:
                try:
                    # Получаем данные об услуге и жильце
                    service = Services.get(Services.service_id == payment.services_id)
                    resident = Residents.get(Residents.resident_id == payment.residents_id)

                    # Формируем строку с информацией о платеже, включая все поля
                    payment_info = (
                        f"Payment ID: {payment.id}, "
                        f"Житель: {resident.login}, "
                        f"Услуга: {service.service_name}, "
                        f"Стоимость: {payment.amount} руб., "
                        f"Дата: {payment.payment_date.strftime('%Y-%m-%d %H:%M:%S')}, "
                        f"Статус: {payment.status}"
                    )
                    listbox.insert(tk.END, payment_info)

                except Services.DoesNotExist:
                    listbox.insert(tk.END, f"Услуга для платежа ID {payment.id} не найдена.")
                except Residents.DoesNotExist:
                    listbox.insert(tk.END, f"Житель для платежа ID {payment.id} не найден.")
                except Exception as e:
                    listbox.insert(tk.END, f"Ошибка при загрузке данных для платежа ID {payment.id}: {e}")

        except Exception as e:
            # Если ошибка при запросе к базе данных
            listbox.insert(tk.END, f"Ошибка при получении данных о платежах: {e}")

        except Exception as e:
            # Если ошибка при запросе к базе данных
            listbox.insert(tk.END, f"Ошибка при получении данных о платежах: {e}")

    def change_payment_status(self, listbox):
        """Изменяет статус для выбранного платежа."""
        selected_payment_index = listbox.curselection()

        if not selected_payment_index:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите платёж.")
            return

        # Получаем ID выбранного платежа из текста
        payment_info = listbox.get(selected_payment_index[0])
        payment_id = int(payment_info.split(",")[0].split(":")[1].strip())  # Извлекаем ID платежа

        # Получаем выбранный статус
        new_status = self.status_var.get()

        try:
            # Получаем платёж из базы данных
            payment = Payments.get(Payments.id == payment_id)
            payment.status = new_status
            payment.save()  # Сохраняем изменения в базе данных

            messagebox.showinfo("Успех", f"Статус для платежа ID {payment_id} успешно изменён на {new_status}.")
            self.display_paid_services(listbox)  # Обновляем список оплаченных услуг

        except Payments.DoesNotExist:
            messagebox.showerror("Ошибка", f"Платёж с ID {payment_id} не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при изменении статуса: {e}")


# Главная функция для запуска программы
def main():
    root = tk.Tk()
    root.title("Авторизация")  # Назначаем заголовок для главного окна

    # Создаем окно авторизации
    login_panel = LoginPanel(root)
    root.mainloop()


# Запуск программы
if __name__ == "__main__":
    main()