from django.contrib import admin
from .models import Profile, Skill, SkillExchange, Contact

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(SkillExchange)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("subject", "email", "created_at", "is_resolved")
    list_filter = ("is_resolved",)
    search_fields = ("subject", "email", "message")