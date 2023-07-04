import datetime

from django.db import models
from django.db import connection
from django.utils.timezone import now
from django.db.models import SET_NULL, CASCADE
from django.contrib.auth.models import User


class polygon(models.Model):
    id = models.AutoField(primary_key=True)
    polygonid = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    pop = models.FloatField(null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True, default='swrCat', editable=False)
    wkt = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)

class site(models.Model):
    id = models.AutoField(primary_key=True)
    siteID = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    publicHealthDepartment = models.CharField(max_length=200, null=True, blank=True)
    healthRegion = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    geoLat = models.FloatField(null=True, blank=True, default=None)
    geoLong = models.FloatField(null=True, blank=True, default=None)
    polygonID = models.ForeignKey(polygon, on_delete = SET_NULL, null = True, blank = True)
    link = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)

class uwtp(models.Model):
    id = models.AutoField(primary_key=True)
    uwwName = models.CharField(max_length=200, null=True, blank=True)
    station = models.CharField(max_length=200, null=True, blank=True)
    agg_name = models.CharField(max_length=200, null=True, blank=True)
    station_id = models.ForeignKey(site,on_delete = SET_NULL, null = True, blank = True)
    uwwLatitud = models.FloatField(null=True, blank=True, default=None)
    uwwLongitu = models.FloatField(null=True, blank=True, default=None)
    agg_type = models.CharField(max_length=200, null=True, blank=True)
    init = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.uwwName



class covtype(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    typedef = models.CharField(max_length=200, null=True, blank=True)
    unitdef = models.CharField(max_length=200, null=True, blank=True)
    units = models.CharField(max_length=200, null=True, blank=True)
    idtype = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.type

class sampledata(models.Model):
    id = models.AutoField(primary_key=True)
    sampleid = models.CharField(max_length=200, null=True, blank=True)
    location = models.ForeignKey(uwtp, on_delete = SET_NULL, null = True, blank = True)
    submited_datetime = models.DateTimeField(null=True, blank=True, default=now)
    datestart = models.DateField(null=True, blank=True)
    dateend = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    # instrumentid = models.CharField(max_length=200, null=True, blank=True)
    # reporterid = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True, default='rawWW', editable=False)
    collection = models.CharField(max_length=200, null=True, blank=True, default='cpTP24h', editable=False)
    # preTreatment = models.CharField(max_length=200, null=True, blank=True)
    # pooled = models.CharField(max_length=200, null=True, blank=True)
    # children = models.CharField(max_length=200, null=True, blank=True)
    # parent = models.CharField(max_length=200, null=True, blank=True)
    # sizeL = models.CharField(max_length=200, null=True, blank=True)
    # index = models.CharField(max_length=200, null=True, blank=True)
    # fieldSampleTempC = models.CharField(max_length=200, null=True, blank=True)
    # shippedOnIce = models.CharField(max_length=200, null=True, blank=True)
    # storageTempC = models.CharField(max_length=200, null=True, blank=True)
    # qualityFlag = models.CharField(max_length=200, null=True, blank=True)
    loginname = models.ForeignKey(User, on_delete=SET_NULL,null = True, blank = True)


class wwmeasure(models.Model):
    id = models.AutoField(primary_key=True)
    wwmeasureid = models.CharField(max_length=200, null=True, blank=True)
    # reporterid = models.CharField(max_length=200, null=True, blank=True)
    sampleid = models.ForeignKey(sampledata, on_delete = SET_NULL, null = True, blank = True)
    # labID = models.CharField(max_length=200, null=True, blank=True)
    # assayMethodID = models.CharField(max_length=200, null=True, blank=True)
    submited_datetime = models.DateTimeField(null=True, blank=True, default=now)
    analysisdate = models.DateField(null=True, blank=True)
    reportdate = models.DateField(null=True, blank=True)
    fractionAnalyzed = models.CharField(max_length=200, null=True, blank=True, default='liquid')
    covtype = models.ForeignKey(covtype, on_delete = SET_NULL, null = True, blank = True)
    value = models.FloatField(null=True, blank=True, default=None)
    # aggregation = models.CharField(max_length=200, null=True, blank=True)
    # index = models.CharField(max_length=200, null=True, blank=True)
    # qualityFlag = models.CharField(max_length=200, null=True, blank=True)
    # accessToPublic = models.CharField(max_length=200, null=True, blank=True)
    # accessToAllOrg = models.CharField(max_length=200, null=True, blank=True)
    # accessToPHAC = models.CharField(max_length=200, null=True, blank=True)
    # accessToLocalHA = models.CharField(max_length=200, null=True, blank=True)
    # accessToProvHA = models.CharField(max_length=200, null=True, blank=True)
    # accessToOtherProv = models.CharField(max_length=200, null=True, blank=True)
    # accessToDetails = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    # loginname = models.ForeignKey(User, on_delete=SET_NULL,null = True, blank = True)

class trends(models.Model):
    id = models.AutoField(primary_key=True)
    submited_datetime = models.DateTimeField(null=True, blank=True, default= now)
    fromdate = models.DateField(null=True, blank=True)
    todate = models.DateField(null=True, blank=True)
    loginname = models.ForeignKey(User, on_delete=SET_NULL,null = True, blank = True)
    samplestationid = models.ForeignKey(uwtp, on_delete = SET_NULL, null = True, blank = True)
    value = models.FloatField(null=True, blank=True, default=None)

class variantType(models.Model):
    id = models.AutoField (primary_key = True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__ (self):
        return self.name

class variants(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.ForeignKey(uwtp, on_delete=SET_NULL, null = True, blank = True)
    sampleid = models.CharField(max_length=200, null=True, blank=True)
    Lineage = models.CharField(max_length=200, null=True, blank=True)
    VariantType = models.ForeignKey(variantType, on_delete=SET_NULL, null = True, blank = True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    submited_datetime = models.DateTimeField(null=True, blank=True, default=now)
    datestart = models.DateField(null=True, blank=True)
    dateend = models.DateField(null=True, blank=True)
    loginname = models.ForeignKey(User, on_delete=SET_NULL,null = True, blank = True)
