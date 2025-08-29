import markdown
import bleach
from django import template

register = template.Library()

@register.filter
def markdownify(text):
    html = markdown.markdown(text, extensions=["fenced_code", "tables"])
    return bleach.clean(html)
