from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')
    
    # let each page has 3 projects
    # results = 3
    paginator = Paginator(list(profiles), results)
    try:
        profiles = paginator.page(page)
    # if user is visiting the page for the first time set page to 1
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)

    # if user is trying to access a page that is empty then direct them to the last page
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    # 一次只顯示十頁
    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 5

    # 要記得＋１不然會少一頁
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles



def searchProfiles(request):
    # if there's no search then all the profiles will be included (no filter)
    search_query = ''

    # if there's a search query 
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
    # then the profile will be filtered(i for case insensitively)and see if the profile's name field or short_intro field contains the search_query 
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query)| Q(short_intro__icontains=search_query) | Q(skill__in=skills))

    return profiles, search_query