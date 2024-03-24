from rest_framework.authentication import TokenAuthentication


class TokenAuthSupportCookie(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support cookie based authentication
    """
    def authenticate(self, request):
        # Check if 'auth_token' is in the request cookies.
        # Give precedence to 'Authorization' header.
        if 'token' in request.COOKIES and len(request.COOKIES.get('token')) == 40 and \
                        'HTTP_AUTHORIZATION' not in request.META:
            return self.authenticate_credentials(
                request.COOKIES.get('token')
            )
        return super().authenticate(request)