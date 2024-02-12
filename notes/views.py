# from django.shortcuts import render
# from django.http import HttpResponse, request
from datetime import timedelta
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.views import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Note, User
from .serializers import NoteSerializer, UserSerializer


@api_view(["GET", "POST"])
def notes_list(req):
    if req.method == "GET":
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    elif req.method == "POST":
        data = req.data
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
def note_details(req, pk):
    try:
        note = Note.objects.get(id=pk)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if req.method == "GET":
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    elif req.method == "PATCH":
        serializer = NoteSerializer(note, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif req.method == "DELETE":
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def register_user(req):
    serializer = UserSerializer(data=req.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )


# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(req):
    data = req.data
    try:
        email = data["email"]
        password = data["password"]
    except:
        return APIException("Please provide both email and password")

    user = User.objects.get(email=email)
    if not user:
        return APIException("Invalid Credentials")
    if not user.check_password(password):
        return APIException("Invalid Credentials")

    user_data = UserSerializer(data=user)
    # print(user_data.get_fields)

    refreshToken = RefreshToken.for_user(user)
    accessToken = refreshToken.access_token
    response = Response(
        status=status.HTTP_202_ACCEPTED,
    )

    # if isUser is True:
    response.set_cookie(
        "refresh_token",
        str(refreshToken),
        max_age=timedelta(days=14).seconds,
        httponly=True,
    )
    response.set_cookie(
        "access_token",
        str(accessToken),
        max_age=timedelta(hours=24).seconds,
        httponly=True,
    )
    return response
    # else:
    #     return Response("password wrong", status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def logout_user(req):
    response = Response(status=status.HTTP_202_ACCEPTED)
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")
    logout(req)
    return response
