from rest_framework import serializers

from .models import Project, Pledge

# A serializer is an import/export of data
# taking data from a raw form and converting it into a computer readable form and then doing the reverse too.
# converting from computer native to something else (like JSON)
#we didn't make the date_created the same as the models Project class because the model has already done the job, the serializer is just inferring from the model instructions already input.

class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_active = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


# using **validated_data is a dictionary. so we are asking the serializer to create a dictionary, the asterisk is saying take everything that is here and return it as pairs. so it will be like, description = the thing, key = the value. 

class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        fields = ['id', 'amount', 'comment', 'anonymous', 'project', 'supporter']
        


# ModelSerializer interprets
# to add ALL your fields, you could have written fields = '__all__' which would import ALL your fields