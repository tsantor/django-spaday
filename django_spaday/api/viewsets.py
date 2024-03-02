from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers.deleted import DeletedObjectsSerializer  # noqa
from .utils import get_deleted_objects


class MyModelViewSet(ModelViewSet):
    @action(detail=True, url_path=r"confirm-delete")
    def pre_delete(self, request, pk=None):
        """Return info about what would be deleted."""
        obj = self.get_object()

        deleted_objects, model_count, protected = get_deleted_objects([obj])

        ctx = {
            "deleted_objects": deleted_objects,
            "model_count": dict(model_count).items(),
            "protected": protected,
            "model": str(obj._meta.verbose_name),
        }
        return Response(ctx)
        # return Response(DeletedObjectsSerializer(ctx).data)
