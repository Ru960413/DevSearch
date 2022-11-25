from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):

    page = request.GET.get('page')
    
    # let each page has 3 projects
    # results = 3
    paginator = Paginator(list(projects), results)
    try:
        projects = paginator.page(page)
    # if user is visiting the page for the first time set page to 1
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)

    # if user is trying to access a page that is empty then direct them to the last page
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # 一次只顯示十頁
    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 5

    # 要記得＋１不然會少一頁
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects



def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags =Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query)|
        Q(owner__name__icontains=search_query)|
        Q(tags__in=tags)
    )

    return search_query, projects