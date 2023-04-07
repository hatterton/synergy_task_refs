from django.db import models


class UserModel(models.Model):
    id = models.CharField(max_length=70, primary_key=True)
    ref_level = models.IntegerField()
    team_size = models.IntegerField()
    balance = models.IntegerField()

    parent = models.ForeignKey("UserModel", null=True, related_name="refs", on_delete=models.SET_NULL)
