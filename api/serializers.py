from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

# Doc: https://www.django-rest-framework.org/tutorial/1-serialization/

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'     

        

class ProjectSerializer(serializers.ModelSerializer):
    # connect the owner using ProfileSerializer
    # it'll then gives us all the info about the owner
    owner = ProfileSerializer(many = False)

    # connect the tags using TagSerializer
    tags = TagSerializer(many=True)

    # SerializerMethodField is a read-only field. It gets its value by calling a method on the serializer class it is attached to. It can be used to add any sort of data to the serialized representation of your object.(here the reviews are attached to project, so we call the SerializerMethodField method under it, and add the data of review into each project)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, object):
        # get all the reviews
        reviews = object.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
    