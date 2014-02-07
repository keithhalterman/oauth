from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
import foursquare 
from models import fs 
from django import forms



def newClient():
    return foursquare.Foursquare(client_id='V3KDK14ZMYZRIIQVIUDPILBYPGD00I5MDYBKSK04P1VMI5F2',
                               client_secret='5RZ0IP0NQNWWUW4EPPICDG43IZHGANA5ASVADNJCDV5W4M0I',
                               redirect_uri='http://ec2-54-80-139-1.compute-1.amazonaws.com/test')


def index(request):
	user_list = User.objects.all()
	return render_to_response("registration/home.html", {
       'user_list': user_list,
       })

    #return HttpResponse("Hello, world. You're at the poll index.")
    

def view2(request):
	return HttpResponse("This is another view")
	
def logout_view(request):
	logout(request)
	return HttpResponse('You have been logged out! <br> <a href="/">Home Page</a><br>')
	
def register(request):
    if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             new_user = form.save()
             return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    c = {'form': form}
    return render_to_response("registration/register.html", c, context_instance=RequestContext(request))


def profile(request, user_id):
    if not request.user.is_authenticated():
		return profile_simple(request, user_id)
    elif str(request.user.id) == str(user_id):
        return profile_full(request, user_id)
    else:
        return profile_simple(request, user_id)

def profile_simple(request, user_id):
	#out = '<a href="/">home</a>'
	#return HttpResponse("You Found my Simple Profile " + user_id + out)
	u = User.objects.filter(id=user_id)
	body = "Simple Profile"
	a = fs.objects.filter(user_id=user_id)
	if len(a) > 0:
		client = userClient(user_id)
		checkin = client.users.checkins()['checkins']['items']
		print 'checkin: ' + str(checkin)
		body = 'Simple Profile. '
		body += '<p> latest checkin: </p>'
		if len(checkin) > 0:
			x = checkin[0]
			body += '<p><b>Venue:</b> ' + str(x['venue']['name']) +\
                    ' <b>shout:</b> ' + str(x['shout']) +\
                    ' <b>Total Checkins:</b> ' + str(x['venue']['stats']['checkinsCount']) + '</p>'
		else:
			body += '<p> No checkins yet</p>'

	else:
		body = 'Simple profile. <p>This user has not yet connected to Foursquare</p>'

	return render_to_response('profile.html', {'username': u[0].username, 'body': body})


def profile_full(request, user_id):
	u = User.objects.filter(id=user_id)
	a = fs.objects.filter(user_id=user_id)
	if (len(a) > 0):
		client = userClient(user_id)
		checks = client.users.checkins()['checkins']['items']
		body = "Full profile. Code = " + a[0].access_token
		body += '<p>Checkins:</p>'
		for x in checks:
			body += '<p><b>Venue:</b> ' + str(x['venue']['name']) +\
				' <b>shout:</b> ' + str(x['shout']) +\
				' <b>Total Checkins:</b> ' + str(x['venue']['stats']['checkinsCount']) + '</p>'
	else:
		body = 'Full profile. <p>No account connected. <a href=\"/oauth/start\">Click here to link accounts</a></p>'
	return render_to_response('profile.html', {'username': u[0].username, 'body': body})
	
def handle_oauth(request):
    code = request.GET.get('code', None)
    client = newClient()
    access_token = client.oauth.get_token(code)
    client.set_access_token(access_token)
    user = client.users()['user']
    userId = request.user.id
    a = fs(user_id=userId, access_token=code, fs_id=user['id'])
    a.save()
    return HttpResponseRedirect("/profile/" + str(userId))


def link_oauth(request):
    client = newClient();
    auth_uri = client.oauth.auth_url()
    return HttpResponseRedirect(auth_uri)
