from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from matchings.models import Hobby, Member, Message, Event
from matchings import views
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError


# datetime library to get time for setting cookie
import datetime as D
import sys

appname = 'MatchXHobby'


# decorator that tests whether user is logged in
def loggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            username = request.session['username']
            try: user = Member.objects.get(username=username)
            except Member.DoesNotExist: raise Http404('Member does not exist')
            return view(request, user)
        else:
            return redirect(to=views.login)
    return mod_view

@loggedin
def home(request, user):
    context = { 'appname': appname }
    return render(request, 'matchings/home.html', context)

def signup(request):
    context = { 'appname': appname }
    return render(request,'matchings/signup.html', context)

def register(request):
    # creates new user if it doesn't exist
    if request.POST['username'] and request.POST['email'] and request.POST['password']:
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        user = Member(username=u)
        user.email = e
        user.set_password(p)
        try: user.save()
        except IntegrityError as e: raise Http404('Username '+u+' already taken: Usernames must be unique')

        context = {
            'appname' : appname,
            'username' : u
        }
        # redirects to login
        return redirect(to=views.login)

    else:
        return redirect(to=views.signup)


def login(request):
    if not ('username' in request.POST and 'password' in request.POST):
        context = { 'appname': appname }

        if 'username' in request.session:
            return redirect(to=views.profile)
        else:
            return render(request,'matchings/login.html',context)
    else:
        username = request.POST['username']
        password = request.POST['password']
        try: member = Member.objects.get(username=username)
        except Member.DoesNotExist: raise Http404('User does not exist')
        if member.check_password(password):
            # remember user in session variable
            request.session['username'] = username
            request.session['password'] = password
            context = {
               'appname': appname,
               'username': username,
               'loggedin': True
            }
            response = redirect(to=views.profile)
            # remember last login in cookie
            now = D.datetime.utcnow()
            max_age = 365 * 24 * 60 * 60  #one year
            delta = now + D.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = D.datetime.strftime(delta, format)
            response.set_cookie('last_login',now,expires=expires)
            return response
        else:
            raise Http404('Wrong password')

def logout(request):
    request.session.flush()
    context = { 'appname': appname }
    return render(request,'matchings/logout.html', context)

@loggedin
def profile(request, user):
    # set birth date to NaN if it's unset
    if user.date_of_birth:
        date = user.date_of_birth.strftime("%d %b, %Y")
    else:
        date = "NaN"

    # gets lists of all hobbies of user
    hobbies = user.getlAllHobbies()
    context = { 'user' : user, 'date' : date, 'hobbies' : hobbies}

    return render(request, 'matchings/profile.html', context)

@loggedin
def edit_profile(request, user):

    if request.method == 'GET':
        date = str(user.date_of_birth)
        hobbies = user.getlAllHobbies()
        h_list = Hobby.getList()

        context = { 'method' : 'GET', 'user' : user, 'date': date, 'hobbies' : hobbies, 'h_list' : h_list }
        return render(request, 'matchings/edit_profile.html', context)

    # saves chages made to the user profile
    elif request.method == 'POST':
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.gender = request.POST['gender']
        if request.POST['dob']:
            user.date_of_birth = request.POST['dob']

        n_hobby = request.POST.getlist('hobby')
        o_hobby = set(user.getlAllHobbies())

        # midifies the hobbies
        # removes all hobbies that have been deselected
        for hobby in o_hobby:
            if hobby not in n_hobby:
                user.removeHobby(hobby=hobby)

        # adds the newly selected hobbies
        for hobby in n_hobby:
            if hobby not in o_hobby:
                user.addHobby(hobby=hobby)

        user.save()

        h_list = Hobby.getList()
        hobbies = user.getlAllHobbies()

        context = { 'user' : user, 'hobbies' : hobbies, 'h_list' : h_list }
        return redirect(to=views.profile)

@loggedin
def upload_image(request, user):

    if 'img_file' in request.FILES:
        image_file = request.FILES['img_file']

        user.picture = image_file
        user.save()
        return HttpResponse(user.picture.url)
    else:
        raise Http404('Image file not received')

def takeSecond(elem):
    return elem[1]

@loggedin
def hobby_matching(request, user):

    u_hobby = set(user.getlAllHobbies())
    # finds all users who have at least one matching hobby
    user_list = set()
    for hobby in u_hobby:
        temp = Member.getAllUserByHobby(hobby=hobby)
        for each in temp:
            user_list.add(each)

    user_list.remove(user)
    # counts the number of matching hobbies
    h_dic = {}
    for mem in user_list:
        i = 0
        m_list = mem.getlAllHobbies()
        m_list = set(m_list)
        for each in m_list:
            if each in u_hobby:
                i += 1
        h_dic[mem] = i

    l_dic = h_dic.items()

    # sort list with key
    l_dic = sorted(l_dic, key=takeSecond, reverse=True)

    context = { 'u_hobby' : u_hobby, 'user_list' : user_list, 'h_dic' : l_dic }

    return render(request, 'matchings/hobby_matching.html', context)

@loggedin
def message_send(request, user):
    if request.method == 'GET':

        u_set = set(Member.getAllMembers());
        u_set.remove(user)

        u_list = list()
        for each in u_set:
            u_list.append(each.username)

        context = { 'username' : user.username, 'u_list' : u_list }

        return render(request, 'matchings/message_send.html', context)

    if request.method == 'POST':
        # sends a provate message to receiver
        if request.POST['msg-sender'] and request.POST['msg-receiver'] and request.POST['msg-text']:
            message = Message()
            message.sender = user
            message.receiver = Member.objects.get(username=request.POST['msg-receiver'])
            message.text = request.POST['msg-text']
            message.time = timezone.now()
            try: message.save()
            except IntegrityError as e: raise Http404('Error : '+e)

            return redirect(to=views.message_outbox)

@loggedin
def message_inbox(request, user):
    # shows all received messages
    messages_list = list(Message.objects.filter(receiver=user))
    messages_list.reverse()

    context = { 'messages' : messages_list }

    return render(request, 'matchings/message_inbox.html', context)

@loggedin
def message_outbox(request, user):
    #shows all sent messages
    messages_list = list(Message.objects.filter(sender=user))
    messages_list.reverse()

    context = { 'messages' : messages_list }

    return render(request, 'matchings/message_outbox.html', context)

@loggedin
def event_create(request, user):

    if request.method == 'GET':
        context = { 'username' : user.username }

        return render(request, 'matchings/event_create.html', context)

    if request.method == 'POST':
        # creates a new event
        event = Event()
        event.owner = user
        event.location = request.POST['evt-loc']
        event.date = request.POST['evt-date']
        event.time = request.POST['evt-time']
        event.title = request.POST['evt-title']
        event.desc = request.POST['evt-desc']
        if(request.POST['evt-type'] == "public"):
            event.public = True
        else:
            event.public = False

        try : event.save()
        except IntegrityError as e: raise Http404('Error : '+str(e))

        return redirect(to=events_private)

def getDateTime(elem):
    return (elem.date, elem.time);

@loggedin
def events_public(request, user):
    # shows all public event
    present = D.date.today()
    events = list(Event.objects.filter(public=True, date__gt=present))
    events = sorted(events, key=getDateTime)

    context = { 'events' : events }
    return render(request, 'matchings/events_public.html', context)

@loggedin
def events_private(request, user):
    # shows all the private and personal events
    events = list(Event.getAllEventOf(user=user))
    events = sorted(events, key=getDateTime)

    context = { 'events' : events }
    return render(request, 'matchings/events_private.html', context)

@loggedin
def join_event(request, user):
    # allows to join a public event
    if 'evt_title' in request.POST:
        evt_title = request.POST['evt_title']

        event = Event.getEventByTitle(title=evt_title)
        if not(event.owner.username == user.username):
            l_reg = list(event.getAllParticipants())
            if user not in l_reg:
                event.addParticipant(user)
            else:
                return HttpResponse("You are already registred for : '"+evt_title+"'")
        else:
            return HttpResponse("You are the owner of the event!\nCan't register for it!")

        event.save()

        return HttpResponse("Registred for : '"+evt_title+"'")
    else:
        raise Http404('Event Title not received!')
