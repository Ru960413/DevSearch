from random import choices
from django.db import models
import uuid
from users.models import Profile


# Create your models here.

# create classes that are going to represent table
# the class Project is inherited from models.Model
class Project(models.Model):
    # ON_DELETE: model.cascade -> delete the project when its owner s deleted  
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete= models.CASCADE)
    # creating a title column which can accept at most 200 characters
    title = models.CharField(max_length = 200)
    feature_image = models.ImageField(null=True, blank=True, default="default.jpg")
    # creating a description column which can take null as its value
    # and we can submit a form when this field is empty
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length = 2000, null=True, blank=True) 
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # create many to many relationship between the tag table and the project table
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # creating a column which shows when we added the project
    created = models.DateField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        # order by the created field(ascending first), if add a "-" in front of it (like: ['-created']) then it's newest first
        ordering=['-vote_ratio', '-vote_total', 'title']

        
    @property
    def imageURL(self):
        try:
            url = self.feature_image.url
        except:
            url = '/images/default.jpg'

        return url

    @property
    def reviewers(self):
        # return a list of values which have owner__id as their key
        # (If flat = True, this will mean the returned results are single values, rather than one-tuples.)

        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
    
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value="up").count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


# Run make migration command using "python3 manage.py makemigrations", which will then prep for SQL commands

# And then run "python3 manage.py migrate" to execute the actual migration
    
#Anytime we add or update a model field, we need to do these

class Review(models.Model):
    # create a tuple:The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name. 
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    # tie the current table to the project table, and once the project is deleted all the reviews connected to the project will be deleted at the same time
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length = 200, choices=VOTE_TYPE)
    created = models.DateField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value
    
    class Meta:
        # This is a list of lists that must be unique when considered together. 
        # Make sure that no one can leave more than one review for a project
        unique_together = [['owner', 'project']]

    
    
        


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name