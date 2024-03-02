from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for My Awesome Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def get_user_avatar(self):

        profile = self.profile
        print('\n\n')
        print(profile)
        print('\n\n')
        image = profile.image.url
        print('\n\n')
        print(image)
        print('\n\n')
        if image:
            return image
        return None



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="profile")
    image = models.ImageField(upload_to="images/profile/", blank=True, null=True)





