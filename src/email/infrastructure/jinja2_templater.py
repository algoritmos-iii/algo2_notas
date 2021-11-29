import markdown
from jinja2 import Environment, loaders

from ..domain.interfaces.templater_interface import TemplaterInterface


def markdown2HTML(value: str) -> str:
    return markdown.markdown(value, extensions=["fenced_code"])


class Jinja2Templater(TemplaterInterface):
    def __init__(self, templates_search_path: str) -> None:
        self._jinja_env = Environment(
            loader=loaders.FileSystemLoader(templates_search_path)
        )
        self._jinja_env.filters["md"] = markdown2HTML

    def render(self, template_name: str, context: dict) -> str:
        return self._jinja_env.get_template(template_name).render(context)
