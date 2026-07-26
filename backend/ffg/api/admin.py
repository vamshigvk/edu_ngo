from django.contrib import admin
from api.models import (
    Cohort, User, MentorProfile, MenteeProfile,
    MentorMenteePair, CheckIn, Resource
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('full_name', 'email')

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'program')
    search_fields = ('name', 'program')

@admin.register(MentorMenteePair)
class MentorMenteePairAdmin(admin.ModelAdmin):
    list_display = ('id', 'mentor', 'mentee', 'cohort', 'status', 'match_score')
    list_filter = ('status', 'cohort')
    search_fields = ('mentor__full_name', 'mentee__full_name')

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('pair', 'sequence_number', 'date', 'status')
    list_filter = ('status', 'date')
    ordering = ('pair', 'sequence_number')

# Register remaining core profile structures dynamically
admin.site.register(MentorProfile)
admin.site.register(MenteeProfile)
admin.site.register(Resource)