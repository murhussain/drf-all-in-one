from abc import ABC

from rest_framework import serializers

from movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"
        # fields = ['id', 'name', 'description']
        # exclude = ['active']

    # Get the length of the name in the serializer out put
    def get_len_name(self, object):
        return len(object.name)

    # Object-level validation
    def Validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("The Name should not look the same as description")
        else:
            return data

    #  Field-level validation
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name is Too Short")
        else:
            return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#     #  Object-level validation
#     def Validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("The Name should not look the same as description")
#         else:
#             return data
#
#     #  Field-level validation
#     def validate_name(self, value):
#         if len(value) < 3:
#             raise serializers.ValidationError("Name is Too Short")
#         else:
#             return value
