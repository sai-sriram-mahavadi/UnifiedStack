from django.db import models

# Create your models here.
class Device(models.Model):
    # TODO: Set constants for device title to choose only from
    # a set of networking devices
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.title + ": " + self.desc
    
class Log(models.Model):
    INFO_LEVEL = 'I'
    COMMIT_LEVEL = 'C'
    WARNING_LEVEL = 'W'
    ERROR_LEVEL = 'E'
    LOG_LEVEL_CHOICES = (
        (INFO_LEVEL, 'Info'),
        (COMMIT_LEVEL, 'Commit'),
        (WARNING_LEVEL, 'Warning'),
        (ERROR_LEVEL, 'Error'),
    )
    level = models.CharField(max_length=1, choices=LOG_LEVEL_CHOICES,
                                    default=INFO_LEVEL)
    device = models.ForeignKey(Device, related_name="logs")
    timestamp = models.DateTimeField("Log Time", auto_now=True)
    message = models.CharField(max_length=200)
    def __str__(self):
        return str(self.timestamp) + self.message
    def was_logged_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)
    def __unicode__(self):
        return '%s' % (self.message)
    class Meta:
        ordering =  ('timestamp',)

class ConsoleLog(models.Model):
    console_message = models.CharField(max_length=100, blank=True, default="")
    console_summary = models.CharField(max_length=50)
