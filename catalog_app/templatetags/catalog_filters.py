from django import template


register = template.Library()


# this can be used if you're having trouble configuring the proper locale
# for your operating system
@register.filter(name='currency')
def currency(value):
    return '$' + str(value)
