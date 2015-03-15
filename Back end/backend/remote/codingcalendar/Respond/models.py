from django.db import models

class DataSet(models.Model):
    SiteName = models.CharField(max_length=100)
    ContestURL = models.CharField(max_length=100, default="NOURL")
    TOCS = models.DateTimeField()
    TOCE = models.DateTimeField()
    ID = models.AutoField(primary_key = True)
    Description = models.CharField(max_length=500, default = "do attend")
    def __unicode__(self):
    	return self.SiteName

