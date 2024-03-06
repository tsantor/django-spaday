from rest_framework import status
from rest_framework.renderers import JSONRenderer

STATUS_NAMES = {
    val: name.replace(f"HTTP_{val}_", "")
    for name, val in status.__dict__.items()
    if not callable(val) and name.startswith("HTTP_")
}


def get_status(code):
    """Get the human readable SNAKE_CASE version of a status code."""
    return STATUS_NAMES.get(code, "UNKNOWN")


class MyJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Modify API response format.
        Example success:
        {
            "code": 200,
            "status": "OK",
            "data": {
                "username": "username"
            }
        }

        Example error:
        {
            "code": 404,
            "status": "NOT_FOUND",
            "errors": [
                {
                    "detail": "Not found."
                }
            ]
        }
        """
        response = renderer_context["response"]

        # Modify the response into a cohesive response format
        modified_data = {
            "code": response.status_code,
            "status": get_status(response.status_code),
        }

        if status.is_client_error(response.status_code) or status.is_server_error(response.status_code):
            modified_data["errors"] = data
        else:
            modified_data["data"] = data

        return super().render(modified_data, accepted_media_type, renderer_context)
