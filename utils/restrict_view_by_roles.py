def restrict_view_if_not_admin(request):
    if not request.user.is_super_admin:
        return {'change': False, 'add': False}
    return {'change': True, 'add': True}


def restrict_add_allow_change():
    return {'change': True, 'add': False}
