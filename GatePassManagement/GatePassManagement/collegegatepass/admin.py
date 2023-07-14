from django.contrib import admin

# Register your models here.
from collegegatepass.models import StudentModel, PassRequestModel

admin.site.register(StudentModel)
admin.site.register(PassRequestModel)