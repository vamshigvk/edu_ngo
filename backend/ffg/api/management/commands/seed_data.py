import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Cohort, User, MentorMenteePair, CheckIn

class Command(BaseCommand):
    help = "Seeds the database with authentic mentorship pairings and historical session checkpoints."

    def handle(self, *args, **options):
        self.stdout.write("Purging stale engineering data records...")
        CheckIn.objects.all().delete()
        MentorMenteePair.objects.all().delete()
        User.objects.all().delete()
        Cohort.objects.all().delete()

        self.stdout.write("Seeding active structural Cohorts...")
        cohort_active = Cohort.objects.create(
            name="Global Engineering Mentorship 2026",
            program="Software Development Track",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=180),
            status="active",
            max_mentees=50
        )

        self.stdout.write("Populating user accounts (Mentors and Mentees)...")
        # Define users to match the schema field name: 'full_name'
        users_data = [
            {"full_name": "Aarav Mehta", "email": "aarav.mehta@example.com", "role": "mentee"},
            {"full_name": "Ananya Rao", "email": "ananya.rao@example.com", "role": "mentee"},
            {"full_name": "Vikram Singh", "email": "vikram.singh@example.com", "role": "mentor"},
            {"full_name": "Priya Sharma", "email": "priya.sharma@example.com", "role": "mentor"},
        ]

        users = []
        for u in users_data:
            obj = User.objects.create(
                full_name=u["full_name"],
                email=u["email"],
                role=u["role"]
            )
            users.append(obj)

        self.stdout.write("Assembling structural Mentor-Mentee pairings...")
        mentees = [u for u in users if u.role == "mentee"]
        mentors = [u for u in users if u.role == "mentor"]

        pairs = []
        for index, mentee in enumerate(mentees):
            # Form clean pairs mapping back to our active cohort rules
            assigned_mentor = mentors[index % len(mentors)]
            pair = MentorMenteePair.objects.create(
                mentor=assigned_mentor,
                mentee=mentee,
                cohort=cohort_active,
                status="active",
                match_score=94.5
            )
            pairs.append(pair)

        self.stdout.write("Generating historical session Check-In tracking chains...")
        # Populate incremental checkpoint sequences for the pairs
        for pair in pairs:
            for seq in range(1, 4):
                past_date = timezone.now() - timezone.timedelta(days=(4 - seq) * 7)
                CheckIn.objects.create(
                    pair=pair,
                    sequence_number=seq,
                    date=past_date.date(),
                    notes=f"Completed sequence checkpoint #{seq}. Working smoothly against architecture milestones.",
                    status="completed"
                )

        self.stdout.write(self.style.SUCCESS("Database seeding completed smoothly! All records match structural schemas."))