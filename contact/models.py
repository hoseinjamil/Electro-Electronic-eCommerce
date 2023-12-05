from django.db import models

class ContactUs(models.Model):
    name= models.CharField(max_length=20)
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    body=models.CharField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject