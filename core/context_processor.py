from .models import UserCredential


def aside_bar(request):
    try:
        user_credential = UserCredential.objects.get(user=request.user.id)
    except UserCredential.DoesNotExist:
        user_credential = None
    return {'user_credential': user_credential}
