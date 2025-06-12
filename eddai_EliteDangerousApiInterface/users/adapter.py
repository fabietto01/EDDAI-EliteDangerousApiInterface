from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def populate_user(self, request, sociallogin:SocialLogin, data):
        user = super().populate_user(request, sociallogin, data)
        if sociallogin.provider.id == 'frontier':
            user.username = data.get('firstname', '') + ' ' + data.get('lastname', '')
        return user
    