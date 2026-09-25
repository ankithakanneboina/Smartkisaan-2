from django.db import models


class GovernmentScheme(models.Model):
    """
    Section 15: admin-managed government scheme data. Per the spec's
    explicit instruction ("Do not invent government scheme information"),
    this app ships with NO seed data — real scheme details must be
    entered via /admin/ from an official source, not generated here.
    """
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    eligibility = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    required_documents = models.TextField(blank=True)
    application_process = models.TextField(blank=True)
    official_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
