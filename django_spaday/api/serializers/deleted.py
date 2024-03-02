from rest_framework import serializers


class DeletedObjectsSerializer(serializers.Serializer):
    # TODO
    deleted_objects = serializers.ListField(child=serializers.ListField())
    model_count = serializers.ListField(child=serializers.ListField())
    protected = serializers.ListField()
    model = serializers.CharField()
