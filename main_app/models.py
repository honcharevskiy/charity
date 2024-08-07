from django.db import models
from django_resized import ResizedImageField
from mdeditor.fields import MDTextField
from django.urls import reverse


class Image(models.Model):
    """Image with alternative text."""

    image = ResizedImageField(size=[1000, 800], force_format='JPEG')
    alternative_text = models.CharField(max_length=255)

    def __str__(self):
        return self.alternative_text

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Account(models.Model):
    """Accounts information."""

    title = models.CharField(max_length=255)
    iban = models.CharField(max_length=255, null=True, blank=True)
    description = MDTextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Category(models.Model):
    """Project categories."""

    name = models.CharField(max_length=255)
    en_name = models.CharField(max_length=255, blank=True, null=True)

    description = MDTextField(null=True, blank=True)
    en_description = MDTextField(null=True, blank=True)

    statistic_counter = models.BigIntegerField(null=True, blank=True)

    statistic_info = models.CharField(max_length=255, null=True, blank=True)
    statistic_additional_info = models.CharField(max_length=255, null=True, blank=True)

    en_statistic_info = models.CharField(max_length=255, null=True, blank=True)
    en_statistic_additional_info = models.CharField(max_length=255, null=True, blank=True)

    picture = models.ForeignKey(Image, on_delete=models.DO_NOTHING, blank=True, null=True)

    slug = models.SlugField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Return url to the specific category."""
        return reverse('categories-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Project(models.Model):
    """Information about project."""

    title = models.CharField(max_length=370, null=True, blank=True)
    description = MDTextField(null=True, blank=True)

    en_title = models.CharField(max_length=370, null=True, blank=True)
    en_description = MDTextField(null=True, blank=True)

    goal = models.BigIntegerField(verbose_name='Accumulation goal.')
    accumulated_current = models.BigIntegerField(
        verbose_name='How much money already accumulated.'
    )

    ua_timeline = models.BooleanField(default=True, blank=True)
    en_timeline = models.BooleanField(default=False, blank=True)

    accounts = models.ManyToManyField(Account)
    images = models.ManyToManyField(Image, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    slug = models.SlugField(unique=True)

    is_finished = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title or self.en_title}'

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """Set fields on save."""
        self.en_timeline = all([self.en_title, self.en_description])
        self.ua_timeline = all([self.title, self.description])
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )

    def get_absolute_url(self):
        """Generate url to the specific Project."""
        return reverse('projects-detail', kwargs={'slug': self.slug})
        pass


class Founder(models.Model):
    """Information about founders."""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    picture = models.ForeignKey(Image, blank=True, null=True, on_delete=models.DO_NOTHING)

    en_name = models.CharField(max_length=255)
    en_description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name or self.en_name}'

    class Meta:
        verbose_name = 'Founder'
        verbose_name_plural = 'Founders'


class News(models.Model):
    """Information about news."""

    title = models.CharField(max_length=255)
    description = MDTextField()
    picture = models.ForeignKey(Image, on_delete=models.DO_NOTHING, blank=True, null=True)

    en_title = models.CharField(max_length=255, blank=True, null=True)
    en_description = MDTextField(blank=True, null=True)

    slug = models.SlugField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ua_timeline = models.BooleanField(default=True, blank=True)
    en_timeline = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.title or self.en_title}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """Set fields on save."""
        self.en_timeline = all([self.en_title, self.en_description])
        self.ua_timeline = all([self.title, self.description])
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )

    def get_absolute_url(self):
        """Generate url to the specific News."""
        return reverse('news-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Media(models.Model):
    """Separate media not related to other entities."""

    image = ResizedImageField(size=[1000, 800], force_format='JPEG')
    alternative_text = models.CharField(max_length=255)

    description = models.CharField(max_length=400, blank=True, null=True)
    en_description = models.CharField(max_length=400, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.alternative_text