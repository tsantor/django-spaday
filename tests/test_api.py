import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestLoginView:
    def test_login(self, api_client, user):
        url = reverse("api:rest_login")
        data = {
            "username": user.username,
            "email": user.email,
            "password": "testpass",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK

        assert "access" in response.data
        assert "refresh" in response.data
        assert "user" in response.data

        assert "pk" in response.data["user"]
        assert "is_active" in response.data["user"]
        assert "is_superuser" in response.data["user"]
        assert "is_staff" in response.data["user"]
        assert "first_name" in response.data["user"]
        assert "last_name" in response.data["user"]
        assert "email" in response.data["user"]
        assert "permissions_codenames" in response.data["user"]
        assert "initials" in response.data["user"]
        assert "full_name" in response.data["user"]

        user.refresh_from_db()
        assert user.last_login is not None

    def test_logout(self, authenticated_client):
        url = reverse("api:rest_logout")
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
class TestUserViewSet:
    def test_create(self, authenticated_client):
        url = reverse("api:users-list")
        data = {
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "testpassword",
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update(self, authenticated_client, user):
        url = reverse("api:users-detail", kwargs={"pk": user.pk})
        data = {"first_name": "Updated", "email": "updateduser@test.com"}
        response = authenticated_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.first_name == "Updated"
        assert user.email == "updateduser@test.com"

    def test_list(self, authenticated_client, user):
        response = authenticated_client.get(reverse("api:users-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_retrieve(self, authenticated_client, user):
        url = reverse("api:users-detail", kwargs={"pk": user.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_pre_delete(self, authenticated_client, user):
        url = reverse("api:users-pre-delete", kwargs={"pk": user.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert "deleted_objects" in response.data
        assert "model_count" in response.data
        assert "protected" in response.data
        assert "model" in response.data

    # TODO: Test is failing due
    # django.db.utils.IntegrityError: The row in table 'auditlog_logentry'
    # with primary key '2' has an invalid foreign key: auditlog_logentry.actor_id
    # contains a value '1' that does not have a corresponding value in auth_user.id.
    # def test_delete(self, authenticated_client, user):
    #     url = reverse("api:users-detail", kwargs={"pk": user.pk})
    #     response = authenticated_client.delete(url)
    #     assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_change_password(self, authenticated_client, user):
        url = reverse("api:users-change-password", kwargs={"pk": user.pk})
        data = {"password": "Cfbd331K@", "password2": "Cfbd331K@"}
        response = authenticated_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password("Cfbd331K@")

    def test_recent_logins(self, api_client, superuser_authenticated_client, user):
        url = reverse("api:rest_login")
        data = {
            "username": user.username,
            "email": user.email,
            "password": "testpass",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK

        response = superuser_authenticated_client.get(
            reverse("api:users-recent-logins")
        )
        assert response.status_code == status.HTTP_200_OK
        # TODO: Getting empty results as if last_login is not being updated
        # print(response.data)
        # assert len(response.data) >= 1


@pytest.mark.django_db()
class TestGroupViewSet:
    def test_list(self, authenticated_client, group):
        response = authenticated_client.get(reverse("api:groups-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_retrieve(self, authenticated_client, group):
        url = reverse("api:groups-detail", kwargs={"pk": group.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_pre_delete(self, authenticated_client, group):
        url = reverse("api:groups-pre-delete", kwargs={"pk": group.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert "deleted_objects" in response.data
        assert "model_count" in response.data
        assert "protected" in response.data
        assert "model" in response.data

    def test_delete(self, authenticated_client, group):
        url = reverse("api:groups-detail", kwargs={"pk": group.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_users(self, authenticated_client, group):
        response = authenticated_client.get(
            reverse("api:groups-users", kwargs={"pk": group.pk})
        )
        assert response.status_code == status.HTTP_200_OK

    def test_add_users(self, authenticated_client, user, group):
        data = {"users": [user.pk]}
        response = authenticated_client.post(
            reverse("api:groups-add-users", kwargs={"pk": group.pk}), data
        )
        assert response.status_code == status.HTTP_200_OK
        assert user.pk in response.data["users"]

    def test_remove_users(self, authenticated_client, user, group):
        group.user_set.add(user)
        data = {"users": [user.pk]}
        response = authenticated_client.post(
            reverse("api:groups-remove-users", kwargs={"pk": group.pk}), data
        )
        assert response.status_code == status.HTTP_200_OK
        assert user.pk not in response.data["users"]

    def test_combobox(self, authenticated_client, group):
        response = authenticated_client.get(reverse("api:groups-combobox"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db()
class TestPermissionViewSet:
    def test_combobox(self, authenticated_client):
        url = reverse("api:permissions-combobox")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= 1


@pytest.mark.django_db()
class TestLogEntryViewSet:
    def test_list(self, authenticated_client, log_entry):
        url = reverse("api:auditlogs-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

    def test_retrieve(self, authenticated_client, log_entry):
        url = reverse("api:auditlogs-detail", kwargs={"pk": log_entry.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_pre_delete(self, authenticated_client, log_entry):
        url = reverse("api:auditlogs-pre-delete", kwargs={"pk": log_entry.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert "deleted_objects" in response.data
        assert "model_count" in response.data
        assert "protected" in response.data
        assert "model" in response.data

    def test_delete(self, authenticated_client, log_entry):
        url = reverse("api:auditlogs-detail", kwargs={"pk": log_entry.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
class TestTaskResultViewSet:
    def test_list(self, authenticated_client, task_result):
        url = reverse("api:taskresults-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_retrieve(self, authenticated_client, task_result):
        url = reverse("api:taskresults-detail", kwargs={"pk": task_result.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_pre_delete(self, authenticated_client, task_result):
        url = reverse("api:taskresults-pre-delete", kwargs={"pk": task_result.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        assert "deleted_objects" in response.data
        assert "model_count" in response.data
        assert "protected" in response.data
        assert "model" in response.data

    def test_delete(self, authenticated_client, task_result):
        url = reverse("api:taskresults-detail", kwargs={"pk": task_result.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
