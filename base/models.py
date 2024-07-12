from django.db import models

# Create your models here.
# A class represents a table.
class Room(models.Model):
    #host=
    #topic=
    name=models.CharField(max_length=200)
    description= models.TextField(null=True, blank=True) 
    # () cannot be blank otherwise the table cannot have any value.
    # participants=
    updated=models.DateTimeField(auto_now=True)
    # whenever save method is called, take a snapshot of the table at that instance, automatically. auto_now takes a snapshot everytime table is saved.TIME ROOM IS UPDATED
    created= models.DateTimeField(auto_now_add=True)
    # this takes a snapshot time when the table is created.so it will never change. TIME WHEN THE ROOM IS CREATED
    def __str__(self):
        return self.name
    # the __str__ method is automatically called, and it returns the name of the item
    # The __str__ method is used to provide a readable string representation of an object. This string representation is what you see when you print the object or when you see the object in a Django admin interface or in a Django template.
    # migrations folder has files that contain a list of sql commands