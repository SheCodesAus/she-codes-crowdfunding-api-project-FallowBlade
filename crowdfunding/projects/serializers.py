from rest_framework import serializers

from .models import Project, Pledge

from users.serializers import CustomUserSerializer

# A serializer is an import/export of data
# taking data from a raw form and converting it into a computer readable form and then doing the reverse too.
# converting from computer native to something else (like JSON)
#we didn't make the date_created the same as the models Project class because the model has already done the job, the serializer is just inferring from the model instructions already input. 
# Each field in the model generally corresponds to a column in the database. Each field of the model has a specific definition in the sense of the data it stores or the type of field it is. It can be a CharField or IntegerField, a ManytoManyField or a OneToManyField or just be a ForeignKey. We can also define the minimal validation requirements, used in Django’s admin and in automatically-generated forms. It is crucial to remember that these fields are important as they will go on to define our database.
# when you execute the Python command to run migrations, Django performs a system check and creates the necessary tables in the database — Elegant and Neat. (Django also adds a primary key to the it but this can be overridden.)


#### PLEDGE SERIALIZER ####
#   ##This is the serializer for parsing model info about pledges from users & the required fields ####
#NOTE I'm unsure how this is linked to an individual Project - ask later.
class PledgeSerializer(serializers.ModelSerializer):
   
    supporter = serializers.SerializerMethodField()
    class Meta:
        model = Pledge
        fields = ['id', 'amount', 'comment', 'anonymous', 'project', 'supporter']
        read_only_fields = ['id', 'supporter']
    
    def get_supporter(self, obj):
        if obj.anonymous: #i.e. if anonymous = true
            return None
        else:
            return obj.supporter.username
    
    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)
        
class PledgeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        fields = []

# ModelSerializer interprets
# to add ALL your fields, you could have written fields = '__all__' which would import ALL your fields

#### PROJECTSERIALIZER ####
#   ##This is the serializer for parsing model info about individual project creations & the required fields ####
class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner_id')
    total = serializers.ReadOnlyField()
    # liked_by = serializers.ReadOnlyField()

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title) 
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal',instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    # tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    # update_tags = serializers.ListField(
    #     child=serializers.CharField(max_length=30), write_only=True)
    
    # def create(self, validated_data):
    #     tag_names = validated_data.pop('update_tags')
    #     instance = super().create(validated_data)
    #     user = self.context['request'].user
    #     tags = []
    #     for name in tag_names:
    #         tag, created = Tags.objects.get_or_create(name=name, defaults={'created_by': user})
    #         tags.append(tag)
    #     instance.tags.set(tags)
    #     return instance

    # def update(self, instance, validated_data):
    #     tag_names = validated_data.pop('update_tags')
    #     instance = super().update(instance, validated_data)
    #     user = self.context['request'].user
    #     tags = []
    #     for name in tag_names:
    #         tag, created = Tags.objects.get_or_create(name=name, defaults={'created_by': user})
    #         tags.append(tag)
    #     instance.tags.set(tags)
    #     return instance

    # liked_by= CustomUserSerializer(many=True, read_only=True)

class ProjectSearch(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class PledgeSearch(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        fields = '__all__'
# using **validated_data is a dictionary. so we are asking the serializer to create a dictionary, the asterisk is saying take everything that is here and return it as pairs. so it will be like, description = the thing, key = the value. 

