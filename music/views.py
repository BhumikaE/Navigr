from django.http import HttpResponse
from models import Album, Lists, Position, Notification
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.views.generic import View
from .forms import UserForm, TaskForm, NotifyForm
from django.template import loader
from translate import Translator
from django.http import JsonResponse
from classify import getCategory
from nearby import common_elements, GoogPlac


def index(request):
    all_albums = Album.objects.all()
    template = loader.get_template('music/index.html')
    context = {

        "all_albums" : all_albums,
    }
    html = ''
    return HttpResponse(template.render(context,request))



def get_list(request):
    all_tasks = Lists.objects.all()
    template = loader.get_template('music/todo.html')
    context = {

        "all_tasks" : all_tasks,
    }
    html = ''
    return HttpResponse(template.render(context,request))


'''
   for album in all_albums:
        id = album.id
        url = "/music/" + str(id) + "/"
        html += "<a href="+ url + "> " + album.artist +" </a><br> "

'''
def play(request):
    translator = Translator(to_lang="zh")
    translation = translator.translate("This is a pen.")
    return HttpResponse(translation)

def details(request, album_id):
    return HttpResponse("<h1> music id :" + str(album_id) + "</h1>")

def routes(request):
    template = loader.get_template('music/routes.html')
    return HttpResponse(template.render('',request))

def todo(request):
    template = loader.get_template('music/todo.html')

    if request.method == 'POST':
        return redirect('https://www.google.com')
        #return redirect('https://www.google.com')
        form = TaskForm(request.POST)
        if form.is_valid():
            return redirect('https://www.google.com')
            user = form.save(commit=False)
            task = form.cleaned_data['custom_textbox']
            user.save()

    return HttpResponse(template.render('',request))


def login(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
  #      return HttpResponse("sdff",password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                #albums = Album.objects.filter(user=request.user)
                return redirect('lists')
            else:
                return render(request, 'music/index.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/index.html', {'error_message': 'Invalid login'})


def logout_user(request):
    logout(request)
    return render(request, 'music/index.html')

class StartSearch(View):
    form_class = ""



class CreateLists(View):

    form_class = TaskForm
    template_name = "music/todo.html"



    def get(self, request):

        if not request.user.is_authenticated():
            return render(request, 'music/index.html')

        form = self.form_class(None)
        user_id = request.user.id

        lists = Lists.objects.all().filter(user_id= user_id).order_by('-id')
        all_notifications = Notification.objects.all()
        notification_count = all_notifications.count()
        #all_notifications = Notification.objects.all().count()
        return render(request, self.template_name, {'form' : form , 'lists' : lists, 'all_notifications' : all_notifications , 'notification_count': notification_count})

    def post(self,request):
        #return redirect('https://www.google.com')
        #  return redirect('https://www.google.com')
        #return redirect('https://www.google.com')
        user_id = request.user.id

        lists = Lists.objects.all().filter(user_id= user_id).order_by('-id')
        all_notifications = Notification.objects.all()
        notification_count = all_notifications.count()


        form = TaskForm(request.POST)
        if form.is_valid():
            my_task = form.save(commit=False)
            task = form.cleaned_data['task']
            task_category = getCategory(task)

            add_task = Lists.objects.create(task=task, user_id = user_id, category = task_category)

        return render(request, self.template_name, {'form' : form , 'lists' : lists, 'all_notifications' : all_notifications , 'notification_count': notification_count})


class UserFormView(View):
    form_class = UserForm
    template_name = "music/registration_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form })

    def post(self,request):
        #return redirect('https://www.google.com')
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    #request.user
                    return redirect('index')

        return render(request, self.template_name, {'form': form})


def view_list(request):

        lists = Lists.objects.all()
        return render(request, 'music/view_list.html', {
                'lists': lists,
            })

def add_new_task(request):
    task = request.GET.get('task', None)

    add_task = Lists.objects.create( task = task)
    add_task.save()
    #all_tasks = Lists.objects.all()
    #template = loader.get_template('music/todo.html')
    #context = {

       # "all_tasks" : all_tasks,
    #}
    html = ''
    return JsonResponse("")

def delete_task(request, id):

    list = Lists.objects.get(pk=id)
    list.delete()
    lists = Lists.objects.filter(user=request.user)
    return redirect('/music/todo.html')
    return render(request, 'music/todo.html', {'lists': lists})


def start_search(request, user_id):
    '''
        try:

        lists = Position.objects.get(user_id=user_id)
        current_latitude = 19.1239
        current_longitude = 72.8361
        pl = (GoogPlac(current_latitude, current_longitude, 500,
                       'department_store,store,bakery,beauty_salon,bicycle_store,book_store,car_repair,clothing_store,electronics_store,florist,furniture_store,hair_care,hardware_store,jewelry_store,laundary,pet_store,pharmacy,plumber,shoe_store,shopping_mall',
                       'AIzaSyA6udyv0riUcZQnn_8TqzqMjOevOIcZHX4'))

        categories = Lists.objects.filter(user_id=user_id).values('category')
        #print categories
        myList = []

        for i in range(len(categories)):
            myList.append(categories[i]["category"])
            #   print myList
            # category_list = list(categories)


        list1 = myList

        #print list1
        #print list1
        storeName=""
        store_type=""
        store_latitude=""
        store_longitude=""
        all_store_names=""
        all_store_types=""

        for i in range(len(pl['results'])):
            if len(common_elements((pl['results'][i]['types']), list1)) != 0:
#                storeName = storeName.join(pl['results'][i]['name'])
#               store_type = store_type.join(common_elements((pl['results'][i]['types']), list1))


                #   print storeName
                #  print store_type
                #        store_latitude = store_latitude.join(pl['results'][i]['latitude'])
                #       store_longitude = store_longitude.join(pl['results'][i]['longitude'])
                #                all_store_names = all_store_names + storeName
                #               all_store_types = all_store_types + " " + store_type
                add_position = Notification.objects.create(user_id=user_id,
                                                           store_name=pl['results'][i]['name'])

        all_notifications = Notification.objects.all()
        render(request,'music/todo.html',{"all_notifications": all_notifications})


    except Position.DoesNotExist:
        add_position = Position.objects.create(user_id=user_id)
        current_latitude = 19.1239
        current_longitude = 72.8361
        pl = (GoogPlac(current_latitude, current_longitude, 500,
                       'department_store,store,bakery,beauty_salon,bicycle_store,book_store,car_repair,clothing_store,electronics_store,florist,furniture_store,hair_care,hardware_store,jewelry_store,laundary,pet_store,pharmacy,plumber,shoe_store,shopping_mall',
                       'AIzaSyA6udyv0riUcZQnn_8TqzqMjOevOIcZHX4'))

        categories = Lists.objects.filter(user_id=user_id).values('category')

        myList = []

        for i in range(len(categories)):
            myList.append(categories[i]["category"])

        list1 = myList

        for i in range(len(pl['results'])):
            if len(common_elements((pl['results'][i]['types']), list1)) != 0:
                add_position = Notification.objects.create(user_id=user_id,
                                                           store_name=pl['results'][i]['name'])

        all_notifications = Notification.objects.all()
        render(request, 'music/todo.html', {"all_notifications": all_notifications})

    lists = Lists.objects.all().filter(user_id=user_id).order_by('-id')
    return redirect('/music/todo.html')
    return render(request, 'music/todo.html', {'lists':lists,'add_position': add_position})

    '''


def get_directions(request):
    template_name = "music/getdirections.html"

    return render(request, template_name)

