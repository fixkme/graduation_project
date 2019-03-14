from django import forms


class LoginForm(forms.Form):
    nickname = forms.CharField(
        label="用户名", max_length=16, widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder':'昵称/手机号', 'required':'required'}))
    pwd = forms.CharField(
        label="密码", max_length=16, widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder':'密码','required':'required'}))
