import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class Cohort(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    max_mentees = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.program})"


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('mentee', 'Mentee'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    phone = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class MentorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    expertise = models.JSONField(default=list)
    max_mentees = models.PositiveIntegerField(default=1)
    availability = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    languages = models.JSONField(default=list)

    def __str__(self):
        return f"Mentor: {self.user.full_name}"


class MenteeProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentee_profile')
    university = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)
    cohort = models.ForeignKey(Cohort, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentees')

    def __str__(self):
        return f"Mentee: {self.user.full_name}"


class ApplicationFormConfig(models.Model):
    FIELD_TYPE_CHOICES = [
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('number', 'Number'),
        ('dropdown', 'Dropdown'),
        ('multi_select', 'Multi Select'),
        ('date', 'Date'),
        ('file_upload', 'File Upload'),
        ('boolean', 'Boolean'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='form_configs')
    field_name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=30, choices=FIELD_TYPE_CHOICES)
    is_required = models.BooleanField(default=False)
    field_order = models.PositiveIntegerField(default=0)
    options = models.JSONField(default=list, blank=True)
    validation_rules = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['field_order']

    def __str__(self):
        return f"{self.cohort.name} - {self.field_name} ({self.field_type})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('scored', 'Scored'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
    ]

    PURPOSE_CHOICES = [
        ('scholarship', 'Scholarship'),
        ('admission', 'Admission'),
        ('career_switch', 'Career Switch'),
        ('skill_building', 'Skill Building'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    answers = models.JSONField(default=dict)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES, default='other')
    auto_score = models.FloatField(default=0.0)
    final_score = models.FloatField(default=0.0)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"App by {self.user.full_name} for {self.cohort.name} (Status: {self.status})"


class ScoringRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='scoring_rules')
    field_name = models.CharField(max_length=255)
    weight = models.FloatField(default=1.0)
    scoring_logic = models.JSONField(default=dict)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_scoring_rules')

    def __str__(self):
        return f"Scoring Rule: {self.field_name} (Weight: {self.weight}) for {self.cohort.name}"


class MatchingRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='matching_rules')
    criteria_name = models.CharField(max_length=255)
    weight = models.FloatField(default=1.0)
    match_logic = models.JSONField(default=dict)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_matching_rules')

    def __str__(self):
        return f"Matching Rule: {self.criteria_name} for {self.cohort.name}"


class MentorMenteePair(models.Model):
    STATUS_CHOICES = [
        ('recommended', 'Recommended'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('terminated', 'Terminated'),
    ]

    OUTCOME_CHOICES = [
        ('achieved', 'Achieved'),
        ('partial', 'Partial'),
        ('not_achieved', 'Not Achieved'),
        ('pending', 'Pending'),
        ('unknown', 'Unknown'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_pairs')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_pairs')
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='pairs')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='recommended')
    match_score = models.FloatField(default=0.0)
    recommended_at = models.DateTimeField(auto_now_add=True)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_pairs')
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    outcome = models.CharField(max_length=30, choices=OUTCOME_CHOICES, default='pending')
    outcome_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pair: Mentor {self.mentor.full_name} x Mentee {self.mentee.full_name} ({self.status})"


class CheckIn(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pair = models.ForeignKey(MentorMenteePair, on_delete=models.CASCADE, related_name='checkins')
    sequence_number = models.PositiveIntegerField()
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    action_items = models.JSONField(default=list, blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='logged_checkins')
    next_checkin_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pair', 'sequence_number']

    def __str__(self):
        return f"CheckIn #{self.sequence_number} for Pair {self.pair.id} ({self.status})"


class Resource(models.Model):
    TYPE_CHOICES = [
        ('scholarship', 'Scholarship'),
        ('course', 'Course'),
        ('university_info', 'University Info'),
        ('guide', 'Guide'),
        ('video', 'Video'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    continent = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=500)
    description = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_resources')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resource: {self.title} ({self.type})"


class RolePermission(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    is_allowed = models.BooleanField(default=False)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_permissions')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['role', 'resource', 'action'], name='unique_role_resource_action')
        ]

    def __str__(self):
        status = "Allowed" if self.is_allowed else "Denied"
        return f"{self.role} -> {self.action} on {self.resource}: {status}"