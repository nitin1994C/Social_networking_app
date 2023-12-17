from .models import User, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# @receiver(post_save, sender=User)
def post_save_form_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('user has been created')
    else:
        # for Updating the user
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)

post_save.connect(post_save_form_signal, sender=User)


