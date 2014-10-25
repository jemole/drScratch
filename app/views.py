from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from app.models import Project, Dashboard, Attribute, Dead, Sprite, Mastery, Duplicate
# Models for User
from django.contrib.auth.models import User
from app.forms import UploadFileForm, UserForm
from zipfile import ZipFile
# Library for executing shell commands
import os
# Library cast from string to dictionary
import ast
# Authentication Django
from django.contrib.auth import logout, login, authenticate
#from django.contrib.auth.models import User
#Library for using dates
from datetime import datetime, date
from django.utils import simplejson

def loginUser(request):
	"""Log in app to user"""
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/mydashboard')
			else:
				return HttpResponse('user not found')
	else:
		return HttpResponse('error while log in')

def logoutUser(request):
	"""Method for logging out"""
	logout(request)
	return HttpResponseRedirect('/')

def profileSettings(request):
	"""Main page for registered user"""
	return render_to_response("profile.html")

def myHistoric(request):
	"""Show the progress in the application"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	mydashboard = Dashboard.objects.get(user=user)
	projects = mydashboard.project_set.all()
	return render_to_response("historic.html", {'projects': projects},
													context_instance=RequestContext(request))

def main(request):
	"""Main page"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	# The first time that one user enters
	# Create the dashboards associated to users
	createDashboards()
	return render_to_response("main2.html", {'user': user},
											context_instance=RequestContext(request))

def uncompress_zip(zip_file):
	unziped = ZipFile(zip_file, 'r')
	for file_path in unziped.namelist():
		if file_path == 'project.json':
			file_content = unziped.read(file_path)
	show_file(file_content)

def handle_uploaded_file(f):
	# Path where the file zip are found
	dir_zips = '/home/test/dr-scratch/drScratch/dirZips/'	
	fi = dir_zips + f.name
	with open(fi, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return fi

def writeErrorAttribute(dic):
	"""Write in a list the form correct of attribute plugin"""
	lErrors = []
	for key in dic.keys():
		text = ''
		dx = dic[key]
		if key != 'stage':
			if dx["orientation"] == 1:
				text = 'orientation,'
			if dx["position"] == 1:
				text += ' position, '
			if dx["visibility"] == 1:
				text += ' visibility,'
			if dx["costume"] == 1:
				text += 'costume,'
			if dx["size"] == 1:
				text += ' size'
			if text != '':
				text = key + ': ' + text + ' modified but not initialized correctly'
				lErrors.append(text)
			text = None
		else:
			if dx["background"] == 1:
				text = key + ' background modified but not initialized correctly'
				lErrors.append(text)
	return lErrors

def upload_file(request):
	"""Upload file from form POST"""
	if request.method == 'POST':
		form = UploadFileForm(request.POST)
		# Analyze the scratch project
		fileName = handle_uploaded_file(request.FILES['zipFile'])
		# Redirect to dashboard for unregistered user
		d = analyzeProject(fileName)
		#d["numSprite"] = len(d["sprite"])
		#numDeads = len(d["dead"]) / 2
		#d["numDeads"] = numDeads
		#iterator = 0
		#ltexts = []
		#for x in d["dead"]:
		#	if (iterator % 2) == 0:
		#		text = x + ' with '
		#	else:
		#		text += str(x) + ' blocks'
		#		ltexts.append(text)
		#		text = None
		#	iterator +=1
		#d["ldeads"] = ltexts
		#d["lattributes"] = writeErrorAttribute(d["attribute"])
		#d["numIncorrects"] = len(d["lattributes"])
		#lx = d["mastery"].items()
		return render_to_response("dashboard-unregistered.html", d)
	elif request.method == 'GET':
		return HttpResponse('Error: GET 404 Not Found')
	else:
		return HttpResponse('Error: File is not charged correctly')

def procDuplicateScript(lines):
	"""Return number of duplicate scripts"""
        numDuplicate = 0
	listLines = lines.split('\n')
	if len(listLines) > 2:
		numDuplicate = listLines[1][0]
	return numDuplicate	#ready

def procSpriteNaming(lines):
	"""Return the number of default spring"""
	listLines = lines.split('\n')
	numSN = [listLines[1][0]]
	lObjects = listLines[2:]	#tajada
	lfinal = lObjects[:-1] # + numSN
	return lfinal

def procBroadcastReceive(lines):
	"""Return the number of lost messages"""
	listLines = lines.split('\n')
	# messages never received
	laux = listLines[1]
	return laux

def procDeadCode(lines):
	"""Number of dead code with characters and blocks"""
	lLines = lines.split('\n')
	laux = lLines[1:]
	lobjs = []
	lcharacter = []
	literator = []
	iterator = 0
	for x in laux:
		if '[kurt.Script' in x:
			# Found an object			
			lcharacter.append(x)
			if iterator != 0:
				literator.append(iterator)
				iterator = 0
		if 'kurt.Block' in x:
			iterator += 1
	# last iterator
	literator.append(iterator)
	# process the characters
	for c in lcharacter:
		naux = c.split(':')[0]
		if '{' in naux:
			naux = naux.split('{')[1]
		lobjs.append(naux)
	lfinal = mergeList(lobjs, literator)
	return lfinal

def mergeList(list1, list2):
	"""Do merge between 2 lists"""
	# Duncan solution
	lfinal = [None]*(len(list1) + len(list2))
	lfinal[::2] = list1
	lfinal[1::2] = list2
	return lfinal

def procInitialization(lines):
	"""Initialization"""
	dic = {}
	lLines = lines.split('.sb2')
	d = ast.literal_eval(lLines[1])
	dic["attribute"] = d
	return dic

def procMastery(lines):
	"""Mastery"""
	dic = {}
	lLines = lines.split('\n')
	d = ast.literal_eval(lLines[1])
	laux = lLines[2].split(':')[1]
	points = int(laux.split('/')[0])
	maxi = int(laux.split('/')[1])
	dic["mastery"] = d
	dic["mastery"]["TotalPoints"] = points
	return dic

def analyzeProject(file_name):
	dic = {}
	print file_name
	metricDeadCode = "hairball -p blocks.DeadCode " + file_name
	metricCountLines = "hairball -p blocks.BlockCounts " + file_name
	metricDuplicateScript = "hairball -p duplicate.DuplicateScripts " + file_name
	metricSpriteNaming = "hairball -p convention.SpriteNaming " + file_name
	metricBroadcastReceive = "hairball -p checks.BroadcastReceive " + file_name
	metricAttribute = "hairball -p initialization.AttributeInitialization " + file_name
	metricMastery = "hairball -p mastery.Mastery " + file_name
	resultMastery = os.popen(metricMastery).read()
	resultCountLines = os.popen(metricCountLines).read()
#	resultDeadCode = os.popen(metricDeadCode).read()
#	resultDuplicateScript = os.popen(metricDuplicateScript).read()
#	resultSpriteNaming = os.popen(metricSpriteNaming).read()
#	resultBroadcastReceive = os.popen(metricBroadcastReceive).read()
#	resultInitialization = os.popen(metricAttribute).read()
#	dic["duplicate"] = procDuplicateScript(resultDuplicateScript)
#	dic["sprite"] = procSpriteNaming(resultSpriteNaming)
#	dic["broadcast"] = procBroadcastReceive(resultBroadcastReceive)	
#	dic["dead"] = procDeadCode(resultDeadCode)
#	dic.update(procInitialization(resultInitialization))
	dic.update(procMastery(resultMastery))
	return dic

def mydashboard(request):
	"""Dashboard page"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	# The main page of user
	# To obtain the dashboard associated to user
	mydashboard = Dashboard.objects.get(user=user)
	projects = mydashboard.project_set.all()
	beginner = mydashboard.project_set.filter(level="beginner")
	developing = mydashboard.project_set.filter(level="developing")
	advanced = mydashboard.project_set.filter(level="advanced")
	return render_to_response("content-dashboard.html", {'user': user,
														'beginner': beginner,
														'developing': developing,
														'advanced': advanced,
														'projects': projects},
														context_instance=RequestContext(request))


def uploadZip(request):
	"""Upload and save the zip"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
		
	if request.method == 'POST':
		form = UploadFileForm(request.POST)
		# Analyze the scratch project
		fileName = handle_uploaded_file(request.FILES['zipFile'])
		# Analize project and to save in database the metrics
		d = analyzeProject(fileName)
		fupdate = datetime.now()
		# Get the short name
		shortName = fileName.split('/')[-1]
		# Get the dashboard of user
		myDashboard = Dashboard.objects.get(user=user)	
		# Save the project
		newProject = Project(name=shortName, version=1, score=0, path=fileName, fupdate=fupdate, dashboard=myDashboard)
		newProject.save()
		# Save the metrics	
		dmaster = d["mastery"]
		newMastery = Mastery(myproject=newProject, abstraction=dmaster["Abstraction"], paralel=dmaster["Parallelization"], logic=dmaster["Logic"], synchronization=dmaster["Synchronization"], flowcontrol=dmaster["FlowControl"], interactivity=dmaster["UserInteractivity"], representation=dmaster["DataRepresentation"], TotalPoints=dmaster["TotalPoints"])
		newMastery.save()
		newProject.score = dmaster["TotalPoints"]
                print "Puntos:" 
                print newProject.score
		if newProject.score > 15:
			newProject.level = "advanced"
		elif newProject.score > 7:
			newProject.level = "developing"
		else:
			newProject.level = "beginner"
		newProject.save()
		
		for charx, dmetrics in d["attribute"].items():
			if charx != 'stage':
				newAttribute = Attribute(myproject=newProject, character=charx, orientation=dmetrics["orientation"], position=dmetrics["position"], costume=dmetrics["costume"], visibility=dmetrics["visibility"], size=dmetrics["size"])
			newAttribute.save()

		iterator = 0
		for deadx in d["dead"]:
			if (iterator % 2) == 0:
				newDead = Dead(myproject=newProject, character=deadx, blocks=0)
			else:
				newDead.blocks = deadx
			newDead.save()
			iterator += 1
		
		newDuplicate = Duplicate(myproject=newProject, numduplicates=d["duplicate"][0])
		newDuplicate.save()
		for charx in d["sprite"]:
			newSprite = Sprite(myproject=newProject, character=charx)
			newSprite.save()
			print newSprite.character
		return HttpResponseRedirect('/myprojects')

def createDashboards():
	"""Get users and create dashboards"""
	allUsers = User.objects.all()
	for user in allUsers:
		try:
			newdash = Dashboard.objects.get(user=user)
		except:
			fupdate = datetime.now()
			newDash = Dashboard(user=user.username, frelease=fupdate)
			newDash.save()
	

def myProjects(request):
	"""Show all projects of dashboard"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	mydashboard = Dashboard.objects.get(user=user)
	projects = mydashboard.project_set.all()
	return render_to_response("myprojects.html", {'projects': projects},
													context_instance=RequestContext(request))
	

def buildMastery(item):
	"""Generate the dictionary with mastery"""
	dmastery = {}
	dmastery["Total points"] = item.TotalPoints
	dmastery["Abstraction"] = item.abstraction
	dmastery["Parallelization"] = item.paralel
	dmastery["Logic"] = item.logic
	dmastery["Synchronization"] = item.synchronization
	dmastery["Flow Control"] = item.flowcontrol
	return dmastery

def buildAttribute(qattribute):
	"""Generate dictionary with attribute"""
	# Build the dictionary
	dic = {}
	for item in qattribute:
		dic[item.character] = {"orientation": item.orientation, "position": item.position, "costume": item.costume, "visibility":item.visibility, "size": item.size}
	listInfo = writeErrorAttribute(dic)
	return listInfo

def idProject(request, idProject):
	"""Resource unique of project"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	dmastery = {}
	project = Project.objects.get(id=idProject)
	item = Mastery.objects.get(myproject=project)
	dmastery = buildMastery(item)
	TotalPoints = dmastery["TotalPoints"]
	dsprite = Sprite.objects.filter(myproject=project)
	ddead = Dead.objects.filter(myproject=project)
	dattribute = Attribute.objects.filter(myproject=project)
	listAttribute = buildAttribute(dattribute)
	numduplicate = Duplicate.objects.filter(myproject=project)[0].numduplicates
	return render_to_response("project.html", {'project': project,
												'dmastery': dmastery,
												'lattribute': listAttribute,
												'numduplicate': numduplicate,
												'dsprite': dsprite,
												'Total points': TotalPoints,
												'ddead': ddead},
												context_instance=RequestContext(request))
	

def defineRules(request):
	"""Show the rules in Doctor Scratch"""
	if request.user.is_authenticated():
		user = request.user.username
	else:
		user = None
	return render_to_response("rules.html")	
	





