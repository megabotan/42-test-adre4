from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.tag
def edit_link(paser, token):
    try:
        tag_name, object_ = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])
    return EditLinkNode(object_)


class EditLinkNode(template.Node):
    def __init__(self, object_):
        self.object_ = template.Variable(object_)

    def render(self, context):
        try:
            ready_object = self.object_.resolve(context)
            return reverse(
                'admin:{0}_{1}_change'.format(
                    ready_object._meta.app_label,
                    ready_object._meta.object_name).lower(),
                args=[ready_object.id])
        except template.VariableDoesNotExist:
            return ''
