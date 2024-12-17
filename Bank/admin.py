from django.contrib import admin
from django.contrib import admin
from .models import accounts

# Define the admin class for User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('Name','userid', 'Email', 'phone_no', 'passwords', 'moneybox','depost','withdrawls','historys','timestraps')  # Fields to display in admin list view
    search_fields = ('Name','userid', 'email', 'phone_no', 'passwords', 'moneybox','depost','withdrawls','historys','timestraps')  # Fields to search by in admin list view

# Register the models with their corresponding admin classes
admin.site.register(accounts, UserAdmin)
