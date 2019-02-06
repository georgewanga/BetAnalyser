from django.db import models


class HomeQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class HomeManager(models.Manager):
    def get_queryset(self):
        return HomeQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()


class Home(models.Model):
    match_date = models.DateTimeField(unique=True)
    home_team = models.CharField(max_length=120)
    away_team = models.CharField(max_length=120)
    soccerway_url = models.CharField(max_length=255,null=True,blank=True)
    betin_url = models.CharField(max_length=255,null=True,blank=True)
    table_score = models.IntegerField(default=0)
    p_table_score = models.CharField(max_length=50)
    last_five_score = models.IntegerField(default=0)
    p_last_five_score = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = HomeManager()

    def __str__(self):
        return self.home_team+' vs '+self.away_team

    class Meta:
        verbose_name_plural = "Home"

    @property
    def name(self):
        return self.soccerway_url
