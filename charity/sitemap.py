from django.contrib.sitemaps import Sitemap


from main_app import models


class NewsSitemap(Sitemap):
    """Represent News in sitemap."""

    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        """Return news that will be displayed in sitemap."""
        return models.News.objects.all()

    def lastmod(self, obj: models.News):
        """Return last-modified date for every news."""
        return obj.updated_at


class ProjectsSitemap(Sitemap):
    """Represent model Projects in sitemap."""

    changefreq = 'weekly'
    priority = 1

    def items(self):
        """Return projects that will be displayed in sitemap."""
        return models.Project.objects.filter(is_finished=False)

    def lastmod(self, obj: models.Project):
        """Return last-modified date for every project."""
        return obj.updated_at


class CategoriesSitemap(Sitemap):
    """Represent model Category in sitemap."""

    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        """Return categories that will be displayed in sitemap."""
        return models.Category.objects.all()

    def lastmod(self, obj: models.Project):
        """Return last-modified date for every category."""
        return obj.updated_at


sitemaps = {
    'sitemaps': {
        'news': NewsSitemap,
        'projects': ProjectsSitemap,
        'categories': CategoriesSitemap,
    }
}
