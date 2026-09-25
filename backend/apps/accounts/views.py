from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer
from .services.otp_service import send_otp, verify_otp, consume_verified_session

User = get_user_model()


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            try:
                from .tracking_models import LoginLog
                user = User.objects.filter(email=request.data.get("email")).first()
                if user:
                    ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or request.META.get("REMOTE_ADDR")
                    LoginLog.objects.create(user=user, ip_address=ip or None)
            except Exception:
                pass
        return response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data.get("phone_number", "").strip()
        otp_session_id = request.data.get("otp_session_id", "").strip()
        if phone:
            if not otp_session_id:
                return Response({"detail": "OTP verification required for mobile registration."}, status=status.HTTP_400_BAD_REQUEST)
            verified_phone = consume_verified_session(otp_session_id)
            if not verified_phone:
                return Response({"detail": "OTP session invalid or expired. Verify mobile first."}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({"user": UserSerializer(user).data, "access": str(refresh.access_token), "refresh": str(refresh)}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
        except (KeyError, TokenError):
            return Response({"detail": "Invalid or missing refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user


class OTPSendView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        phone = request.data.get("phone_number", "").strip()
        if not phone:
            return Response({"detail": "phone_number is required."}, status=400)
        if len(phone.replace("+", "").replace(" ", "")) < 10:
            return Response({"detail": "Enter a valid 10-digit mobile number."}, status=400)
        result = send_otp(phone)
        if not result["sent"]:
            return Response({"detail": "Could not send OTP. Try again."}, status=500)
        return Response({"session_id": result["session_id"], "phone_number": result["phone_number"], "detail": "OTP sent."})


class OTPVerifyView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        session_id = request.data.get("session_id", "").strip()
        otp_input = request.data.get("otp", "").strip()
        if not session_id or not otp_input:
            return Response({"detail": "session_id and otp are required."}, status=400)
        result = verify_otp(session_id, otp_input)
        if not result["verified"]:
            return Response({"detail": result["error"]}, status=400)
        return Response({"verified": True, "phone_number": result["phone_number"], "detail": "Mobile verified."})


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email", "")
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            return Response({"detail": "Reset link generated.", "uid": uid, "token": token})
        return Response({"detail": "If that email exists, a reset link was sent."})


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            uid = force_str(urlsafe_base64_decode(request.data["uid"]))
            user = User.objects.get(pk=uid)
        except (KeyError, User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"detail": "Invalid reset link."}, status=400)
        if not default_token_generator.check_token(user, request.data.get("token", "")):
            return Response({"detail": "Invalid or expired token."}, status=400)
        new_password = request.data.get("new_password", "")
        if len(new_password) < 8:
            return Response({"detail": "Password must be at least 8 characters."}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password reset successful."})


# ── Admin views ──────────────────────────────────────────────────────────────

class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if not self.request.user.is_admin_role:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        qs = User.objects.all().order_by("-date_joined")
        role = self.request.query_params.get("role")
        if role: qs = qs.filter(role=role)
        return qs


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    def get_permissions(self):
        from .permissions import IsAdminRole
        return [IsAdminRole()]
    def get_serializer_class(self):
        from rest_framework import serializers as s
        class AdminUserSerializer(UserSerializer):
            role = s.ChoiceField(choices=User.Role.choices)
            class Meta(UserSerializer.Meta):
                read_only_fields = ("id", "is_staff", "date_joined")
        return AdminUserSerializer


class AdminAnalyticsView(APIView):
    def get_permissions(self):
        from .permissions import IsAdminRole
        return [IsAdminRole()]
    def get(self, request):
        from datetime import timedelta
        from django.utils import timezone
        from django.db.models import Count
        from .tracking_models import LoginLog, PageView
        today = timezone.now().date()
        thirty_ago = timezone.now() - timedelta(days=30)
        by_role = {row["role"]: row["count"] for row in User.objects.values("role").annotate(count=Count("id"))}
        return Response({
            "totalUsersByRole": by_role,
            "totalLogins": LoginLog.objects.count(),
            "todayLogins": LoginLog.objects.filter(logged_in_at__date=today).count(),
            "pageViewsCount": PageView.objects.count(),
            "activeUsers": User.objects.filter(is_staff=False, last_login__gte=thirty_ago).count(),
        })
