import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import UserFactory


@pytest.mark.django_db()
def test_standard_pagination(authenticated_client):
    num_results = 10  # Default page size
    UserFactory.create_batch(15)
    response = authenticated_client.get(reverse("api:users-list"))
    assert response.status_code == status.HTTP_200_OK
    assert "links" in response.data
    assert "next_page" in response.data
    assert "previous_page" in response.data
    assert "current_page" in response.data
    assert "num_pages" in response.data
    # assert "start_index" in response.data
    # assert "end_index" in response.data
    assert "num_results" in response.data
    assert "results" in response.data
    # print(response.data)
    assert len(response.data["results"]) == num_results
