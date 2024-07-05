from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel=get_user_model()

class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        
        # this is not possible and required if user or email address is unique 
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username).order_by('id').first() )

        if user.check_password(password) and self.user_can_authenticate(user):
                return user