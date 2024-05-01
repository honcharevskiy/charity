from django.contrib import admin
from main_app import models


class AccountsAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class ProjectsAdmin(admin.ModelAdmin):

    exclude = ['ua_timeline', 'en_timeline']
    pass


class ProjectImagesAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Account, AccountsAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Project, ProjectsAdmin)
admin.site.register(models.ProjectImage, ProjectImagesAdmin)
