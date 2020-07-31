from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validate(self, post_data):
        errors = {}
    # First Name - required; at least 2 characters; letters only
        if len(post_data['form_fn']) < 2:
            errors['form_fn'] = "First name must be two characters or more."
        elif post_data['form_fn'].isalpha() == False:
            errors['form_fn'] = "First name must only cantain letters."
    # Last Name - required; at least 2 characters; letters only
        if len(post_data['form_ln']) < 2:
            errors['form_ln'] = "Last name must be two characters or more."
        elif post_data['form_ln'].isalpha() == False:
            errors['form_ln'] = "Last name must only cantain letters."
    # Email - required; valid format
        if not EMAIL_REGEX.match(post_data['form_em']):
            errors['form_em'] = "Email must be a valid format."
        elif len(User.objects.filter(email = post_data['form_em'])) > 0:
            errors['form_em'] = "Email already registered, please login."
    # Password - required; at least 8 characters; matches password confirmation
        if len(post_data['form_pw']) < 8:
            errors['form_pw'] = "Password must be longer than 8 characters."
        if post_data['form_pw'] != post_data['form_cpw']:
            errors['form_pw'] = "Passwords do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f'Name: {self.first_name} {self.last_name} ID: {self.id}'

class TrailManager(models.Manager):
    def validate_trail(self, postData):
        errors = {}
        if len(postData['trail_name']) < 3:
            errors['trail_name'] = "Trail name must consist of at least 3 characters"
        if len(postData['location']) < 3:
            errors['location'] = "A location must be provided"
        return errors

class Trail(models.Model):
    trail_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    elevation = models.CharField(max_length=10)
    difficulty = models.CharField(max_length=255)
    desc = models.TextField()
    creator = models.ForeignKey(User, related_name="created_hike", on_delete=models.CASCADE)

    objects = TrailManager()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)