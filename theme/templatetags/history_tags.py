from django import template

register = template.Library()


@register.simple_tag
def get_history_type_string(log):
    if log.history_type == "+":
        return "created"
    elif log.history_type == "-":
        return "deleted"
    elif log.history_type == "~":
        if log.history_object.deleted_at:
            return "deleted"
        else:
            return "updated"
    else:
        return log.history_type
