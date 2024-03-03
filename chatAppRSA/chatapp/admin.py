from django.contrib import admin

# Register your models here.
from .models import UserProfile, Message

# Admin class for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'public_key', 'profile_image']  # Specify fields to display in the admin interface

# Admin class for Message
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient','content','encrypted_content', 'timestamp']  # Specify fields to display in the admin interface

# Register models with their respective admin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Message, MessageAdmin)