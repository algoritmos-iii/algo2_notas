from abc import ABC, abstractmethod


class TemplaterInterface(ABC):
    @abstractmethod
    def render(self, template_name: str, context: dict) -> str:
        """
        Fills the template with the values in the context and return the output.
        """
        ...
