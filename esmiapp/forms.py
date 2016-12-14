from django.contrib.auth.forms import UserCreationForm
from esmiapp.models import Users


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'first_name', 'last_name', 'middle_name', 'birthday', 'phonenumber',
                  'password1', 'password2')
