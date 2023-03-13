from rest_framework import serializers

from .models import Project, Pledge, Category

from users.serializers import CustomUserSerializer

#### NOTES ON SERIALIZERS #####
        # - A serializer is an import/export of data
        # - it's taking data from a raw form and converting it into a computer readable form and then doing the reverse too (e.g. from comp. native to JSON).
        #A serializer is just inferring from the model instructions already input.
        # Each field in the model generally corresponds to a column in the database. 
            # Each field of the model has a specific definition in the sense of the data it stores or the type of field it is. It can be a CharField or IntegerField, a ManytoManyField or a OneToManyField or just be a ForeignKey. 
            # We can also define the minimal validation requirements, used in Django’s admin and in automatically-generated forms.
            #  It is crucial to remember that these fields are important as they will go on to define our database.
        # when you execute the Python command to run migrations, Django performs a system check and creates the necessary tables in the database.
#### NOTES ON SERIALIZERS #####


#### PLEDGE SERIALIZER ####
         ##This is the serializer for parsing model info about pledges from users & the required fields ####
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

#### PLEDGEDETAILSERIALIZER ####
        # This is pulling all the fields in the pledge id model as a list
# class PledgeDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pledge
#         fields = []


#### PROJECTSERIALIZER ####
        ##This is the serializer for parsing model info about individual project & the required fields ####
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
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())


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
        # using **validated_data is a dictionary. 
        # so we are asking the serializer to create a dictionary, the asterisk is saying take everything that is here and return it as pairs. 
        # so it will be like, description = the thing, key = the value. 
class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
# This serializer is saying, add specific pledges corresponding to my project against the individual project.

class ProjectSearch(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
    # This is a serializer to be used in serach views which is partsing all fields from the Project Model.


# This is to create category
class CategorySerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField()

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

# This is to update a specific category
class CategoryDetailSerializer(CategorySerializer):
        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.slug = validated_data.get('slug', instance.slug)
            instance.save()
            return instance
        # Tried to do tags nested in ProjectSerializer, but decided on sep. category instead as easier..