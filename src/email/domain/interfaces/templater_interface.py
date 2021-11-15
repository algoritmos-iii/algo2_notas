from abc import ABC, abstractmethod


class TemplaterInterface(ABC):
    @abstractmethod
    def render(template_name: str, context: dict) -> str:
        ...
