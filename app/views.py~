#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.core.cache import cache  
from django.shortcuts import render_to_response
from django.template import RequestContext as RC
from django.contrib.auth import logout, login, authenticate
from app.models import Project, Dashboard, Attribute
from app.models import Dead, Sprite, Mastery, Duplicate, File
from app.forms import UploadFileForm, UserForm
from django.contrib.auth.models import User
from datetime import datetime, date
import requests
import os
import ast
import json
import sys

#_______________________ MAIN _______________________________#

def main(request):
    """Main page"""
    if request.user.is_authenticated():
        user = request.user.username    
    else:
        user = None
    # The first time one user enters
    # Create the dashboards associated to users
    createDashboards()
    return render_to_response("main/main.html",
                                {'user':user},
                                context_instance=RC(request))

def redirectMain(request):
    """Page not found redirect to main"""
    return HttpResponseRedirect('/')

#________________________ REGISTRY __________________________#

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
                    return HttpResponseRedirect('/myDashboard')
            else:
                flag = True
                return render_to_response("main/main.html", 
                                            {'flag': flag},
                                            context_instance=RC(request))

    else:
        return HttpResponseRedirect("/")


def logoutUser(request):
    """Method for logging out"""
    logout(request)
    return HttpResponseRedirect('/')

#________________________ DASHBOARD ____________________________# 

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
       
def myDashboard(request):
    """Dashboard page"""
    if request.user.is_authenticated():
        user = request.user.username
        # The main page of user
        # To obtain the dashboard associated to user
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        beginner = mydashboard.project_set.filter(level="beginner")
        developing = mydashboard.project_set.filter(level="developing")
        advanced = mydashboard.project_set.filter(level="advanced")
        return render_to_response("myDashboard/content-dashboard.html", 
                                    {'user': user,
                                    'beginner': beginner,
                                    'developing': developing,
                                    'advanced': advanced,
                                    'projects': projects},
                                    context_instance=RC(request))
    else:
        user = None
        return HttpResponseRedirect("/")

def myProjects(request):
    """Show all projects of dashboard"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myProjects/content-projects.html", 
                                {'projects': projects},
                                context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")
    

def myRoles(request):
    """Show the roles in Doctor Scratch"""
    if request.user.is_authenticated():
        user = request.user.username
        return render_to_response("myRoles/content-roles.html",
                                context_instance=RC(request))   
    else:
        return HttpResponseRedirect("/") 
     


def myHistoric(request):
    """Show the progress in the application"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myHistoric/content-historic.html", 
                                    {'projects': projects},
                                    context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


#__________________________ FILES _______________________________________#

def progressBar(request):
    if request.method == 'POST':
        return render_to_response("prueba.html")
    else:
        return HttpResponseRedirect('/')

def upload_progress(request):
        """
        A view to report back on upload progress.
        Return JSON object with information about the progress of an upload.
        """
        print "LA PETICIÓN ES: \n" + str(request) + "\n"
        #import ipdb
        #ipdb.set_trace()
        progress_id = ''
        if 'X-Progress-ID' in request.GET:
            progress_id = request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in request.META:
            progress_id = request.META['X-Progress-ID']
        if progress_id:
            cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
            data = cache.get(cache_key)
            return HttpResponse(simplejson.dumps(data))
        else:
            return HttpResponseServerError(
                'Server Error: You must provide X-Progress-ID header or query param.')

#TO UNREGISTERED USER
def uploadUnregistered(request):
    """Upload file from form POST"""
    if request.method == 'POST':
        # Create BS of files
        file = request.FILES['zipFile']
        fileName = File (filename = file.name.encode('utf-8'))
        fileName.save()
        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
        fileSaved = dir_zips + str(fileName.id) + ".sb2"
        print "FICHERO GUARDADO EN: " + fileSaved
        pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        logFile = open (pathLog + "logFile.txt", "a")
        logFile.write("FileName: " + str(fileName.filename) + "\t" + "ID: " + \
        str(fileName.id) + "\n")
        # Save file in server
        counter = 0
        file_name = handle_uploaded_file(file, fileSaved, counter)
        # Analyze the scratch project
        d = analyzeProject(file_name)
        # Redirect to dashboard for unregistered user
        return render_to_response("upload/dashboard-unregistered.html", d)
    else:
        return HttpResponseRedirect('/')



def handle_uploaded_file(file, fileSaved, counter):
    # If file exists,it will save it with new name: name(x)
    if os.path.exists(fileSaved):
        counter = counter + 1
        if counter == 1:
            fileSaved = fileSaved.split(".")[0] + "(1).sb2"
        else:
            fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").sb2"
        

        fileName = handle_uploaded_file(file, fileSaved, counter)
        return fileName
    else:
        with open(fileSaved, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return fileSaved

#_______________________ AUTOMATIC ANALYSIS _________________________________#

def analyzeProject(file_name):
    dictionary = {}
    if os.path.exists(file_name):
        #Request to hairball
        metricMastery = "hairball -p mastery.Mastery " + file_name
        metricDuplicateScript = "hairball -p \
                                duplicate.DuplicateScripts " + file_name
        metricSpriteNaming = "hairball -p convention.SpriteNaming " + file_name
        metricDeadCode = "hairball -p blocks.DeadCode " + file_name 
        metricInitialization = "hairball -p \
                           initialization.AttributeInitialization " + file_name
        
        #Plug-ins not used yet
        #metricBroadcastReceive = "hairball -p 
        #                          checks.BroadcastReceive " + file_name
        #metricBlockCounts = "hairball -p blocks.BlockCounts " + file_name

        #Response from hairball     
        resultMastery = os.popen(metricMastery).read()
        resultDuplicateScript = os.popen(metricDuplicateScript).read()
        resultSpriteNaming = os.popen(metricSpriteNaming).read()
        resultDeadCode = os.popen(metricDeadCode).read()
        resultInitialization = os.popen(metricInitialization).read()
        #Plug-ins not used yet
        #resultBlockCounts = os.popen(metricBlockCounts).read()
        #resultBroadcastReceive = os.popen(metricBroadcastReceive).read()

        #Create a dictionary with necessary information
        dictionary.update(procMastery(resultMastery))
        dictionary.update(procDuplicateScript(resultDuplicateScript))
        dictionary.update(procSpriteNaming(resultSpriteNaming))
        dictionary.update(procDeadCode(resultDeadCode))
        dictionary.update(procInitialization(resultInitialization))
        #Plug-ins not used yet
        #dictionary.update(procBroadcastReceive(resultBroadcastReceive))
        #dictionary.update(procBlockCounts(resultBlockCounts))
        return dictionary
    else:
        return HttpResponseRedirect('/')


# __________________________ PROCESSORS _____________________________#

def procMastery(lines):
    """Mastery"""
    dic = {}
    lLines = lines.split('\n')
    d = ast.literal_eval(lLines[1])
    lLines = lLines[2].split(':')[1]
    points = int(lLines.split('/')[0])
    maxi = int(lLines.split('/')[1])
    dic["mastery"] = d
    dic["mastery"]["points"] = points
    dic["mastery"]["maxi"] = maxi
    return dic

def procDuplicateScript(lines):
    """Return number of duplicate scripts"""
    dic = {}
    number = 0
    lLines = lines.split('\n')
    if len(lLines) > 2:
        number = lLines[1][0]
    dic["duplicateScript"] = dic
    dic["duplicateScript"]["number"] = number
    return dic


def procSpriteNaming(lines):
    """Return the number of default spring"""
    dic = {}
    lLines = lines.split('\n')
    number = lLines[1].split(' ')[0]
    lObjects = lLines[2:]
    lfinal = lObjects[:-1]
    dic['spriteNaming'] = dic
    dic['spriteNaming']['number'] = str(number)
    dic['spriteNaming']['sprite'] = lfinal
    return dic


def procDeadCode(lines):
    """Number of dead code with characters and blocks"""
    lLines = lines.split('\n')
    lLines = lLines[1:]
    lcharacter = []
    literator = []
    iterator = 0
    for frame in lLines:
        if '[kurt.Script' in frame:
            # Found an object
            name = frame.split("'")[1]         
            lcharacter.append(name)
            if iterator != 0:
                literator.append(iterator)
                iterator = 0
        if 'kurt.Block' in frame:
            iterator += 1
    literator.append(iterator)

    number = len(lcharacter)
    dic = {}
    dic["deadCode"] = dic  
    dic["deadCode"]["number"] = number
    for i in range(number):
        dic["deadCode"][lcharacter[i]] = literator[i]
  
    return dic


def procInitialization(lines):
    """Initialization"""
    dic = {}
    lLines = lines.split('.sb2')
    d = ast.literal_eval(lLines[1])
    keys = d.keys()
    values = d.values()
    items = d.items()
    number = 0
    
    for keys, values in items:
        list = []
        attribute = ""
        internalkeys = values.keys()
        internalvalues = values.values()
        internalitems = values.items()
        flag = False
        counterFlag = False
        i = 0
        for internalkeys, internalvalues in internalitems:
            if internalvalues == 1:
                counterFlag = True
                for value in list:
                    if internalvalues == value:
                        flag = True
                if not flag:
                    list.append(internalkeys)
                    if len(list) < 2:
                        attribute = str(internalkeys)
                    else:
                        attribute = attribute + ", " + str(internalkeys)
        if counterFlag:
            number = number + 1
        d[keys] = attribute
        
    dic["initialization"] = d
    dic["initialization"]["number"] = number

    return dic

# ___________________ PROCESSORS OF PLUG-INS NOT USED YET ___________________#

#def procBlockCounts(lines):
#    """CountLines"""
#    dic = {}
#    dic["countLines"] = lines

#    print "BLOCK COUNTS: " + str(dic)
#    return dic


#def procBroadcastReceive(lines):
#    """Return the number of lost messages"""
#    dic = {}
#    lLines = lines.split('\n')
    # messages never received or broadcast
#    laux = lLines[1]
#    laux = laux.split(':')[0]
#    dic["neverRB"] = dic
#    dic["neverRB"]["neverReceive"] = laux
#    laux = lLines[3]
#    laux = laux.split(':')[0]
#    dic["neverRB"]["neverBroadcast"] = laux
    
#    return dic

#___________________________ UNDER DEVELOPMENT _________________________#

#UNDER DEVELOPMENT: Children!!!Carefull
def registration(request):
    """Registration a user in the app"""
    return render_to_response("formulary.html")


#UNDER DEVELOPMENT: Children!!!Carefull
def profileSettings(request):
    """Main page for registered user"""
    return render_to_response("profile.html")

#UNDER DEVELOPMENT:
#TO REGISTERED USER
def uploadRegistered(request):
    """Upload and save the zip"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        return HttpResponseRedirect('/')
        
    if request.method == 'POST':
        form = UploadFileForm(request.POST)
        # Analyze the scratch project and save in our server files
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
        newProject.score = dmaster["Total{% if forloop.counter0|divisibleby:1 %}<tr>{% endif %}Points"]
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

#_____ ID/BUILDERS ____________#

def idProject(request, idProject):
    """Resource uniquemastery of project"""
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
        dic[item.character] = {"orientation": item.orientation, 
                                "position": item.position, 
                                "costume": item.costume, 
                                "visibility":item.visibility, 
                                "size": item.size}
    listInfo = writeErrorAttribute(dic)
    return listInfo

#_______BUILDERS'S HELPERS ________#

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



# _________________________  _______________________________ #

def uncompress_zip(zip_file):
    unziped = ZipFile(zip_file, 'r')
    for file_path in unziped.namelist():
        if file_path == 'project.json':
            file_content = unziped.read(file_path)
    show_file(file_content)

