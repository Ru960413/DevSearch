from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile

from django.conf import settings
from django.core.mail import send_mail 



def profileUpdated(sender, instance, created, **kwargs):
    # when a user is created, a user profile is automatically created
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email= user.email,
            name=user.first_name,
        )
        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'

        send_mail(
            subject, 
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently = False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    # only update the profile if the user is in database
    if created == False:
        user.first_name = profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()


# when we delete the user from Profile in admin, it works fine.
# but then when we delete user from User in admin a "DoesNotExist" error is raised, because when the user is deleted its profile has already been deleted by "ON_DELETE", hence we'll need a try and except here
def deleteUser(sender, instance, **kwargs):
    try:
        print("Deleting user...")
        user = instance.user
        user.delete()

    except User.DoesNotExist:
        print("User does not exist. This has to do with the relationship between User and Profile.")


# To receive a signal, register a receiver function using the Signal.connect() method. The receiver function is called when the signal is sent. All of the signal’s receiver functions are called one at a time, in the order they were registered.
    
# connect a receiver to a signal(post_save here) 
# you can register to receive signals sent only by particular senders, the sender will be the model class being saved, so you can indicate that you only want signals sent by some model
post_save.connect(profileUpdated, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)