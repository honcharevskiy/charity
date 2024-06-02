from rest_framework import serializers

from charity import settings
from main_app import models


class AccountSerializer(serializers.ModelSerializer):
    """Serialize account."""

    class Meta:
        model = models.Account
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    """Serialize image fields."""

    class Meta:
        model = models.Image
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Serialize category."""

    name = serializers.SerializerMethodField(source='get_name', read_only=True)
    description = serializers.SerializerMethodField(
        source='get_description', read_only=True
    )
    statistic_info = serializers.SerializerMethodField(
        source='get_statistic_info', read_only=True
    )
    statistic_additional_info = serializers.SerializerMethodField(
        source='get_statistic_additional_info', read_only=True
    )

    def get_name(self, category: models.Category) -> str:
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return category.name

        return category.en_name

    def get_description(self, category: models.Category) -> str:
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return category.description

        return category.en_description

    def get_statistic_info(self, category: models.Category) -> str:
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return category.statistic_info

        return category.en_statistic_info

    def get_statistic_additional_info(self, category: models.Category) -> str:
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return category.statistic_additional_info

        return category.en_statistic_additional_info

    class Meta:
        model = models.Category
        fields = [
            'id',
            'name',
            'statistic_additional_info',
            'statistic_info',
            'description',
            'statistic_counter',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """Serialize project."""

    title = serializers.SerializerMethodField(source='get_title', read_only=True)
    description = serializers.SerializerMethodField(
        source='get_description', read_only=True
    )
    category = CategorySerializer()
    accounts = AccountSerializer(many=True)

    def get_title(self, project: models.Project) -> str:
        """Chose default or en title based on language."""
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return project.title

        return project.en_title

    def get_description(self, project: models.Project) -> str:
        """Chose default or en description based on language."""
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return project.description

        return project.en_description

    class Meta:
        model = models.Project
        fields = [
            'id',
            'title',
            'description',
            'goal',
            'accumulated_current',
            'accounts',
            'category',
        ]


class FounderSerializer(serializers.ModelSerializer):
    """Serialize founder info to json format."""

    name = serializers.SerializerMethodField(source='get_name', read_only=True)
    description = serializers.SerializerMethodField(
        source='get_description', read_only=True
    )
    picture = ImageSerializer()

    def get_name(self, founder: models.Founder) -> str:
        """Chose default or en title based on language."""
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return founder.name

        return founder.en_name

    def get_description(self, founder: models.Project) -> str:
        """Chose default or en description based on language."""
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return founder.description

        return founder.en_description

    class Meta:
        model = models.Founder
        fields = [
            'id',
            'name',
            'description',
            'picture',
        ]


class NewsSerializer(serializers.ModelSerializer):
    """Serialize project."""

    title = serializers.SerializerMethodField(source='get_title', read_only=True)
    description = serializers.SerializerMethodField(
        source='get_description', read_only=True
    )
    created_at = serializers.DateTimeField(format='%d/%m/%y')

    def get_title(self, news: models.Project) -> str:
        """Chose default or en title based on language."""
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return news.title

        return news.en_title

    def get_description(self, news: models.Project) -> str:
        """Chose default or en description based on language."""
        if self.context['request'].language == settings.DEFAULT_LANGUAGE:
            return news.description

        return news.en_description

    class Meta:
        model = models.News
        fields = [
            'id',
            'title',
            'description',
            'created_at',
        ]
