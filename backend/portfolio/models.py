from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    bio = models.TextField()
    email = models.EmailField()
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    technologies = models.ManyToManyField("Skill", blank=True, related_name="projects")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Skill(models.Model):

    CATEGORY_CHOICES = [
        ("language", "Programming Languages"),
        ("backend", "Backend"),
        ("frontend", "Frontend"),
        ("database", "Database"),
        ("tools", "Tools & Technologies"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["category", "name"]


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=150, blank=True)

    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)

    description = models.TextField(blank=True)
    currently_studying = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.degree} - {self.institution}"

    class Meta:
        ordering = ["-start_year"]


class Experience(models.Model):

    EMPLOYMENT_TYPES = [
        ("internship", "Internship"),
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("freelance", "Freelance"),
        ("volunteer", "Volunteer"),
        ("leadership", "Leadership"),
    ]

    position = models.CharField(max_length=150)
    organization = models.CharField(max_length=200)

    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_TYPES, default="internship"
    )

    location = models.CharField(max_length=150, blank=True)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    currently_working = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} - {self.organization}"

    class Meta:
        ordering = ["-start_date"]


# contact message
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ["-created_at"]
