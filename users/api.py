from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied

from django.core.mail import EmailMessage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi as openapi
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.parsers import (
    FileUploadParser,
    FormParser,
    JSONParser,
    MultiPartParser
)

from core.permissions import IsUserOrManager, IsAuthorizedToAdd
from . serializers import UserSerializer, UserDetailSerializer, LoginSerializer
from . models import User
from files.methods import is_mediauploadx_editor, is_mediauploadx_editor


@swagger_auto_schema(
    methods=['post'],
    manual_parameters=[],
    tags=['Users'],
    operation_summary='Contact user',
    operation_description='Contact user through email, if user has set this option',
)
@api_view(["POST"])
def contact_user(request, username):
    if not request.user.is_authenticated:
        return Response(
            {"detail": "request need be authenticated"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    user = User.objects.filter(username=username).first()
    if user and (user.allow_contact or is_mediauploadx_editor(request.user)):
        from_email = request.user.email
        subject = f"[{settings.PORTAL_NAME}] - Message from {from_email}"
        body = request.data.get("body")
        body = """
You have received a message through the contact form\n
Sender name: %s
Sender email: %s\n
\n %s
""" % (
            request.user.name,
            from_email,
            body,
        )
        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            reply_to=[from_email],
        )
        email.send(fail_silently=True)

    return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (JSONParser, MultiPartParser,
                      FormParser, FileUploadParser)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', type=openapi.TYPE_INTEGER,
                              in_=openapi.IN_QUERY, description='Page number'),
        ],
        tags=['Users'],
        operation_summary='List users',
        operation_description='Paginated listing of users',
    )
    def get(self, request, format=None):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        users = User.objects.filter()
        location = request.GET.get("location", "").strip()
        if location:
            users = users.filter(location=location)
        
        page = paginator.paginate_queryset(users, request)

        serializer = UserSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

class UserDetail(APIView):
    """"""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrManager)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get_user(self, username):
        try:
            user = User.objects.get(username=username)
            # this need be explicitly called, and will call
            # has_object_permission() after has_permission has succeeded
            self.check_object_permissions(self.request, user)
            return user
        except PermissionDenied:
            return Response({"detail": "not enough permissions"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='username', type=openapi.TYPE_STRING, in_=openapi.IN_PATH, description='username', required=True),
        ],
        tags=['Users'],
        operation_summary='List user details',
        operation_description='Get user details',
    )
    def get(self, request, username, format=None):
        # Get user details
        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        serializer = UserDetailSerializer(user, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="logo", in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True, description="logo"),
            openapi.Parameter(name="description", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="description"),
            openapi.Parameter(name="name", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="name"),
            openapi.Parameter(name='username', type=openapi.TYPE_STRING, in_=openapi.IN_PATH, description='username', required=True),
        ],
        tags=['Users'],
        operation_summary='Edit user details',
        operation_description='Post user details - authenticated view',
        responses={201: openapi.Response('response description', UserDetailSerializer), 400: 'bad request'},
    )
    def post(self, request, username, format=None):
        # USER
        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        serializer = UserDetailSerializer(user, data=request.data, context={"request": request})
        if serializer.is_valid():
            logo = request.data.get("logo")
            if logo:
                serializer.save(logo=logo)
            else:
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[],
        tags=['Users'],
        operation_summary='Xto_be_written',
        operation_description='to_be_written',
    )
    def put(self, request, uid, format=None):
        # ADMIN
        user = self.get_user(uid)
        if isinstance(user, Response):
            return user

        if not request.user.is_superuser:
            return Response({"detail": "not allowed"}, status=status.HTTP_400_BAD_REQUEST)

        action = request.data.get("action")
        if action == "feature":
            user.is_featured = True
            user.save()
        elif action == "unfeature":
            user.is_featured = False
            user.save()

        serializer = UserDetailSerializer(user, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[],
        tags=['Users'],
        operation_summary='to_be_written',
        operation_description='to_be_written',
    )
    def delete(self, request, username, format=None):
        # Delete a user
        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserWhoami(generics.RetrieveAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    @swagger_auto_schema(
        tags=['Users'],
        operation_summary='Whoami user information',
        operation_description='Whoami user information',
        responses={200: openapi.Response('response description', UserDetailSerializer), 403: 'Forbidden'},
    )
    def get(self, request, *args, **kwargs):
        return super(UserWhoami, self).get(request, *args, **kwargs)


class UserToken(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        tags=['Users'],
        operation_summary='Get a user token',
        operation_description="Returns an authenticated user's token",
        responses={200: 'token', 403: 'Forbidden'},
    )
    def get(self, request, *args, **kwargs):
        token = Token.objects.filter(user=request.user).first()
        if not token:
            token = Token.objects.create(user=request.user)

        return Response({'token': str(token)}, status=200)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    @swagger_auto_schema(
        tags=['Users'],
        operation_summary='Login url',
        operation_description="Login url endpoint. According to what the portal provides, you may provide username and/or email, plus the password",
        manual_parameters=[
            openapi.Parameter(name="username", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="username"),
            openapi.Parameter(name="email", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description="email"),
            openapi.Parameter(name="password", in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description="password"),
        ],
        responses={200: openapi.Response('user details', LoginSerializer), 404: 'Bad request'},
    )
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
