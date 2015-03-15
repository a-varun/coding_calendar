from django.shortcuts import render

from django.http import HttpResponse

from Respond.models import DataSet

import pytz

import datetime

import json

import xmltodict

import urllib3

import re

Previously_Scraped_Time = ''


def removeStaleData():
	now  = datetime.datetime.now()
	now = pytz.utc.localize(now)	
	DataSet.objects.filter(TOCE__lte= now).delete()

def getDateTime(stri):
	arr = stri.split()
	yyyy, mm, dd = map(int, arr[0].split('-'))
	hh,mi,ss = map(int, arr[1].split(':'))
	return datetime.datetime(yyyy,mm,dd,hh,mi,ss,0,pytz.UTC)

def obtainFromHackerrank():
	http = urllib3.PoolManager()
	rss = http.request('GET','https://www.hackerrank.com/calendar/feed.rss')
	if rss.status != 200:
		return
	rssData = rss.data
	dictData = xmltodict.parse(rssData)
	events = dictData['rss']['channel']['item']
	for event in events:
		tupl = DataSet()
		if not event['title']:
			continue
		tupl.SiteName = event['title']
		if event['url']:
			tupl.ContestURL = event['url']
		tupl.TOCS = getDateTime(event['startTime'])
		tupl.TOCE = getDateTime(event['endTime'])
		if event['description']:
			event['description'] = re.sub('<[^>]*>', '', event['description'])
			event['description'] = re.sub('<[^>]*>', '', event['description'])
			event['description'] = event['description'].strip()
			event['description'] = re.sub('\n', '', event['description'])
			event['description'] = re.sub('[^a-zA-Z0-9,. -]', '', event['description'])
			tupl.Description = event['description']
		if DataSet.objects.filter(SiteName = tupl.SiteName , ContestURL = tupl.ContestURL , TOCS = tupl.TOCS , TOCE = tupl.TOCE).count()!=0:
			continue
		tupl.save()

def scrapeData():
	removeStaleData()
	obtainFromHackerrank()


def giveJson(request):
	if request.method == "GET":
		if 'scrape' in request.GET:
			scrapeData()
		#obtainFromHackerrank()
		#Get the required data
		datas = []

		hourOffset = -5
		minuteOffset = -30
		if 'hour' in request.GET:
			try:
				hourOffset += int(request.GET['hour'])
			except:
				hourOffset += 5				
		else:

			hourOffset += 5

		if 'minute' in request.GET:
			try:
				minuteOffset += int(request.GET['minute'])
			except:
				minuteOffset += 30	
		else:
			minuteOffset += 30

		
		now  = datetime.datetime.now()
		now = pytz.utc.localize(now)
		datas = DataSet.objects.filter( TOCE__gte= now)
		returndic = {}
		returndic['count'] = len(datas)
		returndic['data'] = []
		for data in datas:
			temp = {}
			times = data.TOCS
			timee = data.TOCE
			offst = datetime.timedelta(hours=hourOffset, minutes=minuteOffset)
			#offst = pytz.utc.localize(offst)
			print "Offset", offst
			times+=offst
			timee+=offst
			temp['starttime'] = str(times)
			temp['endtime'] = str(timee)
			temp['URL'] = data.ContestURL
			temp['ID'] = data.ID
			temp['name'] = data.SiteName
			temp['Description'] = data.Description
			returndic['data'].append(temp)
		returndic['data'].sort(key = lambda x: x['starttime'])
		codechef=[]
		topcoder=[]
		hackerrank=[]
		codeforces=[]
		for dic in returndic['data']:
			if 'codechef' in dic['URL'].lower():
				codechef.append(dic)
				continue
			if 'topcoder' in dic['URL'].lower():
				topcoder.append(dic)
				continue
			if 'hackerrank' in dic['URL'].lower():
				hackerrank.append(dic)
				continue
			if 'codeforces' in dic['URL'].lower():
				codeforces.append(dic)
				continue
		returndic['codechefcount'] = len(codechef)
		returndic['codechef'] = codechef

		returndic['topcodercount'] = len(topcoder)
		returndic['topcoder'] = topcoder

		returndic['codeforcescount'] = len(codeforces)
		returndic['codeforces'] = codeforces

		returndic['hackerrankcount'] = len(hackerrank)
		returndic['hackerrank'] = hackerrank

		return HttpResponse(json.dumps(returndic))

def indexit(request):
	return render(request, 'index.html',{})	

if __name__ == "__main__":
	scrapeData()