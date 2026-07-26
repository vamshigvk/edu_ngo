"""Helpers that attach derived (non-mapped) display attributes to ORM objects.

The related ``user``/``mentor``/``mentee`` relationships are eager-loaded
(``lazy="selectin"``), so these run without triggering async lazy-load errors.
"""


def enrich_user_name(obj) -> None:
    obj.user_name = obj.user.full_name if getattr(obj, "user", None) else None


def enrich_pair_names(obj) -> None:
    obj.mentor_name = obj.mentor.full_name if getattr(obj, "mentor", None) else None
    obj.mentee_name = obj.mentee.full_name if getattr(obj, "mentee", None) else None
