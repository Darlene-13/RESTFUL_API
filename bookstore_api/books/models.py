from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    language= models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(autor_now=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['genre']),
            models.Index(fields=['language']),
        ]

class PriceHistory (models.Model):
    book = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank= True)

    def __str__(self):
        return f"{self.book.title}- {self.price}- {self.start_date}"
    
    class Meta:
        ordering = ['-start_date']

