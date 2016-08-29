from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


# class StudentRegisterForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=20)
#     password = forms.CharField(widget=forms.PasswordInput)
#     email = forms.EmailField(label='Email', max_length=50)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     first_name = forms.CharField(label='First Name', max_length=20)
#     last_name = forms.CharField(label='Last Name', max_length=20)
#     student_id = forms.IntegerField(label='Student ID')
#
#
# class TeacherRegisterForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=20)
#     password = forms.CharField(widget=forms.PasswordInput)
#     email = forms.EmailField(label='Email', max_length=50)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     first_name = forms.CharField(label='First Name', max_length=20)
#     last_name = forms.CharField(label='Last Name', max_length=20)
