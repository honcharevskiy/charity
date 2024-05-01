from rest_framework import serializers

from charity import settings
from main_app import models


class AccountSerializer(serializers.ModelSerializer):
    """Serialize account."""

    class Meta:
        model = models.Account
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """Serialize category."""

    name = serializers.SerializerMethodField(source="get_name", read_only=True)

    def get_name(self, category: models.Category) -> str:
        if self.context["request"].language == settings.DEFAULT_LANGUAGE:
            return category.name

        return category.en_name

    class Meta:
        model = models.Category
        fields = ["id", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    """Serialize project."""

    title = serializers.SerializerMethodField(source="get_title", read_only=True)
    description = serializers.SerializerMethodField(
        source="get_description", read_only=True
    )
    category = CategorySerializer()
    accounts = AccountSerializer(many=True)

    def get_title(self, project: models.Project) -> str:
        """Chose default of en title based on language."""
        if self.context["request"].language == settings.DEFAULT_LANGUAGE:
            return project.title

        return project.en_title

    def get_description(self, project: models.Project) -> str:
        """Chose default of en description based on language."""
        if self.context["request"].language == settings.DEFAULT_LANGUAGE:
            return project.description

        return project.en_description

    class Meta:
        model = models.Project
        fields = [
            "id",
            "title",
            "description",
            "goal",
            "accumulated_current",
            "accounts",
            "category",
        ]
