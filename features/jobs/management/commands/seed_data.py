import random
import textwrap

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from features.applications.models import Application
from features.jobs.models import JobDescription
from features.resumes.models import Resume

User = get_user_model()

JOBS = [
    {
        "title": "Senior Backend Engineer",
        "skills": ["Python", "Django", "PostgreSQL", "REST APIs", "Docker"],
    },
    {
        "title": "Frontend Developer",
        "skills": ["JavaScript", "React", "TypeScript", "CSS", "HTML"],
    },
    {
        "title": "DevOps Engineer",
        "skills": ["AWS", "Kubernetes", "Terraform", "CI/CD", "Linux"],
    },
    {
        "title": "Data Scientist",
        "skills": ["Python", "Pandas", "scikit-learn", "SQL", "Statistics"],
    },
    {
        "title": "Machine Learning Engineer",
        "skills": ["PyTorch", "TensorFlow", "MLOps", "Python", "NLP"],
    },
    {
        "title": "Full Stack Developer",
        "skills": ["Node.js", "React", "MongoDB", "Express", "GraphQL"],
    },
    {
        "title": "Product Designer",
        "skills": ["Figma", "UX Research", "Prototyping", "Design Systems", "UI"],
    },
    {
        "title": "QA Automation Engineer",
        "skills": ["Selenium", "Pytest", "Cypress", "CI/CD", "Python"],
    },
    {
        "title": "Mobile Engineer (iOS)",
        "skills": ["Swift", "SwiftUI", "Xcode", "REST APIs", "Core Data"],
    },
    {
        "title": "Cloud Solutions Architect",
        "skills": ["AWS", "Azure", "Microservices", "Networking", "Security"],
    },
]

FIRST_NAMES = [
    "Alice", "Brian", "Carla", "David", "Elena", "Frank", "Grace", "Henry",
    "Isabel", "Jamal", "Kira", "Liam", "Maria", "Noah", "Olivia", "Pedro",
    "Quinn", "Rosa", "Samuel", "Tina", "Umar", "Vera", "Wesley", "Xenia",
]

LAST_NAMES = [
    "Anderson", "Brooks", "Chen", "Diaz", "Evans", "Ferraro", "Gupta",
    "Hughes", "Ibrahim", "Johnson", "Khan", "Lopez", "Mensah", "Novak",
    "Owusu", "Park", "Rossi", "Silva", "Tanaka", "Volkov",
]


_DESCRIPTION_TEMPLATE = textwrap.dedent(
    """\
    # {title}

    We are looking for a talented **{title}** to join our growing team.
    You will work closely with product, design, and engineering to ship
    high-quality software that delights our customers.

    ## About the Role

    As a {title}, you will own features end-to-end, collaborate across
    teams, and help shape our technical direction. This is a high-impact
    position with plenty of room for growth.

    ## Responsibilities

    - Design, build, and maintain reliable, scalable systems
    - Collaborate with cross-functional teams on new initiatives
    - Write clean, well-tested, and well-documented code
    - Participate in code reviews and mentor junior engineers
    - Continuously improve performance, quality, and developer experience

    ## Required Skills

    {skills_md}

    ## Nice to Have

    - Experience working in an agile, fast-paced environment
    - Strong communication and problem-solving skills
    - A passion for building great products

    ## What We Offer

    - Competitive salary and equity
    - Flexible, remote-friendly working hours
    - Generous learning and development budget
    - A supportive and inclusive team culture

    > _We are an equal opportunity employer and value diversity._
    """
)


def markdown_description(title: str, skills: list[str]) -> str:
    skills_md = "\n".join(f"- {skill}" for skill in skills)
    return _DESCRIPTION_TEMPLATE.format(title=title, skills_md=skills_md)


RESUME_TEMPLATE = textwrap.dedent(
    """\
    {name}
    {email} | +1 (555) 010-{phone}

    SUMMARY
    Experienced professional with a strong background in {primary} and {secondary}.
    Proven track record of delivering high-quality results in fast-paced teams.

    SKILLS
    {skills}

    EXPERIENCE
    Senior Contributor — Acme Corp (2021 - Present)
    - Led key projects involving {primary} and {secondary}.
    - Collaborated with cross-functional teams to ship features.

    Contributor — Globex Inc (2018 - 2021)
    - Built and maintained production systems.

    EDUCATION
    B.Sc. Computer Science — State University
    """
)


class Command(BaseCommand):
    help = "Seed the database with sample jobs and applications."

    def add_arguments(self, parser):
        parser.add_argument("--jobs", type=int, default=10)
        parser.add_argument("--applications", type=int, default=20)

    @transaction.atomic
    def handle(self, *args, **options):
        num_jobs = options["jobs"]
        num_applications = options["applications"]

        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if user is None:
            self.stderr.write(
                self.style.ERROR("No users found. Create a user first (createsuperuser).")
            )
            return

        random.seed(42)

        # --- Jobs ---
        created_jobs = []
        for i in range(num_jobs):
            spec = JOBS[i % len(JOBS)]
            title = spec["title"]
            if i >= len(JOBS):
                title = f"{title} #{i // len(JOBS) + 1}"
            job = JobDescription.objects.create(
                title=title,
                description=markdown_description(title, spec["skills"]),
                required_skills=spec["skills"],
                is_published=random.random() < 0.7,
                created_by=user,
            )
            created_jobs.append(job)
        self.stdout.write(self.style.SUCCESS(f"Created {len(created_jobs)} jobs."))

        # --- Applications (each gets its own resume) ---
        statuses = [c[0] for c in Application.STATUS_CHOICES]
        created_apps = 0
        for i in range(num_applications):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
            email = f"{first.lower()}.{last.lower()}{i}@example.com"
            phone = f"{random.randint(1000, 9999)}"
            job = random.choice(created_jobs)
            skills = job.required_skills or ["Communication", "Teamwork"]

            resume_text = RESUME_TEMPLATE.format(
                name=name,
                email=email,
                phone=phone,
                primary=skills[0],
                secondary=skills[1] if len(skills) > 1 else skills[0],
                skills=", ".join(skills),
            )
            resume = Resume.objects.create(
                candidate_name=name,
                email=email,
                raw_text=resume_text,
                uploaded_by=user,
            )
            resume.file.save(
                f"seed_resume_{i}.txt",
                ContentFile(resume_text.encode("utf-8")),
                save=True,
            )

            Application.objects.create(
                job=job,
                resume=resume,
                full_name=name,
                email=email,
                phone=f"+1 (555) 010-{phone}",
                cover_letter=(
                    f"Dear Hiring Manager,\n\nI am excited to apply for the "
                    f"{job.title} role. My experience with {skills[0]} makes me "
                    f"a strong fit.\n\nBest regards,\n{name}"
                ),
                status=random.choice(statuses),
            )
            created_apps += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created_apps} applications."))
        self.stdout.write(self.style.SUCCESS("Seeding complete."))
