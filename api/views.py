from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser

from api.serializers import UserSerializer, NoteSerializer
from notes.models import Note


class UserList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'message': 'Deleted'}, status=200)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'message': 'Deleted'}, status=200)
