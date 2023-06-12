# custom_filters.py
from django import template

register = template.Library()

@register.filter
def ordinal_suffix(value):
    value = int(value)
    if 10 <= value % 100 < 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(value % 10, "th")
        if suffix == "st" and value % 100 == 11:
            suffix = "th"
    return f"{value}{suffix}"

@register.filter
def get_status(upis_status, predmet_id):
    return upis_status.get(predmet_id, 'none')

