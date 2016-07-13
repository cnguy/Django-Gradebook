from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    # #
    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     if not user:
    #         raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
    #     return self.cleaned_data
    # #
    # def login(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     return user


class StudentRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=20)
    last_name = forms.CharField(label='Last Name', max_length=20)
    student_id = forms.IntegerField(label='Student ID')


class TeacherRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', max_length=20)
    last_name = forms.CharField(label='Last Name', max_length=20)
