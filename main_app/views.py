from django.http import HttpResponse, HttpRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from charity import settings
from main_app import models
from main_app import serializers
from rest_framework import mixins


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class AccountsList(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoriesList(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        """Keep only those categories that translated to current language."""
        if self.request.language != settings.DEFAULT_LANGUAGE:
            return models.Category.objects.exclude(en_name__isnull=True)

        return models.Category.objects.all()


class ProjectList(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Project.objects.filter(is_finished=False)
    serializer_class = serializers.ProjectSerializer

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        """Keep only those project that translated to current language."""
        if self.request.query_params.get("category_id"):
            self.queryset = self.queryset.filter(
                category=self.request.query_params.get("category_id"),
            )
        if self.request.language != settings.DEFAULT_LANGUAGE:
            return self.queryset.filter(en_timeline=True)

        return self.queryset.filter(ua_timeline=True)
