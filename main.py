
"""
1. Отсутствует класс Task: В TaskMananger и других местах вы используете класс Task, но объявили только абстрактный класс Zadaci. Класс Task нужно явно создать и унаследовать от Zadaci.
2. Не импортирован модуль os: В методе load_from_json используется os.path.exists, но import os в начале файла нет.
3. Опечатки в настройке logging:
	• Параметр %(activetime)s не существует в стандартном логировании Python (правильно %(asctime)s).
	• В кодировке файла ошибка: encoding='uft-8' (надо utf-8).
4. Заглушка в списке задач: В TaskMananger.__init__ написано self.tasks: List[Task] = [0]. Из-за этого при сохранении пустой базы программа попытается вызвать метод .to_dict() у числа 0 и выдаст ошибку AttributeError. Список должен быть пустым: [].

"""
"""

Что было улучшено помимо исправления ошибок:

• Меню вместо бесконечного ввода: В оригинальной версии можно было только добавлять задачи, но нельзя было посмотреть текущие. Теперь добавлено простое текстовое меню.
• Абстракция заработала: Теперь Zadaci — это честный абстрактный класс с @abstractmethod, а Task — его наследник.
• Логирование в деле: Добавлены вызовы logging.info и logging.error. Теперь в файле simple.log действительно будут фиксироваться действия программы.
"""
from abc import ABC, abstractmethod
import json
import logging
import os
from typing import List, Dict, Any

# Исправлены опечатки в %(asctime)s и utf-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('simple.log', encoding='utf-8')
    ]
)

class Zadaci(ABC):
    """ Абстрактный класс для будущих расширений (например, разные типы задач) """
    def __init__(self, title: str, completed: bool = False):
        self.title = title
        self.completed = completed

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass


class Task(Zadaci):
    """ Конкретная реализация задачи """
    def to_dict(self) -> Dict[str, Any]:
        """ Преобразует объект задачи в словарь для JSON. """
        return {
            "title": self.title,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """ Создает задачу из словаря при чтении из JSON """
        return cls(title=data["title"], completed=data.get('completed', False))


class TaskManager:  # Исправлена опечатка в названии Mananger -> Manager
    def __init__(self, filename: str = "task.json"):
        self.filename = filename
        self.tasks: List[Task] = []  # Убрали, теперь список изначально пустой
        self.load_from_json()

    def add_task(self, title: str) -> None:
        new_task = Task(title=title)
        self.tasks.append(new_task)
        self.save_to_json()
        logging.info(f"Добавлена новая задача: {title}")

    def save_to_json(self) -> None:
        """ Сохраняет все задачи в JSON файл """
        data = [task.to_dict() for task in self.tasks]
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"Ошибка при сохранении файла: {e}")

    def load_from_json(self) -> None:
        """ Загружает задачи из JSON файла при старте """
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
            logging.info(f"Успешно загружено {len(self.tasks)} задач.")
        except (json.JSONDecodeError, KeyError) as e:
            logging.warning(f"Ошибка чтения файла (файл поврежден или пуст): {e}")
            self.tasks = []


class ConsoleApp:
    def __init__(self):
        self.manager = TaskManager()

    def print_menu(self) -> None:
        print("\n--- To-Do List ---")
        print("1. Посмотреть список задач")
        print("2. Добавить задачу")
        print("3. Выход ('exit')")

    def show_tasks(self) -> None:
        if not self.manager.tasks:
            print("Список задач пуст.")
            return
        for idx, task in enumerate(self.manager.tasks, 1):
            status = "✅" if task.completed else "❌"
            print(f"{idx}. [{status}] {task.title}")

    def run(self) -> None:
        while True:
            self.print_menu()
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self.show_tasks()
            elif choice == "2":
                text = input("Введите описание задачи: ").strip()
                if text:
                    self.manager.add_task(text)
                    print(f"Задача '{text}' успешно сохранена!")
            elif choice.lower() == "exit" or choice == "3":
                print("Выход из программы.")
                break
            else:
                print("Неверный ввод, попробуйте снова.")


if __name__ == '__main__':
    app = ConsoleApp()
    app.run()
