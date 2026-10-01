from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status


class LoginView(APIView):
    """
    Logs the demo user in and sets Django's default session cookie
    (named 'sessionid'), matching the Cookie: sessionid=<value> shown
    in the dissertation's Break evidence.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)  # sets the sessionid cookie on the response
        return Response({"detail": "Logged in.", "username": user.username})


class ProfileView(APIView):
    """
    The endpoint under test in 5.3. Returns the authenticated user's
    account data. Whether this data can be READ by a cross-origin script
    depends entirely on the CORS configuration in settings.py — this view
    itself does not change between the vulnerable and fixed states.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email or "joe@example.com",
            "address": "221B Fake Street",
            "api_key": "sk_live_FAKE_123456789",
        })
