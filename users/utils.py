from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group, Permission

from decouple import config

USER_TYPE_CHOICES = {
    0: 'Superuser',
    1: 'System Administrator',
    2: 'Board Chairperson',
    3: 'Board Vice-Chair',
    4: 'Board Member',
    5: 'Secretary/C.E.O',
    6: 'Director HR',
    7: 'Legal Officer',
    8: 'Principal HR',
    9: 'HRM & D Officer',
    10: 'Legal Researcher',
    11: 'Records Management Officer',
}


def logout_redirect_uri(request):
    print(request.get_host())
    messages.success(request, f'Signed out successfully')
    id_token = request.session['oidc_id_token']
    auth_url = config('AUTH_URL')
    logout_url = f'{auth_url}/cpsb-openid/end-session/?id_token_hint={id_token}&post_logout_redirect_uri=http://{request.get_host()}/'
    return logout_url


class AuthManager(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(AuthManager, self).create_user(claims)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')

        user.id_number = claims.get('id_number', '')
        user.user_type = claims.get('user_type', '')
        user.user_type_desc = USER_TYPE_CHOICES[user.user_type]

        user.date_of_birth = claims.get('user_profile')[
            0]['fields']['date_of_birth']
        user.gender = claims.get('user_profile')[0]['fields']['gender']

        user.save()

        # IF GROUPS ARE NEEDED, DO THE CONFIGS HERE

        return user

    def verify_claims(self, claims):
        verified = super(AuthManager, self).verify_claims(claims)
        id_number = claims.get('id_number')
        profile = claims.get('profile')
        return verified and id_number and profile
