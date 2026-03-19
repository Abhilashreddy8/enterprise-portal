from django.test import TestCase

# Create your tests here.
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_get_reports():

    client = APIClient()

    response = client.get("/api/reports/")

    assert response.status_code in [200, 401]

from django.contrib.auth.models import User

@pytest.mark.django_db
def test_authenticated_api():

    user = User.objects.create_user(
        username="testuser",
        password="test123"
    )

    client = APIClient()

    client.force_authenticate(user=user)

    response = client.get("/api/reports/")

    assert response.status_code == 200

@pytest.mark.django_db
def test_create_report():

    user = User.objects.create_user(
        username="testuser",
        password="test123"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "title": "Test Report",
        "status": "Uploaded"
    }

    response = client.post("/api/reports/", data)

    assert response.status_code == 200