from django.db import models

class Candidate(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    joined_date = models.DateField(null=True)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f'{self.firstname} - {self.lastname}'
    

class UserPDF(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    file = models.FileField(upload_to='user_pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"