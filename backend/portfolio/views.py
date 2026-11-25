import json
import logging
import time
import traceback
from contextlib import redirect_stderr
from io import StringIO

from django.shortcuts import render
from django.conf import settings 
from django.core import mail
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

def _email_diagnostics(email):
    """Run one real SMTP send and return everything needed to debug it."""
    info = {
        "backend": settings.EMAIL_BACKEND,
        "host": settings.EMAIL_HOST,
        "port": settings.EMAIL_PORT,
        "use_tls": getattr(settings, "EMAIL_USE_TLS", None),
        "host_user": settings.EMAIL_HOST_USER,
        "password_set": bool(settings.EMAIL_HOST_PASSWORD),
        "password_len": len(settings.EMAIL_HOST_PASSWORD or ""),
        "default_from": settings.DEFAULT_FROM_EMAIL,
        "contact_email": settings.CONTACT_EMAIL,
        "timeout": getattr(settings, "EMAIL_TIMEOUT", None),
        "recipients": email.recipients(),
    }

    output = StringIO()
    started = time.time()
    try:
        connection = mail.get_connection(fail_silently=False)
        connection.open()
        try:
            connection.connection.set_debuglevel(1)
        except Exception:
            pass
        with redirect_stderr(output):
            info["sent"] = connection.send_messages([email])
        connection.close()
        info["ok"] = True
    except Exception as exc:
        info["ok"] = False
        info["error"] = f"{type(exc).__name__}: {exc}"
        info["traceback"] = traceback.format_exc()[-1200:]

    info["elapsed"] = round(time.time() - started, 3)
    info["smtp_log"] = output.getvalue()[-2500:]
    return json.dumps(info, default=str, indent=2)


@api_view(["POST"])
def contact_api(request):
    serializer = ContactMessageSerializer(data=request.data)#Receives submitted JSON data

    if serializer.is_valid():
        contact=serializer.save()
        subject= f"Portfolio Contact from {contact.name}"
        
        email_body = (
            f"Name: {contact.name}\n"
            f"Email: {contact.email}\n\n"
            f"Message:\n{contact.message}"
        )

        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],#my mail
            reply_to=[contact.email],
        )

        # TEMPORARY diagnostic: a probe submission stores the real SMTP
        # transcript on the message row so it can be inspected from the
        # database without exposing it publicly. Remove once resolved.
        if contact.email.strip().lower() == "diag@local.test":
            contact.message = "DIAG\n" + _email_diagnostics(email)
            contact.save(update_fields=["message"])
            return Response(
                {"message": "Diagnostic stored."},
                status=201
            )

        try:
            sent = email.send(fail_silently=False)
            logger.info(
                "Contact email %s for message %s (to=%s)",
                "sent" if sent else "was not accepted",
                contact.id,
                settings.CONTACT_EMAIL,
            )

        except Exception:
            logger.exception(
                "Contact email failed for message %s (to=%s)",
                contact.id,
                settings.CONTACT_EMAIL,
            )
            return Response(
                {
                    "message": (
                        "Your message was saved, "
                        "but the email could not be sent."
                    )
                },
                status=500
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
            {
                "message": "Your message has been sent successfully!"
            },
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )