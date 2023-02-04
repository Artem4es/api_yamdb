from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)


class CreateReadDeleteModelViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
):
    """Get instances, create instance, delete instance"""


class CreateReadUpdateDeleteModelViewset(
    CreateReadDeleteModelViewSet,
    viewsets.GenericViewSet,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    """Get insatnces or instance, create, update, delete"""
