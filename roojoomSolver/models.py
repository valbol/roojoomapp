from django.db import models
from django.forms import ModelForm


class Issue(models.Model):
    ON = 'ON'
    OFF = 'OFF'
    BLINK = 'BLINK'
    LIGHT_STATUS_CHOICES=[(ON, 'On'),(OFF, 'Off'), (BLINK, 'Blink')]
    
    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'
        ordering = ['created_at']
  
    user_id = models.PositiveIntegerField()
    issue_description = models.TextField(max_length=300)
    serial = models.CharField(max_length=64, help_text="Example for a serial 24-X-125447-DC")
    light_status1 = models.CharField(choices=LIGHT_STATUS_CHOICES, default=OFF, max_length=5)
    light_status2 = models.CharField(choices=LIGHT_STATUS_CHOICES, default=OFF, max_length=5)
    light_status3 = models.CharField(choices=LIGHT_STATUS_CHOICES, default=OFF, max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    resolution = models.CharField(max_length=20 ,default='n/a')

    def __str__(self) -> str:
        return f"user_id: {self.user_id} timestamp: {self.created_at}"

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['user_id', 'issue_description', 'serial' , 
                'light_status1','light_status2','light_status3']