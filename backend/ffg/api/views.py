from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Count
from django.http import HttpResponse # Added for dashboard views
from api.models import (
    Cohort, User, MentorProfile, MenteeProfile, ApplicationFormConfig,
    Application, ScoringRule, MatchingRule, MentorMenteePair, CheckIn,
    Resource, RolePermission
)
from api.serializers import (
    CohortSerializer, UserSerializer, MentorProfileSerializer, MenteeProfileSerializer,
    ApplicationFormConfigSerializer, ApplicationSerializer, ScoringRuleSerializer,
    MatchingRuleSerializer, MentorMenteePairSerializer, CheckInSerializer,
    ResourceSerializer, RolePermissionSerializer
)
from api.services import MatchingEngineService, ApplicationWorkflowService
from api.permissions import IsCohortManagerOrOwner

# Import the newly created service layer at the top of api/views.py
from api.services import MatchingEngineService, ApplicationWorkflowService, ScoringEngineService

# Locate your CohortViewSet inside api/views.py and update the method block:
class CohortViewSet(viewsets.ModelViewSet):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer

    def run_scoring_engine(self, request, cohort_id=None):
        """
        Route: POST /api/cohorts/<uuid:cohort_id>/scoring/run/
        """
        try:
            # Instantiate and run the comprehensive scoring evaluation matrix
            engine = ScoringEngineService(cohort_id=cohort_id)
            count, scores_list = engine.run_scoring()

            return Response({
                "cohort_id": str(cohort_id),
                "applications_processed": count,
                "scores": scores_list
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CohortViewSet(viewsets.ModelViewSet):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer

    def run_scoring_engine(self, request, cohort_id=None):
        """
        Route: POST /api/cohorts/<uuid:cohort_id>/scoring/run/
        """
        try:
            # Add or separate your exact analytical scoring logic metrics execution here
            return Response({
                "status": "success",
                "message": f"Successfully calculated compatibility scores for cohort {cohort_id}."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def run_matching_engine(self, request, cohort_id=None):
        """
        Route: POST /api/cohorts/<uuid:cohort_id>/matching/run/
        """
        try:
            engine = MatchingEngineService(cohort_id=cohort_id)
            pairs_generated = engine.generate_pairings()
            return Response({
                "status": "success",
                "message": f"Successfully evaluated profiles. Generated {pairs_generated} candidate recommendations."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCohortManagerOrOwner]

class MentorProfileViewSet(viewsets.ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsCohortManagerOrOwner]

class MenteeProfileViewSet(viewsets.ModelViewSet):
    queryset = MenteeProfile.objects.all()
    serializer_class = MenteeProfileSerializer
    permission_classes = [IsCohortManagerOrOwner]

class ApplicationFormConfigViewSet(viewsets.ModelViewSet):
    queryset = ApplicationFormConfig.objects.all()
    serializer_class = ApplicationFormConfigSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsCohortManagerOrOwner]

    @action(detail=True, methods=['post'], url_path='submit')
    def submit_application(self, request, pk=None):
        try:
            service = ApplicationWorkflowService()
            updated_app = service.validate_and_submit(application_id=pk)
            return Response({
                "status": "success",
                "message": "Application validated and submitted successfully.",
                "current_status": updated_app.status
            }, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='review')
    def review_application(self, request, pk=None):
        approve_decision = request.data.get("approve", True)
        try:
            service = ApplicationWorkflowService()
            updated_app = service.review_application(application_id=pk, approve=approve_decision)
            return Response({
                "status": "success",
                "message": f"Application has been processed cleanly to state: {updated_app.status}.",
                "current_status": updated_app.status
            }, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

class ScoringRuleViewSet(viewsets.ModelViewSet):
    queryset = ScoringRule.objects.all()
    serializer_class = ScoringRuleSerializer

class MatchingRuleViewSet(viewsets.ModelViewSet):
    queryset = MatchingRule.objects.all()
    serializer_class = MatchingRuleSerializer

class MentorMenteePairViewSet(viewsets.ModelViewSet):
    queryset = MentorMenteePair.objects.all()
    serializer_class = MentorMenteePairSerializer
    permission_classes = [IsCohortManagerOrOwner]

class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [IsCohortManagerOrOwner]

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer


# --- STANDALONE NON-API DASHBOARD VIEWS ---

permission_classes = [IsCohortManagerOrOwner]

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer


# --- STANDALONE NON-API DASHBOARD VIEWS ---
def employee_dashboard_view(request):
    """
    Program Manager / Admin Dashboard Engine
    Route: GET /dashboard/emp/
    """
    metrics = {
        "platform_summary": {
            "total_users": User.objects.count(),
            "total_active_cohorts": Cohort.objects.filter(status="active").count(),
            "total_applications_under_review": Application.objects.filter(status="submitted").count(),
        },
        "cohort_breakdown": list(
            Cohort.objects.values("id", "name", "status")
            .annotate(total_pairs=Count("pairs"))  # Fixed keyword mapping here
        ),
        "system_health": {
            "total_pairings_formed": MentorMenteePair.objects.count(),
            "completed_checkins": CheckIn.objects.filter(status="completed").count(),
        }
    }
    return JsonResponse(metrics, safe=False, json_dumps_params={'indent': 2})

def mentor_dashboard_view(request):
    """
    Mentor Portal Metrics Engine
    Route: GET /dashboard/mentor/
    """
    assigned_pairs = MentorMenteePair.objects.all()

    metrics = {
        "role": "Mentor",
        "engagement_metrics": {
            "active_assigned_mentees": assigned_pairs.count(),
            "pending_action_items": CheckIn.objects.filter(status="scheduled").count()
        },
        "assigned_cohorts": list(
            Cohort.objects.filter(pairs__in=assigned_pairs)  # Fixed keyword mapping here
            .values("name", "start_date", "end_date").distinct()
        )
    }
    return JsonResponse(metrics, safe=False, json_dumps_params={'indent': 2})

def mentee_dashboard_view(request):
    """
    Mentee Portal Metrics Engine
    Route: GET /dashboard/mentee/
    """
    # In production, filter using request.user. Here we show global context metrics for testing
    my_pairings = MentorMenteePair.objects.all()

    metrics = {
        "role": "Mentee",
        "my_program_status": {
            "has_active_match": my_pairings.exists(),
            "logged_checkins_count": CheckIn.objects.filter(status="completed").count()
        },
        "available_resources": [
            {"title": "Platform Onboarding Guide", "type": "PDF"},
            {"title": "Setting SMART Goals Document", "type": "Doc"}
        ]
    }
    return JsonResponse(metrics, safe=False, json_dumps_params={'indent': 2})