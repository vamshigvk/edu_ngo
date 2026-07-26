from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    CohortViewSet, UserViewSet, MentorProfileViewSet, MenteeProfileViewSet,
    ApplicationFormConfigViewSet, ApplicationViewSet, ScoringRuleViewSet,
    MatchingRuleViewSet, MentorMenteePairViewSet, CheckInViewSet,
    ResourceViewSet, RolePermissionViewSet
)

router = DefaultRouter()
router.register(r'cohorts', CohortViewSet, basename='cohort')
router.register(r'users', UserViewSet, basename='user')
router.register(r'mentor-profiles', MentorProfileViewSet, basename='mentorprofile')
router.register(r'mentee-profiles', MenteeProfileViewSet, basename='menteeprofile')
router.register(r'form-configs', ApplicationFormConfigViewSet, basename='formconfig')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'scoring-rules', ScoringRuleViewSet, basename='scoringrule')
router.register(r'matching-rules', MatchingRuleViewSet, basename='matchingrule')
router.register(r'pairs', MentorMenteePairViewSet, basename='pair')
router.register(r'checkins', CheckInViewSet, basename='checkin')
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'permissions', RolePermissionViewSet, basename='permission')

urlpatterns = [
    # Explicit Overrides for matching API validation rules exactly
    path('cohorts/<uuid:cohort_id>/scoring/run/', CohortViewSet.as_view({'post': 'run_scoring_engine'}), name='cohort-scoring-run'),
    path('cohorts/<uuid:cohort_id>/matching/run/', CohortViewSet.as_view({'post': 'run_matching_engine'}), name='cohort-matching-run'),

    path('', include(router.urls)),
]