from rest_framework import serializers
import re
from .models import *
from django.contrib.auth.models import User
from .models import Profile
from .utils import generate_aub_id


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class AppUserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField()
    date_of_birth = serializers.DateField()
    place_of_birth = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        image = validated_data.pop('image', None)

        user = User.objects.create_user(
            username=self._generate_aub_id(),
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        Profile.objects.create(
            user=user,
            aub_id=user.username,
            gender=validated_data['gender'],
            date_of_birth=validated_data['date_of_birth'],
            phone_number=validated_data['phone_number'],
            image=image,
        )

        return user  # ✅ RETURN USER AGAIN


    def _generate_aub_id(self):
        last = (
            Profile.objects
            .exclude(aub_id__isnull=True)
            .exclude(aub_id__exact='')
            .order_by('-id')
            .first()
        )

        if not last:
            return '000100'

        try:
            last_id = int(last.aub_id)
        except ValueError:
            return '000100'

        return str(last_id + 1).zfill(6)
    
def to_representation(self, instance):
    return instance


    
class LoginByIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_id = data.get("user_id")
        password = data.get("password")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid user ID or password")

        data["user"] = user
        return data

class NewsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'content',
            'image',
            'category',
            'views',
            'created_at',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_id', 'course_name', 'course_info']
    
class CourseInfoSerializer(serializers.ModelSerializer):

    course = serializers.SlugRelatedField(
        slug_field='course_id',
        queryset=Course.objects.all()
    )

    class Meta:
        model = CourseInfo
        fields = ['id', 'course', 'program', 'price_per_semester', 'price_per_year']

class EventMenuSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    event_date = serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = EventMenu
        fields = [
            'id',
            'title',
            'description',
            'image',
            'event_date',
            'is_active',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class BookSerializer(serializers.ModelSerializer):
    book_image = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'book_id',
            'book_title',
            'book_image',
            'description',
            'views',
            'created_at',
        ]

    def get_book_image(self, obj):
        request = self.context.get('request')
        if obj.book_image:
            return request.build_absolute_uri(obj.book_image.url)
        return None



class ExtraCourseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ExtraCourse
        fields = [
            'id',
            'name',
            'price',
            'duration',
            'related_course',
            'image',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class JobPostingSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = [
            'id',
            'title',
            'description',
            'contact',
            'telegram_link',
            'image',
            'is_open',
            'created_at',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'id',
            'degree_level',
            'major',
            'status',
            'created_at',
        ]
        read_only_fields = ['status', 'created_at']
