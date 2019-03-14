from django.contrib.auth.decorators import user_passes_test

def superuser_required():
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_superuser,
        login_url='/music/not_permitted'
    )
    return actual_decorator
