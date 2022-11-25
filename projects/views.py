from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
#import the form we created 
from .forms import ProjectForm, ReviewForm
from .helpers import searchProjects, paginateProjects


# Create your views here.

# reference: https://docs.djangoproject.com/en/3.2/topics/pagination/
# For the home page
def projects(request):
    search_query, projects = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    
    context = {"projects": projects, "search_query": search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

# For a single project
def project(request, pk):
    # set the UUID of the project equals to primary key(aka pk)
    # get all the projects and their tags
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = projectObj.tags.all()
    # print('projectObj:', projectObj)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        # Update project vote count
        messages.success(request, "Your review was successfully submitted")
        
        # redirect the user to the project page
        return redirect('project', pk=projectObj.id)
    
    return render(request, 'projects/single-project.html', {"project": projectObj, "form": form, 'tags': tags})


@login_required(login_url='login')
def createProject(request):
    # get the profile of the currently logged-in user 
    profile = request.user.profile

    # instantiate the class ProjectForm
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get("newtags").replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)

            # set the currently logged-in user to the owner of project
            project.owner = profile
            project.save()
            # BUG: can add new tags but can't delete them...
            for tag in newtags:
                # get or create the tags
                tag, created = Tag.objects.get_or_create(name=tag)
                # adding the tags to the project
                project.tags.add(tag)

            return redirect('projects')

            
    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    # get the project (belonged to the current logged-in user), update it and set its id to primary key
    project = profile.project_set.get(id=pk)
    # instantiate the class ProjectForm with that project
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        # the split method will split a string into a list(default separator is  any whitespace)
        newtags = request.POST.get("newtags").replace(",", " ").split()
        
        # pass in the instance
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                # get or create the tags
                tag, created = Tag.objects.get_or_create(name=tag)
                # adding the tags to the project
                project.tags.add(tag)

            return redirect('account')

            
    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def deleteProject(request, pk):
    # make sure only the owner of certain project can delete them
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('account')
    context = {'object': project}
    return render(request, 'delete_template.html', context)