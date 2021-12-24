import markdown
from jinja2 import Environment, loaders

from ..domain.interfaces.templater_interface import TemplaterInterface


def markdown2HTML(value: str) -> str:
    """Converts a markdown string into html code"""
    return markdown.markdown(value, extensions=["fenced_code"])


def as_grade_str(value: float) -> str:
    """
    Returns the a value converted to a string rounded to 3 significant
    figures using the least amount of decimal places possible.

    For example, `9.50` gets converted to `"9.5"`.
    """
    return "{:.3g}".format(value)


class Jinja2Templater(TemplaterInterface):
    """An implementation of a Templater using Jinja2."""

    def __init__(self, templates_search_path: str) -> None:
        self._jinja_env = Environment(
            loader=loaders.FileSystemLoader(templates_search_path)
        )
        self._jinja_env.filters["md"] = markdown2HTML
        self._jinja_env.filters["as_grade_str"] = as_grade_str

    def render(self, template_name: str, context: dict) -> str:
        return self._jinja_env.get_template(template_name).render(context)
