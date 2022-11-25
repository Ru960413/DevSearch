# turn any Python data into Json format
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from . serializers import ProjectSerializer
from projects.models import Project, Review, Tag

# if we add IsAuthenticated as the parameter for the permission class that means we need to add Json web token in order to access the view, (i.e. to get permission), which we can add in Postman's header

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/vote'},

        # generate tokens for users(like class based views)
        {'POST': '/api/users/token'},
        # generate a new token for user, so user stay logged in
        {'POST': '/api/users/token/refresh'},
    ]

    # The first parameter, data, should be a dict instance.
    # If the safe parameter is set to False it can be any JSON-serializable object.
    # return JsonResponse(routes, safe=False)

    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    # need to pass in request.user because we are using the api_view decorator
    print("USER:", request.user)
    # get all the projects
    projects = Project.objects.all()

    # the serializer will take the query sets and turn them into Json data
    # serializer is a object here
    serializer = ProjectSerializer(projects, many=True)
    # we use .data to access the data in the serializer object
    # it'll return a list of dictionaries
    return Response(serializer.data)



@api_view(['GET'])
def getProject(request, pk):
    # get the single project
    project = Project.objects.get(id=pk)

    # the serializer will take the project instance and turn it into Json data
    # serializer is a object here
    serializer = ProjectSerializer(project, many=False)

    # we use .data to access the data in the serializer object
    # it'll return a single dictionary
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    # the get_or_create method will either get the object or create the object(here it's the review), depending on whether the object has already existed or not(if not then created=True)
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project
    )
    # print(review, created)
    # update the value of the review with the value, which is sent via POST method through API in Postman
    review.value = data['value']
    review.save()

    # trigger the property for this project and update total votes and vote ratio 
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data["tag"]
    projectId = request.data["project"]

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)
    return Response("Tag was deleted")
