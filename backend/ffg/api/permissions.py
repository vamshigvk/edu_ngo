from rest_framework import permissions

class IsCohortManagerOrOwner(permissions.BasePermission):
    """
    Granular permission framework:
    - Cohort Managers have unrestricted access to manage structures.
    - Mentors and Mentees can only read or update records they own.
    """
    def has_permission(self, request, view):
        # Allow authenticated users to browse baseline route indexes
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 1. Cohort Managers have full master administrative clearance
        if getattr(request.user, 'role', None) == 'cohort_manager':
            return True

        # 2. Safely resolve resource mapping based on the structural object type
        # Check User Profile ownership
        if hasattr(obj, 'email'):
            return obj == request.user

        # Check Profile links (MentorProfile / MenteeProfile)
        if hasattr(obj, 'user'):
            return obj.user == request.user

        # Check Application forms submitted by the user
        if hasattr(obj, 'user'):
            return obj.user == request.user

        # Check Check-Ins tracking sequences
        if hasattr(obj, 'pair'):
            return obj.pair.mentor == request.user or obj.pair.mentee == request.user

        # Check MentorMenteePairs matching pools
        if hasattr(obj, 'mentor') and hasattr(obj, 'mentee'):
            return obj.mentor == request.user or obj.mentee == request.user

        # Default fallback: deny access if no clear structural ownership matches
        return False