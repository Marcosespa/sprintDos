import requests
from social_core.backends.oauth import BaseOAuth2
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = "auth0"
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = "POST"
    EXTRA_DATA = [
        ('picture', 'picture'),
    ]

    def authorization_url(self):
        """Return the authorization endpoint."""
        return "https://" + self.setting("DOMAIN") + "/authorize"

    def access_token_url(self):
        """Return the access token endpoint."""
        return "https://" + self.setting("DOMAIN") + "/oauth/token"

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        url = "https://" + self.setting("DOMAIN") + "/userinfo"
        headers = {'authorization': 'Bearer ' + response['access_token']}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()

        return {
            "username": userinfo.get("nickname") or userinfo.get("name") or userinfo.get("email", ""),
            "first_name": userinfo.get("name", ""),
            "picture": userinfo.get("picture", ""),
            "user_id": userinfo.get("sub", ""),
            "email": userinfo.get("email", "")
        }

def getRole(request):
    try:
        user = request.user
        # Intentar obtener el rol del caché primero
        cache_key = f'user_role_{user.id}'
        cached_role = cache.get(cache_key)
        if cached_role:
            return cached_role

        auth0user = user.social_auth.filter(provider="auth0")[0]
        accessToken = auth0user.extra_data['access_token']
        url = "https://dev-rgo1o3badtq3r0pa.us.auth0.com/userinfo"
        headers = {'authorization': 'Bearer ' + accessToken}
        
        resp = requests.get(url, headers=headers)
        
        if resp.status_code == 429:
            # Si hay rate limiting, usar el rol cacheado anterior o un rol por defecto
            logger.warning(f"Rate limit hit for user {user.id}")
            return cache.get(cache_key, "Usuario")
            
        if resp.status_code != 200:
            logger.error(f"Error getting role: {resp.status_code} - {resp.text}")
            return "Usuario"

        userinfo = resp.json()
        
        # Intenta obtener el rol de diferentes maneras posibles
        role = (userinfo.get('dev-rgo1o3badtq3r0pa.us.auth0.com/role') or 
                userinfo.get('role') or 
                userinfo.get('https://dev-rgo1o3badtq3r0pa.us.auth0.com/roles', ['Usuario'])[0])
        
        # Guardar en caché por 1 hora
        cache.set(cache_key, role, 3600)
        
        return role
        
    except Exception as e:
        logger.error(f"Error in getRole: {str(e)}")
        return "Usuario"
