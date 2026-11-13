from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile_api, name="profile-api"),
    path("projects/", views.projects_api, name="projects-api"),
    path("skills/", views.skills_api, name="skills-api"),
    path("education/", views.education_api, name="education-api"),
    path("experience/", views.experience_api, name="experience-api"),
    path("contact/", views.contact_api, name="contact-api"),
]