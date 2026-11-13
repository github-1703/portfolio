from rest_framework import serializers
from .models import Profile,Project,Skill,Education,Experience,ContactMessage

# reate API endpoints so your React frontend can request and display that information.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        


        
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        
class ProjectSerializer(serializers.ModelSerializer):
    technologies = SkillSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = "__all__"
        
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
        
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "subject", "message", "created_at"]
        read_only_fields = ["id", "created_at","subject"]