#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.core.cache import cache  
from django.shortcuts import render_to_response
from django.template import RequestContext as RC
from django.template import Context, loader
from django.contrib.auth import logout, login, authenticate
from django.utils.translation import ugettext as _
from app.models import Project, Dashboard, Attribute
from app.models import Dead, Sprite, Mastery, Duplicate, File
from app.models import Teacher, Student, Classroom
from app.forms import UploadFileForm, UserForm, NewUserForm, UrlForm, TeacherForm
from app.forms import OrganizationForm
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from email.MIMEText import MIMEText
import smtplib
import email.utils
import os
import ast
import json
import sys
import urllib2
import shutil
import unicodedata
import csv
import kurt
import zipfile
from zipfile import ZipFile

#Global variables
pMastery = "hairball -p mastery.Mastery "
pDuplicateScript = "hairball -p duplicate.DuplicateScripts " 
pSpriteNaming = "hairball -p convention.SpriteNaming "
pDeadCode = "hairball -p blocks.DeadCode "
pInitialization = "hairball -p initialization.AttributeInitialization "

#_____________________________ MAIN ______________________________________#

def main(request):
    """Main page"""
    if request.user.is_authenticated():
        user = request.user.username    
    else:
        user = None
    # The first time one user enters
    # Create the dashboards associated to users
    createDashboards()
    return render_to_response('main/main.html',
                                {'user':user},
                                RC(request))

#___________________________ REDIRECT ____________________________________#

def redirectMain(request):
    """Page not found redirect to main"""
    return HttpResponseRedirect('/')

#_______________________________ ERROR ___________________________________#

def error404(request):
    response = render_to_response('404.html', {},
                                  context_instance = RC(request))
    response.status_code = 404
    return response

def error500(request):
    response = render_to_response('500.html', {},
                                  context_instance = RC(request))
    return response

#_______________________ TO UNREGISTERED USER ___________________________#

def selector(request):
    if request.method == 'POST':
        error = False
        id_error = False
        no_exists = False
        if "_upload" in request.POST:
            d = uploadUnregistered(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))   
            elif d['Error'] == 'MultiValueDict':
                error = True
                return render_to_response('main/main.html',
                            {'error':error},
                            RC(request))
            else:    
                if d["mastery"]["points"] >= 15:
                    return render_to_response("upload/dashboard-unregistered-master.html", d)
                elif d["mastery"]["points"] > 7:
                    return render_to_response("upload/dashboard-unregistered-developing.html", d)
                else:
                    return render_to_response("upload/dashboard-unregistered-basic.html", d)
        elif '_url' in request.POST:
            d = urlUnregistered(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))             
            elif d['Error'] == 'MultiValueDict':
                error = True
                return render_to_response('main/main.html',
                            {'error':error},
                            RC(request))
            elif d['Error'] == 'id_error':
                id_error = True
                return render_to_response('main/main.html',
                            {'id_error':id_error},
                            RC(request))
            elif d['Error'] == 'no_exists':
                no_exists = True
                return render_to_response('main/main.html',
                    {'no_exists':no_exists},
                    RC(request))
            else:
                if d["mastery"]["points"] >= 15:
                    return render_to_response("upload/dashboard-unregistered-master.html", d)
                elif d["mastery"]["points"] > 7:
                    return render_to_response("upload/dashboard-unregistered-developing.html", d)
                else:
                    return render_to_response("upload/dashboard-unregistered-basic.html", d)
    else:
        return HttpResponseRedirect('/')



def handler_upload(fileSaved, counter):
    """ Necessary to uploadUnregistered"""
    # If file exists,it will save it with new name: name(x)
    if os.path.exists(fileSaved): 
        counter = counter + 1
        #Check the version of Scratch 1.4Vs2.0
        version = checkVersion(fileSaved)
        if version == "2.0":
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb2"
            else:
                fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").sb2"
        else:
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb"
            else:
                fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").sb"
        

        file_name = handler_upload(fileSaved, counter)
        return file_name
    else:   
        file_name = fileSaved
        return file_name


def checkVersion(fileName):
    extension = fileName.split('.')[-1]
    if extension == 'sb2':
        version = '2.0'
    else:
        version = '1.4'
    return version


#_______________________Project Analysis Project___________________#

def uploadUnregistered(request):
    """Upload file from form POST for unregistered users"""
    if request.method == 'POST':
        #Revise the form in main
        #If user doesn't complete all the fields,it'll show a warning
        try:
            file = request.FILES['zipFile']
        except:
            d = {'Error': 'MultiValueDict'}
            return  d
        # Create DB of files
        now = datetime.now()
        fileName = File (filename = file.name.encode('utf-8'), 
                        method = "project" , time = now, 
                        score = 0, abstraction = 0, parallelization = 0,
                        logic = 0, synchronization = 0, flowControl = 0,
                        userInteractivity = 0, dataRepresentation = 0,
                        spriteNaming = 0 ,initialization = 0,
                        deadCode = 0, duplicateScript = 0)
        fileName.save()
        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
        fileSaved = dir_zips + str(fileName.id) + ".sb2"

        # Version of Scratch 1.4Vs2.0
        version = checkVersion(fileName.filename)
        if version == "1.4":
            fileSaved = dir_zips + str(fileName.id) + ".sb"
        else:
            fileSaved = dir_zips + str(fileName.id) + ".sb2"

        # Create log
        pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        logFile = open (pathLog + "logFile.txt", "a")
        logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
        str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + "\t\t\t" + \
        "Time: " + str(fileName.time) + "\n")

        # Save file in server
        counter = 0
        file_name = handler_upload(fileSaved, counter)
        
        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        #Create 2.0Scratch's File
        file_name = changeVersion(request, file_name)
    
        # Analyze the scratch project
        try:
            d = analyzeProject(request, file_name, fileName)
        except:
            #There ir an error with kutz or hairball
            #We save the project in folder called error_analyzing
            fileName.method = 'project/error'
            fileName.save()
            oldPathProject = fileSaved
            newPathProject = fileSaved.split("/uploads/")[0] + \
                             "/error_analyzing/" + \
                             fileSaved.split("/uploads/")[1]
            shutil.copy(oldPathProject, newPathProject)
            d = {'Error': 'analyzing'}
            return d
        # Show the dashboard
        # Redirect to dashboard for unregistered user
        d['Error'] = 'None'
        return d
    else:
        return HttpResponseRedirect('/')



def changeVersion(request, file_name):
    p = kurt.Project.load(file_name)
    p.convert("scratch20")
    p.save()
    file_name = file_name.split('.')[0] + '.sb2'
    return file_name   
        


#_______________________URL Analysis Project_________________________________#


def urlUnregistered(request):
    """Process Request of form URL"""        
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():          
            d = {}
            url = form.cleaned_data['urlProject']
            idProject = processStringUrl(url)
            if idProject == "error":
                d = {'Error': 'id_error'}
                return d
            else:
                try:
                    (pathProject, file) = sendRequestgetSB2(idProject)
                except:
                    #When your project doesn't exist
                    d = {'Error': 'no_exists'}
                    return d             
                try:
                    d = analyzeProject(request, pathProject, file)
                except:
                    #There ir an error with kutz or hairball
                    #We save the project in folder called error_analyzing
                    file.method = 'url/error'
                    file.save()
                    oldPathProject = pathProject
                    newPathProject = pathProject.split("/uploads/")[0] + \
                                     "/error_analyzing/" + \
                                     pathProject.split("/uploads/")[1]
                    shutil.copy(oldPathProject, newPathProject)
                    d = {'Error': 'analyzing'}
                    return d

                #Create Json
                djson = createJson(d)

                # Redirect to dashboard for unregistered user
                d['Error'] = 'None'            
                return d
        else:
            d = {'Error': 'MultiValueDict'}
            return  d
    else:
        return HttpResponseRedirect('/')
                     
                
def processStringUrl(url):
    """Process String of URL from Form"""
    idProject = ''
    auxString = url.split("/")[-1]
    if auxString == '':
        # we need to get the other argument    
        possibleId = url.split("/")[-2]
        if possibleId == "#editor":
            idProject = url.split("/")[-3]
        else:
            idProject = possibleId
    else:
        if auxString == "#editor":
            idProject = url.split("/")[-2]
        else:
            # To get the id project
            idProject = auxString
    try:
        checkInt = int(idProject)
    except ValueError:
        idProject = "error"
    return idProject

def sendRequestgetSB2(idProject):
    """First request to getSB2"""
    getRequestSb2 = "http://drscratch.cloudapp.net:8080/" + idProject
    print getRequestSb2
    fileURL = idProject + ".sb2"

    # Create DB of files
    now = datetime.now()
    print now
    fileName = File (filename = fileURL, 
                     method = "url" , time = now, 
                     score = 0, abstraction = 0, parallelization = 0,
                     logic = 0, synchronization = 0, flowControl = 0,
                     userInteractivity = 0, dataRepresentation = 0,
                     spriteNaming = 0 ,initialization = 0,
                     deadCode = 0, duplicateScript = 0)
    fileName.save()
    print "HOLA"
    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    print str(dir_zips)
    fileSaved = dir_zips + str(fileName.id) + ".sb2"
    pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
    print str(pathLog)
    logFile = open (pathLog + "logFile.txt", "a")
    logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
    str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + "\t\t\t" + \
    "Time: " + str(fileName.time) + "\n")

    # Save file in server
    counter = 0
    file_name = handler_upload(fileSaved, counter)
    outputFile = open(file_name, 'wb')
    print str(file_name)
    sb2File = urllib2.urlopen(getRequestSb2)
    print "SI"
    outputFile.write(sb2File.read())
    outputFile.close()
    return (file_name, fileName)



#________________________ CREATE JSON _________________________________#

def createJson(d):
    flagsPlugin = {"Mastery":0, "DeadCode":0, "SpriteNaming":1, "Initialization":0, "DuplicateScripts":0}
    

#________________________ LEARN MORE __________________________________#

def learn(request,page):
    #Unicode to string(page)
    page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')

    dic = {'Pensamiento':'Logic',
           'Paralelismo':'Parallelization',
          'Representacion':'DataRepresentation',
          'Sincronizacion':'Synchronization',
          'Interactividad':'UserInteractivity',
          'Control':'FlowControl',
          'Abstraccion':'Abstraction'}

    if page in dic:
        page = dic[page]

    page = "learn/" + page + ".html"

    if request.user.is_authenticated():
     
        return render_to_response(page,
                                RC(request))
    else:
       
        return render_to_response(page,
                                RC(request))

def learnUnregistered(request):
   	
    return render_to_response("learn/learn-unregistered.html",)

#________________________ COLLABORATORS _____________________________#

def collaborators(request):
   	
    return render_to_response("main/collaborators.html",)


#________________________ TO REGISTER ORGANIZATION __________________#

def signUpOrganization(request):
    if request.method == 'POST':
        print "ENTRA AL POST"
        form = OrganizationForm(request.POST)      
        if form.is_valid(): 
            form.save()
            print "GUARDADO"     
            name = form.cleaned_data['name']
            print name
            #password = form.cleaned_data['password']
            #email = form.cleaned_data['email']
            #hashkey = form.cleaned_data['hashkey']
            return HttpResponseRedirect('/organizations/' + name)

        print "FORM NO VÁLIDO"                
    elif request.method == 'GET':
        return render_to_response("sign/createOrganization.html", context_instance = RC(request))
    
#_________________________ TO SHOW ORGANIZATION'S DASHBOARD ___________#

def organizations(request, name):
    if request.method == 'GET':
        return render_to_response("main/main_organizations.html", context_instance = RC(request))
        
#________________________ TO REGISTER USER __________________________#

def createUser(request):
    """Method for to sign up in the platform"""
    logout(request)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            nickName = form.cleaned_data['nickname']
            emailUser = form.cleaned_data['emailUser']
            passUser = form.cleaned_data['passUser']
            user = User.objects.create_user(nickName, emailUser, passUser)
            return render_to_response("profile.html", {'user': user}, context_instance=RC(request))

def signUpUser(request):
    form = TeacherForm(request.POST or None) 
    if request.method == 'POST': 
        if form.is_valid():       
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            print email
            hashkey = form.cleaned_data['hashkey']
            #classroom = form.cleaned_data['classroom']
            invite(request, username, email, hashkey)
            teacher = Teacher(teacher = request.user, username = username,
                              password = password, email = email,
                              hashkey = hashkey)
            teacher.save()
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
            
    elif request.method == 'GET':
        return render_to_response("sign/createhash.html", context_instance = RC(request))
        


def invite(request, username, email, hashkey):
    emisor = "drscratch.website@gmail.com"
    receptor = "inanna17@gmail.com"
    try:
        mensaje = MIMEText("correo enviado desde Python")
        mensaje['From']=emisor
        mensaje['To']=receptor
        mensaje['Subject']="Asunto del correo"
    except:
        "PROBLEMA MIMEtext"
    try: 
        serverSMTP = smtplib.SMTP('smtp.gmail.com',587)
        serverSMTP.ehlo()
        serverSMTP.starttls()
        serverSMTP.ehlo()
        serverSMTP.login(emisor,"GA.drscratch")
    except:
        print "LA LIBRERIA smtplib"
    try:
        serverSMTP.sendmail(emisor,receptor,mensaje.as_string())
 
        serverSMTP.close() 
        print "Correo enviado" 
    except: 
        print """Error: el mensaje no pudo enviarse. 
        Compruebe que sendmail se encuentra instalado en su sistema"""
 

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


#_______________________ AUTOMATIC ANALYSIS _________________________________#

def analyzeProject(request,file_name, fileName):
    dictionary = {}
    if os.path.exists(file_name):
        list_file = file_name.split('(')
        if len(list_file) > 1:
            file_name = list_file[0] + '\(' + list_file[1]
            list_file = file_name.split(')')
            file_name = list_file[0] + '\)' + list_file[1]
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
        dictionary.update(procMastery(request,resultMastery, fileName))
        dictionary.update(procDuplicateScript(resultDuplicateScript, fileName))
        dictionary.update(procSpriteNaming(resultSpriteNaming, fileName))
        dictionary.update(procDeadCode(resultDeadCode, fileName))
        dictionary.update(procInitialization(resultInitialization, fileName))
        #Plug-ins not used yet
        #dictionary.update(procBroadcastReceive(resultBroadcastReceive))
        #dictionary.update(procBlockCounts(resultBlockCounts))
        
        return dictionary
    else:
        return HttpResponseRedirect('/')

# __________________________ TRANSLATE MASTERY ______________________#

def translate(request,d, fileName):
    if request.LANGUAGE_CODE == "es":
        d_translate_es = {}
        d_translate_es['Abstracción'] = d['Abstraction']
        d_translate_es['Paralelismo'] = d['Parallelization']
        d_translate_es['Pensamiento lógico'] = d['Logic']
        d_translate_es['Sincronización'] = d['Synchronization']
        d_translate_es['Control de flujo'] = d['FlowControl']
        d_translate_es['Interactividad con el usuario'] = d['UserInteractivity']
        d_translate_es['Representación de la información'] = d['DataRepresentation']
        fileName.language = "es"
        fileName.save()
        return d_translate_es
    else:
        return d


# __________________________ PROCESSORS _____________________________#

def procMastery(request,lines, fileName):
    """Mastery"""
    dic = {}
    lLines = lines.split('\n')
    d = {}
    d = ast.literal_eval(lLines[1])
    lLines = lLines[2].split(':')[1]
    points = int(lLines.split('/')[0])
    maxi = int(lLines.split('/')[1])
    
    #Save in DB 
    fileName.score = points
    fileName.abstraction = d["Abstraction"]
    fileName.parallelization = d["Parallelization"]
    fileName.logic = d["Logic"]
    fileName.synchronization = d["Synchronization"]
    fileName.flowControl = d["FlowControl"]
    fileName.userInteractivity = d["UserInteractivity"]
    fileName.dataRepresentation = d["DataRepresentation"]
    fileName.save()

    #Translation
    d_translated = translate(request,d, fileName)

    dic["mastery"] = d_translated
    dic["mastery"]["points"] = points
    dic["mastery"]["maxi"] = maxi   
    return dic

def procDuplicateScript(lines, fileName):
    """Return number of duplicate scripts"""
    dic = {}
    number = 0
    lLines = lines.split('\n')
    if len(lLines) > 2:
        number = lLines[1][0]
    dic["duplicateScript"] = dic
    dic["duplicateScript"]["number"] = number

    #Save in DB 
    fileName.duplicateScript = number
    fileName.save()


    return dic


def procSpriteNaming(lines, fileName):
    """Return the number of default spring"""
    dic = {}
    lLines = lines.split('\n')
    number = lLines[1].split(' ')[0]
    lObjects = lLines[2:]
    lfinal = lObjects[:-1]
    dic['spriteNaming'] = dic
    dic['spriteNaming']['number'] = str(number)
    dic['spriteNaming']['sprite'] = lfinal

    #Save in DB 
    fileName.spriteNaming = str(number)
    fileName.save()

    return dic


def procDeadCode(lines, fileName):
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

    #Save in DB 
    fileName.deadCode = number
    fileName.save()
  
    return dic


def procInitialization(lines, fileName):
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

    #Save in DB 
    fileName.initialization = number
    fileName.save()

    return dic



#_________________________CSV File____________________________#
def exportCsvFile(request):
	"""Export a CSV File"""
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="some.csv"'
	d = {"Abstraction": 2, "level": " Developing", "Parallelization": 1, "Logic": 1, "Synchronization": 2, "FlowControl": 2, "UserInteractivity": 1, "maxPoints": 21, "DataRepresentation": 1, "points": 10}
	writer = csv.writer(response)
	for key, value in d.items():
   		writer.writerow([key, value])

	"""
	writer = csv.writer(response)
	writer.writerow(['First row', 'Paco', '21', 'Madrid'])
	writer.writerow(['Second row', 'Lucia', '25', 'Quito'])
	"""
	return response






##############################################################################
#                           UNDER DEVELOPMENT                                   
##############################################################################

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
                                {'projects': projects,
                                 'user':user},
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


#________________________ PROFILE ____________________________# 


def updateProfile(request):
    """Update the pass, email and avatar"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            newPass = form.cleaned_data['newPass']
            newEmail = form.cleaned_data['newEmail']
            choiceField = forms.ChoiceField(widget=forms.RadioSelect())
            return HttpResponseRedirect('/mydashboard')
        else:
            return HttpResponseRedirect('/')


def changePassword(request, new_password):
    """Change the password of user"""
    user = User.objects.get(username=current_user)
    user.set_password(new_password)
    user.save()

# ___________________ PROCESSORS OF PLUG-INS NOT USED YET ___________________#

#def procBlockCounts(lines):
#    """CountLines"""
#    dic = {}
#    dic["countLines"] = lines
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


#_____________________ CREATE STATS OF ANALYSIS PERFORMED ___________#

def createStats(file_name, dictionary):
    flag = True
    return flag




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
        d = analyzeProject(request,fileName)
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

