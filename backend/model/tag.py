from django.db import models
from backend.model.tagkubun import TAGKUBUN


class TAG(models.Model):
    tag_id       = models.AutoField(primary_key=True)
    tag_name     = models.CharField(max_length=50, default="")
    kubun_id     = models.ForeignKey("backend.TAGKUBUN", on_delete=models.CASCADE,blank=True,null=True)



