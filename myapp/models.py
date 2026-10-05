from django.db import models
# ★ 原本如果只有 Student，這裡加 Scorelist
from .models import *

#Student 資料表的 Model(Table Name: student)
class Student(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=20, blank=False)
    csex =  models.CharField(max_length=1, blank=False, default='F')
    # cBirthday = models.DateField(auto_now_add=True, null=False)
    #這個參數的預設值也為False，設定為True時，會在model物件第一次被建立時，
    #將欄位的值設定為建立時的時間，以後修改物件時，欄位的值不會再更新。
    #cBirthday = models.DateField(auto_now=True, null=False)
    #這個參數的預設值為false，當設定為true時，能夠在儲存該欄位時，
    #將其值設為目前時間，並且每次修改model，都會自動更新
    cbirthday = models.DateField(null=True, blank=True)
    cemail = models.CharField(max_length=100, blank=False)
    cphone = models.CharField(max_length=50, blank=False)
    caddr = models.CharField(max_length=255, blank=False)

    
  # ★ 新增：
    # 告訴 Django：
    # students 這個 Model 不要使用預設的 myapp_students
    # 而是使用 MySQL 現有且已有學生資料的 myapp_student
    class Meta:
        db_table = 'myapp_student'


    def __str__(self):
        return f"{self.cname} ({self.cid})"


# Permissions 資料表的 Model
class Permissions(models.Model):
    cID = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='cID_id')
    
    class Meta:
        db_table = 'myapp_permissions'
    
    def __str__(self):
        return f"Permissions for {self.cID}"