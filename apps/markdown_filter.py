import markdown
def markdown2HTML(value: str) -> str:
    return markdown.markdown(value, extensions=["fenced_code"])