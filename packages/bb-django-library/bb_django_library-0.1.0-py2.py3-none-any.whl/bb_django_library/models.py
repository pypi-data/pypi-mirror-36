from django.db import models


class Foo(models.Model):
    bar = models.CharField(max_length=255)
