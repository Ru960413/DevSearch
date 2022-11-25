from django.shortcuts import render, redirect
from . models import Profile, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .helpers import searchProfiles, paginateProfiles



# Create your views here.

def loginUser(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        # check if there's the username in db
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        # user authentication, check if username and password matches the ones in db
        user = authenticate(request, username=username, password=password)

        # login the user if authentication successful
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
        else:
            messages.error(request, "Username or password is incorrect")
        
    return render(request, "users/login_register.html")

    
def logoutUser(request):
    logout(request)
    messages.success(request, "User is successfully logged out")
    return redirect("login")


def register(request):
    page = 'register'
    form = CustomUserCreationForm()

    # processing the form to make sure username is all lowercase
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")

            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.error(request, "An error has occurred during registration")

    context = {'page': page, 'form':form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    # exclude the description that has an empty string and assign it to topSkills
    topSkills = profile.skill_set.exclude(description__exact="")
    #filter the profile with empty description(include those), and assign the filtered ones to otherSkills
    otherSkills = profile.skill_set.filter(description="")

    context={'profile':profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    Skills = profile.skill_set.all()
    projects = profile.project_set.all()
    

    context = {'profile': profile, 'skills': Skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    # pre-fill all the fields 
    form = ProfileForm(instance=profile)
    

    if request.method == "POST":
        # we have to pass request.FILES into the form’s constructor; this is how file data gets bound into a form.
        #  request.FILES will only contain data if the request method was POST
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')



    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'SKill was added successfully!')
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request,pk):
    # get the profile and skills from the logged-in user and only change the skill when id=pk
    profile = request.user.profile
    skill=profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'SKill was updated successfully!')
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, 'SKill was deleted successfully!')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)



@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context={'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)



@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message':message}

    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            # the sender can be None
            message.sender = sender
            message.recipient = recipient

            if sender:
                # if there are name and email in form,
                # save their name and email
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form':form}
    return render(request, 'users/message_form.html', context)
