from django.shortcuts import render
from django.http import HttpResponse
import json
from bluray.models import *
# Create your views here.

def index(request):
	movie_list = Movie.objects.filter(released=False)
	context = {
		'user_tracking' : [movie.name for movie in request.user.movie_set.all()],
		'movie_list' : movie_list,
	}

	return render(request, 'bluray/index.html', context)

'''
should probably make sure user is logged in
'''
def track(request):
	results = {'success':'False'}
	if request.method == 'GET':
		GET = request.GET
		if GET.has_key('id') and GET.has_key('track'):
			id_in = int(GET['id'])
			track = GET['track']
			user = request.user

			movie = Movie.objects.get(id=id_in)
			if track == "Track":
				movie.tracking.add(user)
			elif track == "Untrack":
				movie.tracking.remove(user)
			movie.save()
			success = '%s %s' %(user.username, track)
			results = {'success':success}

	jason = json.dumps(results)
	return HttpResponse(jason, content_type='application/json')
