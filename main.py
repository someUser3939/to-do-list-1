from abs import ABC, abstractmethod
import json
from typing import List, Dict, Any

class Zadaci(ABC):
    def __init__(self, prompt: str="Введите задачу которую хотите сделать", completed: bool=False):
        self.prompt = prompt
        self.completed = completed

    
    # def __init__(self, zadacha: str) -> None:
    #     self.zadacha = zadacha
    #     """
    #     создаем общую стурктуру
    #     """

    # def read_string(self) -> str:
    #     return input(self.prompt)

    def to_dict(self) -> dict[str, Any]:
        """
        преобразует обьект задачи в словарь json.
        """
        return {
            "title": self.title,
            "completed": self.completed
        }
    @classmethod
    def from_dict(cls, data: Dict[str, Any])

    #работает с записью в файл
