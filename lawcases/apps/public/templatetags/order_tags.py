from django import template

register = template.Library()


@register.filter(name='order_title')
def order_title(value):
    temp = '%s ascending' % value.replace('_', ' ')
    if value[0] == '-':
        temp = '%s descending' % value[1:].replace('_', ' ')
    return temp


@register.filter(name='order')
def order(value, args):
    list = args.split(";")
    if value:
        list = args.split(";")
        ico = '-asc'
        a_tpl = '<a href="%s">%s <i class="fa %s"></i></a>'
        link = '?sort=%s' % list[0]

        if value == list[0]:
            link = '?sort=-%s' % list[0]
        elif value == '-' + list[0]:
            ico = '-desc'
            link = '?sort=%s' % list[0]
        else:
            list[1] = 'fa-unsorted'
            ico = ''

        return a_tpl % (link, list[2], (list[1] + ico))
    else:
        return list[2]