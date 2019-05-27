from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import UpdatePackage

# By adding 'UpdatePackage' as 'sender' argument we only receive signals from that model
@receiver(post_delete, sender=UpdatePackage)
def on_delete(sender, **kwargs):
    instance = kwargs['instance']
    # ref is the name of the field file of the UpdatePackage model
    # replace with name of your file field
    instance.fileRef.delete(save=False)
