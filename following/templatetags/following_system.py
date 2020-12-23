from django import template
register = template.Library()

@register.filter
def who_is_myfolloweds(user,myfolloweds):
    if user.username in myfolloweds:
        return True
    return False