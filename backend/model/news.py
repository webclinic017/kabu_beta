from django.db import models
from backend.model.tag import TAG
from backend.model.label import LABEL
from backend.model.company import COMPANY
from django.utils import timezone

class NEWS(models.Model):
    news_id       = models.AutoField(primary_key=True)
    title         = models.CharField(max_length=200, default="")
    description   = models.CharField(max_length=10000, default="")
    detail_url    = models.CharField(max_length=500, default="")
    class_id      = models.IntegerField(default=0)#0　default    1 china    2 JP     3 USA
    del_flg       = models.IntegerField(default=0)
    checked_flg   = models.IntegerField(default=0)
    url           = models.CharField(max_length=200, default="")

    detail        = models.CharField(max_length=10000, default="")
    tag           = models.ManyToManyField(TAG, blank=True)
    label         = models.ForeignKey(LABEL, on_delete=models.CASCADE,blank=True,null=True)
    create_date   = models.DateField(default=timezone.now)
    company       = models.ManyToManyField(COMPANY, blank=True)
    def __str__(self):
        return f"news_id = {self.news_id}, title = {self.title}, description = {self.description},detail_url = {self.detail_url},class_id = {self.class_id},del_flg = {self.del_flg},checked_flg = {self.checked_flg},url = {self.url},detail = {self.detail},tag = {self.tag.all()},company = {self.company.all()}"

    def by_company(self, company):
        return self.filter(company=company)