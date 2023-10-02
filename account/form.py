from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterCustomerForm(UserCreationForm):
    class _Meta:
        model = User,
        fields = ['email', 'username']
