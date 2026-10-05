from django import template
from datetime import date

register = template.Library()

@register.filter
def roc_date(value):
    if not value:
        return ''
    if isinstance(value, str):
        try:
            value = date.fromisoformat(value)
        except ValueError:
            return value
    year = value.year - 1911
    return f"民國 {year} 年 {value.month:02d} 月 {value.day:02d} 日"
