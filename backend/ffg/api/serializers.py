from rest_framework import serializers
from api.models import (
    Cohort, User, MentorProfile, MenteeProfile, ApplicationFormConfig,
    Application, ScoringRule, MatchingRule, MentorMenteePair, CheckIn,
    Resource, RolePermission
)

class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MentorProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = MentorProfile
        fields = '__all__'


class MenteeProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = MenteeProfile
        fields = '__all__'


class ApplicationFormConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFormConfig
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Application
        fields = '__all__'


class ScoringRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoringRule
        fields = '__all__'


class MatchingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingRule
        fields = '__all__'


class MentorMenteePairSerializer(serializers.ModelSerializer):
    mentor_name = serializers.CharField(source='mentor.full_name', read_only=True)
    mentee_name = serializers.CharField(source='mentee.full_name', read_only=True)

    class Meta:
        model = MentorMenteePair
        fields = '__all__'


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'