"""Export portfolio content to a static JSON file used by the frontend.

The live site is a static build: React reads this file at build time instead of
calling the Django API on every page load. Django is then only needed for the
admin (editing) and the contact form.

Usage:
    python manage.py export_portfolio
    python manage.py export_portfolio --output /path/to/portfolio.json
"""

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from portfolio.models import (
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)

# Cloudinary delivery transformations inserted into the URL. These keep the
# original upload untouched and let Cloudinary generate an optimized copy on
# the fly (WebP/AVIF, compressed, limited width).
# Profile: the hero image is shown up to 440 CSS px wide, cropped to 4:5.
# - c_fill,g_auto:face,ar_4:5 => Cloudinary crops around the face at the exact
#   aspect ratio the layout uses, instead of upscaling a small browser crop.
# - q_auto:good => visibly cleaner than the default q_auto for portraits.
# The 1x URL is generated here; the Hero component adds a 2x srcSet variant.
PROFILE_TRANSFORM = "f_auto,q_auto:good,w_440,c_fill,g_auto:face,ar_4:5"
PROJECT_TRANSFORM = "f_auto,q_auto:good,w_900,c_limit"
DEFAULT_OUTPUT = settings.BASE_DIR.parent / "frontend" / "src" / "data" / "portfolio.json"


def optimize_image_url(url, transform):
    """Insert a Cloudinary transformation into an existing delivery URL."""
    if not url:
        return None
    if "res.cloudinary.com" not in url or "/upload/" not in url:
        return url

    base, rest = url.split("/upload/", 1)
    first_segment = rest.split("/", 1)[0]

    # Already transformed (e.g. "f_auto,q_auto/..."). Leave it alone.
    if "_" in first_segment and not first_segment.startswith("v"):
        return url

    return f"{base}/upload/{transform}/{rest}"


def skill_dict(skill):
    return {"id": skill.id, "name": skill.name, "category": skill.category}


class Command(BaseCommand):
    help = "Export portfolio content to JSON for the static frontend build."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default=str(DEFAULT_OUTPUT),
            help=f"Output path (default: {DEFAULT_OUTPUT})",
        )

    def handle(self, *args, **options):
        profile = Profile.objects.first()
        projects = Project.objects.prefetch_related("technologies").all()
        skills = Skill.objects.all()

        data = {
            "generated_at": None,  # filled below after imports are available
            "profile": self._profile(profile),
            "projects": [self._project(project) for project in projects],
            "skills": [skill_dict(skill) for skill in skills],
            "education": list(Education.objects.values()),
            "experience": list(Experience.objects.values()),
        }

        from django.utils import timezone

        data["generated_at"] = timezone.now().isoformat()

        output = Path(options["output"])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(data, indent=2, ensure_ascii=False, default=str) + "\n",
            encoding="utf-8",
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Exported {len(data['projects'])} projects, "
                f"{len(data['skills'])} skills to {output}"
            )
        )

    def _profile(self, profile):
        if not profile:
            return None

        return {
            "id": profile.id,
            "name": profile.name,
            "title": profile.title,
            "bio": profile.bio,
            "email": profile.email,
            "location": profile.location,
            "profile_image": optimize_image_url(
                profile.profile_image.url if profile.profile_image else None,
                PROFILE_TRANSFORM,
            ),
            "github_url": profile.github_url,
            "linkedin_url": profile.linkedin_url,
        }

    def _project(self, project):
        return {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "github_url": project.github_url,
            "live_url": project.live_url,
            "image": optimize_image_url(
                project.image.url if project.image else None,
                PROJECT_TRANSFORM,
            ),
            "featured": project.featured,
            "created_at": project.created_at,
            "technologies": [
                skill_dict(skill) for skill in project.technologies.all()
            ],
        }
