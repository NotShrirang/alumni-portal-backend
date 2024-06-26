from users.models import (
    AlumniPortalUser,
    Alumni,
    Student,
    Faculty,
    SuperAdmin
)
import requests
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.password_validation import validate_password
from django.db import models
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, Serializer, ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from connection.models import Connection
from connection.serializers import ConnectionSerializer
from skill.serializers import SkillSerializer, UserSkillSerializer
from club.serializers import ClubMemberSerializer


class AlumniPortalUserSerializer(ModelSerializer):
    connections = SerializerMethodField()
    skills = SerializerMethodField()
    cityName = SerializerMethodField()
    isConnected = SerializerMethodField()
    clubs = SerializerMethodField()

    class Meta:
        model = AlumniPortalUser
        fields = ['id', 'email', 'firstName', 'lastName', 'department',
                  'privilege', 'bio', 'resume', 'profilePicture',
                  'city', 'cityName', 'phoneNumber', 'createdAt', 'updatedAt',
                  'isVerified', 'is_active', 'is_admin', 'is_staff',
                  'is_superuser', 'signInMethod', 'connections', 'skills',
                  'clubs', 'isConnected']
        list_fields = fields
        get_fields = fields

    def get_connections(self, obj):
        user_connectionA = obj.userA.filter(
            status='accepted', isActive=True).values_list('userB', flat=True)
        user_connectionB = obj.userB.filter(
            status='accepted', isActive=True).values_list('userA', flat=True)

        connections = set(user_connectionA).union(user_connectionB)

        return len(list(connections))

    def get_skills(self, obj):
        user_skills = obj.skills.all()
        serializer = UserSkillSerializer(user_skills, many=True)
        return serializer.data

    def get_cityName(self, obj):
        if obj.city:
            return f"{obj.city.name}, {obj.city.state.name}, {obj.city.state.country.name}"
        return None

    def get_isConnected(self, obj):
        if self.context['request'].user == AnonymousUser():
            return 'not_connected'
        if Connection.objects.filter(userA=self.context['request'].user, userB=obj, status='accepted', isActive=True).exists(
        ) or Connection.objects.filter(userB=self.context['request'].user, userA=obj, status='accepted', isActive=True).exists():
            return 'accepted'
        elif Connection.objects.filter(userA=self.context['request'].user, userB=obj, status='pending', isActive=True).exists(
        ) or Connection.objects.filter(userB=self.context['request'].user, userA=obj, status='pending', isActive=True).exists():
            return 'pending'
        else:
            return 'not_connected'

    def get_clubs(self, obj):
        user_clubs = obj.clubs.all()
        serializer = ClubMemberSerializer(user_clubs, many=True)
        return serializer.data


class RecommendUserSerializer(ModelSerializer):
    mutualConnections = SerializerMethodField()
    isConnected = SerializerMethodField()

    class Meta:
        model = AlumniPortalUser
        fields = ['id', 'email', 'firstName', 'lastName',
                  'department', 'bio', 'profilePicture', 'mutualConnections',
                  'isConnected']

    def get_mutualConnections(self, obj):
        current_user_connectionA = self.context['request'].user.userA.filter(
            status='accepted', isActive=True).values_list('userB', flat=True)
        current_user_connectionB = self.context['request'].user.userB.filter(
            status='accepted', isActive=True).values_list('userA', flat=True)
        current_user_connections = set(
            current_user_connectionA).union(current_user_connectionB)

        user_connectionA = obj.userA.filter(
            status='accepted', isActive=True).values_list('userB', flat=True)
        user_connectionB = obj.userB.filter(
            status='accepted', isActive=True).values_list('userA', flat=True)

        user_connections = set(user_connectionA).union(user_connectionB)

        mutual_connections = current_user_connections.intersection(
            user_connections)

        mutually_connected_users = AlumniPortalUser.objects.filter(
            id__in=mutual_connections)

        serializer = AlumniPortalUserSerializer(
            mutually_connected_users, many=True, context=self.context)

        return serializer.data

    def get_isConnected(self, obj):
        if Connection.objects.filter(userA=self.context['request'].user, userB=obj, status='accepted', isActive=True).exists(
        ) or Connection.objects.filter(userB=self.context['request'].user, userA=obj, status='accepted', isActive=True).exists():
            return 'accepted'
        elif Connection.objects.filter(userA=self.context['request'].user, userB=obj, status='pending', isActive=True).exists(
        ) or Connection.objects.filter(userB=self.context['request'].user, userA=obj, status='pending', isActive=True).exists():
            return 'pending'
        else:
            return 'not_connected'


class RegisterSerializer(ModelSerializer):
    password = CharField(min_length=8, write_only=True)

    class Meta:
        model = AlumniPortalUser
        fields = ['email', 'password', 'firstName',
                  'lastName', 'department', 'privilege', 'city']

    def create(self, validated_data):
        return AlumniPortalUser.objects.create_user(**validated_data)


class RegisterGoogleSerializer(ModelSerializer):
    token = CharField(required=True)

    class Meta:
        model = AlumniPortalUser
        fields = (
            'token',
        )

    def validate(self, data):
        """
        Check if the user exists.
        """
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={data['token']}"
        response = requests.get(url)
        if (response.status_code == 200):
            response_body = response.json()
            email = response_body["email"]
            user = AlumniPortalUser.objects.filter(email=email)
            if user.exists():
                raise ValidationError(
                    f"User with email {email} already exists")
            data['email'] = email
            return data
        raise ValidationError('invalid token')

    def create(self, validated_data):
        validated_data['is_active'] = True
        validated_data['signInMethod'] = "Google"
        validated_data['isVerified'] = False
        validated_data['privilege'] = "3"
        del validated_data['token']
        user = AlumniPortalUser.objects.create(**validated_data)
        user.save()
        return user


class LoginSerializer(ModelSerializer):
    password = CharField(min_length=6, write_only=True)
    email = CharField(max_length=255)
    tokens = SerializerMethodField()

    def get_tokens(self, obj):
        user = AlumniPortalUser.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = AlumniPortalUser
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.isVerified:
            raise AuthenticationFailed(
                'Account not verified, verify your email.')
        return {
            'email': user.email,
            'tokens': user.tokens
        }


class GoogleLoginSerializer(ModelSerializer):
    accessToken = CharField(write_only=True, required=True)

    class Meta:
        model = AlumniPortalUser
        fields = (
            'accessToken',
        )

    def validate(self, data):
        """
        Check if the user exists.
        """
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={data['accessToken']}"
        response = requests.get(url)
        if (response.status_code == 200):
            response_body = response.json()
            email = response_body["email"]
            user = AlumniPortalUser.objects.filter(email=email)
            if not user.exists():
                raise ValidationError(
                    f"User with email {email} does not exist")
            if not user.first().is_active:
                raise ValidationError(f"User with email {email} is inactive")
            token = RefreshToken.for_user(user.first())
            data = dict()
            data['refresh'] = str(token)
            data['access'] = str(token.access_token)
            return data
        else:
            raise ValidationError('invalid token')


class LogoutSerializer(Serializer):
    refresh = CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class AlumniSerializer(ModelSerializer):
    class Meta:
        model = Alumni
        fields = ['id', 'user', 'batch', 'enrollmentYear', 'passingOutYear']


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'batch', 'enrollmentYear', 'passingOutYear']


class FacultySerializer(ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'user', 'college']


class SuperAdminSerializer(ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'user']


class UpdatePasswordSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True,
                         validators=[validate_password])
    confirmPassword = CharField(write_only=True, required=True)
    oldPassword = CharField(write_only=True, required=True)

    class Meta:
        model = AlumniPortalUser
        fields = ('oldPassword', 'password', 'confirmPassword')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def validate_oldPassword(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError(
                {"oldPassword": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise ValidationError(
                {"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()
        return instance
