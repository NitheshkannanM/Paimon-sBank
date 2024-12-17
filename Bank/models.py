from django.db import models

class accounts(models.Model):
    Name = models.CharField(max_length=50)
    userid = models.CharField(max_length=10, unique=True)
    Email = models.EmailField()
    phone_no = models.IntegerField(unique=True)
    passwords = models.CharField(max_length=120)
    moneybox=models.IntegerField(default=0)
    depost=models.IntegerField(default=0)
    withdrawls=models.IntegerField(default=0)
    historys=models.TextField(null=True,blank=True)
    timestraps=models.DateTimeField(null=True,blank=True)
