from django import template

register = template.Library()

@register.filter
def declension_years(years):
    years = abs(int(years))
    if 11 <= years % 100 <= 19:
        return f"{years} лет"
    elif years % 10 == 1:
        return f"{years} год"
    elif 2 <= years % 10 <= 4:
        return f"{years} года"
    else:
        return f"{years} лет"
