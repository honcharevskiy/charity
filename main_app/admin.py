from django.contrib import admin
from main_app import models
from django.contrib.auth.models import User, Group


class AccountsAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('en_name',)}
    pass


class AccountInline(admin.TabularInline):
    model = models.Project.accounts.through
    extra = 1
    min_num = 3


class ProjectsAdmin(admin.ModelAdmin):
    exclude = ['ua_timeline', 'en_timeline', 'accounts']
    inlines = [AccountInline]
    prepopulated_fields = {'slug': ('en_name',)}


class ProjectImagesAdmin(admin.ModelAdmin):
    pass


class FoundersAdmin(admin.ModelAdmin):
    pass


class NewsAdmin(admin.ModelAdmin):
    exclude = ['ua_timeline', 'en_timeline', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('en_title',)}


admin.site.register(models.Account, AccountsAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Project, ProjectsAdmin)
admin.site.register(models.Image, ProjectImagesAdmin)
admin.site.register(models.Founder, FoundersAdmin)
admin.site.register(models.News, NewsAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
