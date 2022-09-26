from django.db import models

# Create your models here.

class dept(models.Model):
    dept_name=models.CharField(max_length=100)
    salary=models.IntegerField(default=20000)
    def __str__(self) -> str:
        return self.dept_name

class person(models.Model):
    department=models.ForeignKey(dept,null=True,blank=True,on_delete=models.CASCADE,related_name='department')
    name=models.CharField(max_length=200)
    age=models.IntegerField()
