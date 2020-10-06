from django.db import models

class MEMO(models.Model):
    news_id        =models.ForeignKey('NEWS', on_delete=models.CASCADE, default=0)
    memo_id       = models.IntegerField(primary_key=True)
    memo_content  = models.CharField(max_length=50, default="")
