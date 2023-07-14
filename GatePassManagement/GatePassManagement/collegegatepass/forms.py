from django.forms import Form, CharField, PasswordInput, FileField


class StudentForm(Form):
    rno=CharField(max_length=50)
    password=CharField(max_length=50)
    name=CharField(max_length=50)
    email=CharField(max_length=50)
    mobile=CharField(max_length=50)
    year=CharField(max_length=50)
    section=CharField(max_length=50)
    branch=CharField(max_length=50)
    photo =FileField()

class PassRequestForm(Form):
    date=CharField(max_length=50)
    time=CharField(max_length=50)
    reason=CharField(max_length=50)

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class DepartmentLoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())
    branch = CharField(max_length=20)
