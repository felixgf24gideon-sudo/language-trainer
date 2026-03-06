from abc import ABC, abstractmethod
from app.models.task import Task

class BaseTaskBuilder(ABC):
    def __init__(self, level: int):
        self.level = level

    @abstractmethod
    def build(self) -> Task:
        pass

    @property
    @abstractmethod
    def task_type(self) -> str:
        pass
