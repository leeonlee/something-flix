from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from bluray.models import Movie
from rottentomatoes import RT
from datetime import datetime
from time import sleep
from django.conf import settings #API KEY and SCRAPE_DAY
import re

SCRAPE_DAY = getattr(settings, "SCRAPE_DAY", None)
RT_API_KEY = getattr(settings, "RT_API_KEY", None)

'''
Scrape the dates of all movies in the database
Probably want to not scrape for movies already with dates
'''
class Command(BaseCommand):
	help = ''
	option_list = BaseCommand.option_list + (
		make_option('--now', 		#Creates the flag '--now'
		    action='store_true', 	#Stores True inside the specified destination
		    dest='now', 		#Key destination for value to be saved into
		    default=False,		
		    help='Allow command to be run regardless of scrape day'),
        )

	def handle(self, *args, **options):
		if datetime.today().isoweekday() != SCRAPE_DAY and not options['now']:
			print "NOT SCRAPE DAY!!"
			return
		movies = Movie.objects.filter(released=False)
		count = 0
		for movie in movies:

			# can't make more than 5 calls a second so wait a bit
			if count % 5 == 0:
				sleep(2)

			try:
				rt_object = RT(RT_API_KEY).info(movie.rt_id)
				release_date = rt_object['release_dates'].get('dvd', None)
				if release_date:
					# RT release dates look like: 2014-02-13
					movie.release = datetime.strptime(release_date, '%Y-%m-%d').date()
					movie.save()
					print movie.release, movie.name
				else:
					print "No exact date -", movie.name
			except Exception as e:
				print str(movie_name) + ": " + str(e)

			count += 1




