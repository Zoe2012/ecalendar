#encoding=utf-8
from django.db import models

class Calendar(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=20)
    modified_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.date) + '(' + self.name + ')'


class City(models.Model):
    pinyin = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Device(models.Model):
    identification = models.CharField(max_length=100)
    KIND_OS = (
            ('a', 'Aandroid'),
            ('i', 'iOS'),
            )
    os = models.CharField(max_length=1, choices=KIND_OS)

    def __unicode__(self):
        return self.os + '_' + self.identification

class Activity(models.Model):
    city = models.ForeignKey(City)
    location = models.CharField(blank=True, max_length=200)

    title = models.CharField(max_length=2000)
    content = models.TextField()
    url = models.CharField(max_length=255)
    source = models.CharField(blank=True, max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    weight = models.IntegerField(blank=True, null=True)
    
    PROCESS_STATE = (
        (0, 'new'), # bot 新添加的活动，未审核、不可见状态
        (1, 'public'), # 公开的，已审核，对用户可见，其它所有非public状态都对用户不可见
        (2, 'block'), # 被黑名规则单自动block的数据，不删除这些数据，可能被人工改为public或useless状态
        (3, 'useless'), # 垃圾数据不删除，而是标记为useless，表示已审核但没通过
    )
    status = models.SmallIntegerField(choices=PROCESS_STATE, default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField('Tag', blank=True)

    class Meta:
        unique_together = ('start_date', 'url',)

    def __unicode__(self):
        return self.title

class Reaction(models.Model):
    activity = models.ForeignKey(Activity)
    device = models.ForeignKey(Device)

    like = models.NullBooleanField()
    dislike = models.NullBooleanField()
    clicked = models.NullBooleanField()

    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.activity.title

class Feedback(models.Model):
    content = models.CharField(max_length=10000)
    device = models.ForeignKey(Device)

    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content[:20]

class StartURL(models.Model):
    KIND_STATUS = (
            ('s', 'Submitted'),
            ('i', 'Crawling'),
            ('d', 'Done'),
            ('e', 'Error'),
            )

    url = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=1, choices=KIND_STATUS, default='s')

    modified_time = models.DateTimeField(auto_now=True)
    crawl_start_time = models.DateTimeField(editable=False, blank=True, null=True)
    crawl_end_time = models.DateTimeField(editable=False, blank=True, null=True)

    def __unicode__(self):
        return self.url

class Apk(models.Model):
    version = models.CharField(max_length=10, unique=True)
    apkfile = models.FileField(upload_to='apk/%Y-%m-%d-%H-%M')

    def __unicode__(self):
        return self.version

class Blacklist(models.Model):
    word = models.CharField(max_length=20)

    def __unicode__(self):
        return self.word
