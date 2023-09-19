from jinja2 import Environment, PackageLoader, select_autoescape
import markdown

def _markdown2HTML(value: str) -> str:
    """Converts a markdown string into html code"""
    return markdown.markdown(value, extensions=["fenced_code"])


def _as_grade_str(value: float) -> str:
    """
    Returns the a value converted to a string rounded to 3 significant
    figures using the least amount of decimal places possible.
    For example, `9.50` gets converted to `"9.5"`.
    """
    return "{:.3g}".format(value)

jinja2_env = Environment(
    loader=PackageLoader("emails"),
    autoescape=select_autoescape()
)

jinja2_env.filters["md"] = _markdown2HTML
jinja2_env.filters["as_grade_str"] = _as_grade_str
