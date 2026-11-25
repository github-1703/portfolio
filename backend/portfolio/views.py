import logging

import requests
from django.shortcuts import render
from django.conf import settings 
from django.core.mail import EmailMessage

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile,Project,Skill,Education,Experience
from .serializers import ProfileSerializer,ProjectSerializer,SkillSerializer,EducationSerializer,ExperienceSerializer,ContactMessageSerializer

logger = logging.getLogger(__name__)


@api_view(["GET"])
def profile_api(request):
    profile = Profile.objects.first()

    if not profile:
        return Response(
            {"message": "Profile not found"},
            status=404
        )

    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


@api_view(["GET"])
def projects_api(request):
    projects = Project.objects.all()

    serializer = ProjectSerializer(
        projects,
        many=True
    )

    return Response(serializer.data)

@api_view(["GET"])
def skills_api(request):
    skills = Skill.objects.all()

    serializer = SkillSerializer(
        skills,
        many=True
    )

    return Response(serializer.data)


@api_view(["GET"])
def education_api(request):
    education = Education.objects.all()

    serializer = EducationSerializer(
        education,
        many=True
    )

    return Response(serializer.data)

@api_view(["GET"])
def experience_api(request):
    experiences = Experience.objects.all()

    serializer = ExperienceSerializer(
        experiences,
        many=True
    )

    return Response(serializer.data)

def _send_contact_email(contact, subject, body):
    """Send the notification over HTTPS (Brevo) when configured, else SMTP.

    Render's free tier blocks outbound SMTP, so production uses Brevo's HTTPS
    API. Local development keeps using Gmail SMTP.
    """
    recipient = settings.CONTACT_EMAIL
    api_key = getattr(settings, "BREVO_API_KEY", "")

    if api_key:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": api_key,
                "accept": "application/json",
                "content-type": "application/json",
            },
            json={
                "sender": {
                    "email": settings.BREVO_SENDER_EMAIL,
                    "name": settings.BREVO_SENDER_NAME,
                },
                "to": [{"email": recipient}],
                "replyTo": {"email": contact.email, "name": contact.name},
                "subject": subject,
                "textContent": body,
            },
            timeout=15,
        )
        response.raise_for_status()
        return True

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[contact.email],
    )
    return email.send(fail_silently=False) > 0


@api_view(["POST"])
def contact_api(request):
    serializer = ContactMessageSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    contact = serializer.save()
    subject = f"Portfolio Contact from {contact.name}"
    email_body = (
        f"Name: {contact.name}\n"
        f"Email: {contact.email}\n\n"
        f"Message:\n{contact.message}"
    )

    try:
        sent = _send_contact_email(contact, subject, email_body)
    except Exception:
        logger.exception(
            "Contact email failed for message %s (to=%s)",
            contact.id,
            settings.CONTACT_EMAIL,
        )
        sent = False
    else:
        logger.info(
            "Contact email %s for message %s (to=%s)",
            "sent" if sent else "was not accepted",
            contact.id,
            settings.CONTACT_EMAIL,
        )

    if not sent:
        return Response(
            {
                "message": (
                    "Your message was saved, "
                    "but the email could not be sent."
                )
            },
            status=500
        )

    return Response(
        {"message": "Your message has been sent successfully!"},
        status=201
    )
