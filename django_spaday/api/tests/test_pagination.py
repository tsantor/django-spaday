# import pytest
# from django.urls import reverse

# from myapp.models import MyModel
# from django.contrib.auth.models import Permission


# @pytest.fixture
# def my_models(db):
#     # Assuming MyModel has no required fields
#     MyModel.objects.bulk_create([MyModel() for _ in range(50)])


# def test_standard_pagination(api_client, my_models):
#     response = api_client.get(reverse('my_view'))
#     assert response.status_code == 200
#     assert 'current_page' in response.data
#     assert 'num_pages' in response.data
#     assert 'start_index' in response.data
#     assert 'end_index' in response.data
#     assert 'num_results' in response.data
#     assert 'results' in response.data
#     assert len(response.data['results']) == 10  # Default page size
