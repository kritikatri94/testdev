from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SigupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username']
