import uuid
from api.models import Cohort, User, MentorProfile, MenteeProfile, MentorMenteePair, MatchingRule,Application, ApplicationFormConfig

import operator
from api.models import Cohort, Application, ScoringRule

class ScoringEngineService:
    def __init__(self, cohort_id):
        self.cohort_id = cohort_id
        # Safe operator mapping for parsing structural string criteria
        self.operators = {
            "==": operator.eq,
            "!=": operator.ne,
            ">": operator.gt,
            ">=": operator.ge,
            "<": operator.lt,
            "<=": operator.le,
            "contains": lambda container, item: item in container if container else False
        }

    def run_scoring(self):
        """
        Evaluates application answers against cohort rules safely and updates database scores.
        """
        # Fetch the active scoring criteria guidelines for this cohort
        rules = ScoringRule.objects.filter(cohort_id=self.cohort_id)
        # Gather submitted or draft applications bound to this cohort
        applications = Application.objects.filter(cohort_id=self.cohort_id)

        processed_records = []

        for app in applications:
            # Safely unpack the candidate's custom JSON responses
            answers = app.answers if isinstance(app.answers, dict) else {}
            total_calculated_score = 0.0

            for rule in rules:
                # Expect rule configurations to contain operational keys:
                # e.g., rule.criteria = {"field": "years_experience", "operator": ">=", "value": 2}
                criteria = rule.criteria if isinstance(rule.criteria, dict) else {}
                target_field = criteria.get("field")
                op_string = criteria.get("operator")
                threshold_value = criteria.get("value")

                if target_field in answers:
                    user_value = answers[target_field]
                    op_func = self.operators.get(op_string)

                    # Execute clean safe criteria matching calculation
                    if op_func:
                        try:
                            if op_func(user_value, threshold_value):
                                total_calculated_score += float(rule.weight)
                        except (TypeError, ValueError):
                            # Protect system loops if types mismatch during matrix execution
                            continue

            # Update the database values for the application object instance
            app.auto_score = total_calculated_score
            app.final_score = total_calculated_score
            app.save(update_fields=['auto_score', 'final_score'])

            processed_records.append({
                "application_id": str(app.id),
                "score": total_calculated_score
            })

        return len(processed_records), processed_records

class MatchingEngineService:
    def __init__(self, cohort_id):
        self.cohort = Cohort.objects.get(id=cohort_id)
        self.rules = MatchingRule.objects.filter(cohort=self.cohort)

    def calculate_match_score(self, mentor_profile, mentee_profile):
        """
        Calculates a match score from 0.0 to 100.0 based on weighted cohort logic rules.
        """
        if not self.rules.exists():
            # Fallback baseline score if no specialized rules are configured
            return 50.0

        total_weight = 0.0
        earned_score = 0.0

        for rule in self.rules:
            weight = rule.weight
            total_weight += weight
            logic = rule.match_logic  # Expects JSON: {"type": "array_intersection", "mentor_field": "expertise", "mentee_field": "course"}

            rule_type = logic.get("type")

            if rule_type == "array_intersection":
                m_field = logic.get("mentor_field")
                # Handle nested user properties or json profile data safely
                mentor_vals = getattr(mentor_profile, m_field, []) if hasattr(mentor_profile, m_field) else []
                mentee_val = getattr(mentee_profile, logic.get("mentee_field", ""), None)

                if isinstance(mentor_vals, list) and mentee_val in mentor_vals:
                    earned_score += weight

            elif rule_type == "exact_match":
                m_val = getattr(mentor_profile, logic.get("mentor_field", ""), None)
                e_val = getattr(mentee_profile, logic.get("mentee_field", ""), None)
                if m_val and e_val and m_val == e_val:
                    earned_score += weight

        if total_weight == 0:
            return 50.0

        return round((earned_score / total_weight) * 100, 2)

    def generate_pairings(self):
        """
        Scans all cohort profiles, scores them against rules, and populates recommended pairings.
        """
        # Find mentees linked to this specific cohort structure
        mentees = MenteeProfile.objects.filter(cohort=self.cohort)
        # Find all active mentors available globally or inside this program pool
        mentors = MentorProfile.objects.filter(user__is_active=True)

        created_pairs_count = 0

        for mentee_prof in mentees:
            for mentor_prof in mentors:
                # Check if a recommendation profile or link already exists to prevent duplicate rows
                exists = MentorMenteePair.objects.filter(
                    cohort=self.cohort,
                    mentor=mentor_prof.user,
                    mentee=mentee_prof.user
                ).exists()

                if not exists:
                    score = self.calculate_match_score(mentor_prof, mentee_prof)

                    # Create the algorithmic recommendation link
                    MentorMenteePair.objects.create(
                        id=uuid.uuid4(),
                        mentor=mentor_prof.user,
                        mentee=mentee_prof.user,
                        cohort=self.cohort,
                        status="recommended",
                        match_score=score
                    )
                    created_pairs_count += 1

        return created_pairs_count



class ApplicationWorkflowService:
    @staticmethod
    def validate_and_submit(application_id):
        """
        Validates a draft application's answers against the cohort's
        JSON form configuration and promotes it to 'submitted'.
        """
        try:
            app = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            raise ValueError("Application record not found.")

        if app.status != "draft":
            raise ValueError(f"Cannot submit application. Current status is '{app.status}', expected 'draft'.")

        # 1. Fetch the validation template configuration
        try:
            config = ApplicationFormConfig.objects.get(cohort=app.cohort, role=app.user.role)
            form_schema = config.schema_fields  # Expects JSON list of dicts: [{"field_name": "years_experience", "required": true}]
        except ApplicationFormConfig.DoesNotExist:
            # Fallback: If no config template is specified, allow submission bypass
            form_schema = []

        user_answers = app.answers or {}  # Expects JSON dict: {"years_experience": "3"}

        # 2. Validate user answers against schema fields
        if isinstance(form_schema, list):
            for field in form_schema:
                field_name = field.get("field_name")
                is_required = field.get("required", False)

                if is_required and field_name not in user_answers:
                    raise ValueError(f"Validation Error: Missing required form response field: '{field_name}'")

        # 3. Transition state
        app.status = "submitted"
        app.save()
        return app

    @staticmethod
    def review_application(application_id, approve=True):
        """
        Transitions application lifecycle status based on a manager's review decision.
        """
        app = Application.objects.get(id=application_id)
        if app.status != "submitted" and app.status != "under_review":
            raise ValueError("Application must be in 'submitted' or 'under_review' status to process a decision.")

        app.status = "approved" if approve else "rejected"
        app.save()
        return app