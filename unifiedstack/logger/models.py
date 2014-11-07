from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Device(models.Model):
    # TODO: Set constants for device title to choose only from
    # a set of networking devices
    device_title = models.charField(max_length=50)
    device_desc = models.CharField(max_length=200)
    def __str__(self):
        return self.title + ": " + self.device_desc
    
class Log(models.Model):
    INFO_TYPE = 'I'
    COMMIT_TYPE = 'C'
    WARNING_TYPE = 'W'
    ERROR_TYPE = 'E'
    LOG_TYPE_CHOICES = (
        (INFO_TYPE, 'Info'),
        (COMMIT_TYPE, 'Commit'),
        (WARNING_TYPE, 'Warning'),
        (ERROR_TYPE, 'Error'),
    )
    log_type = models.CharField(max_length=1, choices=LOG_TYPE_CHOICES,
                                    default=INFO_TYPE)
    device = models.ForeignKey(Device, related_name="logs")
    log_timestamp = models.DateTimeField("Log Time", auto_now=True)
    log_message = models.CharField(max_length=200)
    def __str__(self):
        return str(self.log_timestamp) + self.log_message
    def was_logged_recently(self):
        return self.log_timestamp >= timezone.now() - datetime.timedelta(days=1)
    def __unicode__(self):
        return '%s' % (self.log_message)
    class Meta:
        ordering =  ('log_timestamp',)
