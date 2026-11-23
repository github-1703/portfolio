from django.shortcuts import render
from django.conf import settings 
from django.core.mail import EmailMessage

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile,Project,Skill,Education,Experience
from .serializers import ProfileSerializer,ProjectSerializer,SkillSerializer,EducationSerializer,ExperienceSerializer,ContactMessageSerializer


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

        try:
            email.send(fail_silently=False)

        except Exception:
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