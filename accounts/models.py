from django.conf import settings
from django.db import models

    
from django.contrib.auth.models import AbstractUser # import an abstract user model which is a child of the  django user model
#define a model user that inherits from AbstractUser model
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True) #attribute name defined
    email = models.EmailField(unique=True,null=True)



USERNAME_FIELD = 'username' #username field defined 
REQUIRED_FIELDS = []




RATE_CHOICES = [
	(1, '1 - Trash'),
	(2, '2 - Horrible'),
	(3, '3 - Terrible'),
	(4, '4 - Bad'),
	(5, '5 - OK'),
	(6, '6 - Recommendable'),
	(7, '7 - Good'),
	(8, '8 - Very Good'),
	(9, '9 - Perfect'),
	(10, '10 - Master Piece'), 
]


class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    
    def __str__(self):
        return f"{self.customer.username} rated {self.owner.username} with {str(self.rate)} stars"