from django.contrib import admin
from apps.core.models import Account, Operation, Budget, Category, Recurring, Tag

admin.site.register(Account)
admin.site.register(Operation)
admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(Recurring)
admin.site.register(Tag)
