from django.contrib import admin
from main_app import models


class AccountsAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class AccountInline(admin.TabularInline):
    model = models.Project.accounts.through
    extra = 1
    min_num = 3


class ProjectsAdmin(admin.ModelAdmin):
    exclude = ['ua_timeline', 'en_timeline', 'accounts']
    inlines = [AccountInline]
    pass


class ProjectImagesAdmin(admin.ModelAdmin):
    pass


class FoundersAdmin(admin.ModelAdmin):
    pass


class NewsAdmin(admin.ModelAdmin):
    exclude = ['ua_timeline', 'en_timeline', 'created_at', 'updated_at']


admin.site.register(models.Account, AccountsAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Project, ProjectsAdmin)
admin.site.register(models.ProjectImage, ProjectImagesAdmin)
admin.site.register(models.Founder, FoundersAdmin)
admin.site.register(models.News, NewsAdmin)
