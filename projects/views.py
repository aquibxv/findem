from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from datetime import datetime
from .models import Project
from django.core.paginator import Paginator
from django.db.models import Q
from profiles.models import UserProfile
from projects.choices import project_type_choices
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create(request):
    """defines a view for creating a new project"""

    if request.method == 'POST' :

        # Get form value
        user = request.user
        author = request.POST.get('project-author')
        title = request.POST.get('project-name')
        description = request.POST.get('project-descirpt')
        college = request.user.college_name
        skill_1 = request.POST.get('upload_skill1', ' ')
        skill_2 = request.POST.get('upload_skill2', ' ')
        skill_3 = request.POST.get('upload_skill3', ' ')
        skill_4 = request.POST.get('upload_skill4', ' ')
        photo_1 = request.POST.get('upload_file1')
        photo_2 = request.POST.get('upload_file2')
        photo_3 = request.POST.get('upload_file3')
        link_1 =  request.POST.get('upload_link1', ' ')
        link_2 =  request.POST.get('upload_link2', ' ')
        link_3 =  request.POST.get('upload_link3', ' ')
        domain =  request.POST.get('project-domain')
        project_type = request.POST.get('project-type')
        resume_inclusion = request.POST.get('project-resume-add', 'false')
        live = request.POST.get('project-live', 'false')
        deadline = request.POST.get('project-deadline')
        upload_date = datetime.now()

        # create the object
        project = Project.objects.create(user=user, author=author, title=title, description=description,
        college=college, skill_1=skill_1, skill_2=skill_2, skill_3=skill_3, skill_4=skill_4, photo_1=photo_1, photo_2=photo_2,
        photo_3=photo_3, link_1=link_1, link_2=link_2, link_3=link_3, domain=domain, project_type=project_type,
        resume_inclusion=resume_inclusion, live=live, deadline=deadline, upload_date=upload_date)

        # update the project_count for the user
        user.project_count = user.project_count + 1;
        user.save()

        messages.success(request, "Your project has been posted successfully")
        return redirect('dashboard')

    return render(request, 'projects/createproject.html' )

@login_required
def search(request):
    """defines a view for searching for projects"""

    project_list = Project.objects.order_by('-upload_date'
                    ).exclude(user_id=request.user.id)
        
    # college
    if 'college' in request.GET:
        college = request.GET['college']
        if college:
            project_list = project_list.filter(college__icontains=college)

    # project_type
    if 'project_type' in request.GET:
        project_type = request.GET['project_type']
        if project_type:
            project_list = project_list.filter(project_type__iexact=project_type)

    # keyword
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            project_list = project_list.filter(description__icontains=keyword)

    # domain
    if 'domain' in request.GET:
        domain = request.GET['domain']
        if domain:
            project_list = project_list.filter(domain__icontains=domain)

    # skill
    if 'skill' in request.GET:
        skill = request.GET['skill']
        if skill:
            project_list = project_list.filter(Q(skill_1__icontains=skill) | Q(skill_2__icontains=skill) |
            Q(skill_3__icontains=skill) | Q(skill_4__icontains=skill))

    # live
    if 'live' in request.GET:
        live = request.GET['live']
        if live == "on":
            project_list = project_list.filter(live__iexact="on")

    paginator = Paginator(project_list, 3)
    page = request.GET.get('page')

    context = {
        'project_list' : paginator.get_page(page),
        'values' : request.GET,
        'project_type_choices' : project_type_choices,
    }

    return render(request, 'projects/search.html', context)

@login_required
def project_view(request, project_id):
    """defines a view for viewing a project"""

    # fetching project
    project = get_object_or_404(Project, pk=project_id)
    author = UserProfile.objects.get(id=project.user_id)

    context = {
        'project' : project,
        'author' : author,
    }

    return render(request, 'projects/project_view.html', context)

@login_required
def project_delete(request, project_id):
    """defines a view for deleting a project"""

    #fetch the project and delete
    project = Project.objects.get(id = project_id)
    project.delete()

    request.user.project_count = request.user.project_count - 1;
    request.user.save()

    return redirect('my_project')

@login_required
def project_edit(request, project_id):
    """defines a view for editing a project"""

    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        
        user = request.user
        author = request.POST.get('project-author')
        title = request.POST.get('project-name')
        description = request.POST.get('project-descirpt')
        college = request.user.college_name
        skill_1 = request.POST.get('upload_skill1', ' ')
        skill_2 = request.POST.get('upload_skill2', ' ')
        skill_3 = request.POST.get('upload_skill3', ' ')
        skill_4 = request.POST.get('upload_skill4', ' ')
        photo_1 = request.POST.get('upload_file1', None)
        photo_2 = request.POST.get('upload_file2', None)
        photo_3 = request.POST.get('upload_file3', None)
        link_1 =  request.POST.get('upload_link1', ' ')
        link_2 =  request.POST.get('upload_link2', ' ')
        link_3 =  request.POST.get('upload_link3', ' ')
        domain =  request.POST.get('project-domain')
        project_type = request.POST.get('project-type')
        resume_inclusion = request.POST.get('project-resume-add', 'false')
        live = request.POST.get('project-live', 'false')
        deadline = request.POST.get('project-deadline')

        # update and saves the object
        if project.title != title:
            project.title = title
        if project.description != description:
            project.description = description
        if project.skill_1 != skill_1:
            project.skill_1 = skill_1
        if project.skill_2 != skill_2:
            project.skill_2 = skill_2
        if project.skill_3 != skill_3:
            project.skill_3 = skill_3
        if project.skill_4 != skill_4:
            project.skill_4 = skill_4
        if project.photo_1 != photo_1:
            project.photo_1 = photo_1
        if project.photo_2 != photo_2:
            project.photo_2 = photo_2
        if project.photo_3 != photo_3:
            project.photo_3 = photo_3
        if project.link_1 != link_1:
            project.link_1 = link_1
        if project.link_2 != link_2:
            project.link_2 = link_2
        if project.link_3 != link_3:
            project.link_3 = link_3
        if project.domain != domain:
            project.domain = domain
        if project.project_type != project_type:
            project.project_type = project_type
        if project.resume_inclusion != resume_inclusion:
            project.resume_inclusion = resume_inclusion
        if project.live != project.live:
            project.live = live
        if project.deadline != deadline:
            project.deadline = deadline

        project.save()

        # return redirect(request, 'dashboard')

    context = {
        'project' : project,
        'project_type_choices' : project_type_choices,
    }

    return render(request, 'projects/project_edit.html', context)
