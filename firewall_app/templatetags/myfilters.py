from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css):
    return field.as_widget(attrs={"class":css})
@register.filter(name='addid')
def addid(value, arg):
    return value.as_widget(attrs={'class': arg})