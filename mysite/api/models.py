from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Task(title={self.title}, description={self.description}, completed={self.completed}, created={self.created})"
    
