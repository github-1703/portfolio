from django.shortcuts import render

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
        serializer.save()

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