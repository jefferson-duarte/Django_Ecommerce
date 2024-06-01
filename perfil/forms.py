from django import forms
from .models import Perfil
from django.contrib.auth.models import User


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirm Password'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
            'password2',
            'email',
        )

    def clean(self):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        # print(cleaned)

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        # print(usuario_db)
        print(password2_data)

        error_msg_user_exist = 'Usuário já existe.'
        error_msg_email_exist = 'E-mail já existe.'
        error_msg_password_match = 'As senha não conferem.'
        error_msg_password_short = 'A senha precisa ter pelo menos 6 caracteres.'  # noqa:E501
        error_msg_required_field = 'Este campo é obrigatório.'

        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exist

            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exist

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match  # noqa:E501
                    validation_error_msgs['password2'] = error_msg_password_match  # noqa:E501

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short  # noqa:E501
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exist

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exist

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            if not password2_data:
                validation_error_msgs['password2'] = error_msg_required_field

            if password_data != password2_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short

        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)
