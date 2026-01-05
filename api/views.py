from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = AppUserRegisterSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            user = serializer.save()
            profile = user.profile

            return Response(
                {
                    "message": "Registered successfully",
                    "user_id": user.username,
                    "full_name": f"{user.first_name} {user.last_name}",
                    "profile_image": (
                        request.build_absolute_uri(profile.image.url)
                        if profile.image else None
                    ),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "gender": profile.gender,
                    "date_of_birth": profile.date_of_birth,
                    "phone_number": profile.phone_number,
                },
                status=status.HTTP_201_CREATED
            )

        print("REGISTER ERRORS =>", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = user.profile

        return Response({
            "user_id": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": f"{user.first_name} {user.last_name}",
            "gender": profile.gender,
            "date_of_birth": profile.date_of_birth,
            "phone_number": profile.phone_number,
            "profile_image": (
                request.build_absolute_uri(profile.image.url)
                if profile.image else None
            )
        })


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        aub_id = request.data.get("user_id")
        password = request.data.get("password")

        user = authenticate(username=aub_id, password=password)

        if not user:
            return Response(
                {"detail": "Invalid ID or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.username,
        })


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()

        if self.request.query_params.get('featured') == 'true':
            return queryset.filter(is_featured=True)

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CourseInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseInfo.objects.all()
    serializer_class = CourseInfoSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')

        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset

class EventMenuViewSet(ReadOnlyModelViewSet):
    queryset = EventMenu.objects.filter(is_active=True)
    serializer_class = EventMenuSerializer
    permission_classes = [AllowAny]



from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter]
    search_fields = ['book_title', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ExtraCourseViewSet(ReadOnlyModelViewSet):
    queryset = ExtraCourse.objects.all()
    serializer_class = ExtraCourseSerializer
    permission_classes = [AllowAny]

class JobPostingViewSet(ReadOnlyModelViewSet):
    queryset = JobPosting.objects.order_by('-created_at')
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]

from django.contrib.auth import get_user_model

User = get_user_model()


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user_id or not old_password or not new_password:
            return Response(
                {"message": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔐 user_id = username (same as login)
        user = get_object_or_404(User, username=user_id)

        # ❌ WRONG OLD PASSWORD
        if not user.check_password(old_password):
            return Response(
                {"message": "Current password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ SET NEW PASSWORD (IMPORTANT)
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )

class EnrollmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # GET /api/enrollment/
    def list(self, request):
        enrollment = Enrollment.objects.filter(user=request.user).first()
        if not enrollment:
            return Response(
                {"detail": "No enrollment found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    # POST /api/enrollment/
    def create(self, request):
        if Enrollment.objects.filter(user=request.user, status='PENDING').exists():
            return Response(
                {"detail": "You already have a pending enrollment"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH /api/enrollment/{id}/
    def partial_update(self, request, pk=None):
        enrollment = Enrollment.objects.filter(
            id=pk,
            user=request.user
        ).first()

        if not enrollment:
            return Response(
                {"detail": "Enrollment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if enrollment.status != 'PENDING':
            return Response(
                {"detail": "Only pending enrollment can be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        enrollment.status = 'CANCELLED'
        enrollment.save()
        return Response({"detail": "Enrollment cancelled"})
    
class ChangePhoneNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response(
                {"message": "Phone number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = user.profile
        profile.phone_number = phone_number
        profile.save()

        return Response(
            {"message": "Phone number updated successfully"},
            status=status.HTTP_200_OK,
        )

class UpdateProfileImageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        profile = request.user.profile
        image = request.FILES.get("image")

        if not image:
            return Response(
                {"message": "Image is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile.image = image
        profile.save()

        return Response(
            {
                "message": "Profile image updated",
                "profile_image": request.build_absolute_uri(profile.image.url),
            },
            status=status.HTTP_200_OK,
        )
