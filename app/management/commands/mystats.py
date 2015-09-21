from django.core.management.base import BaseCommand
from app.models import Stats,File
from app.views import date_range
from datetime import datetime,timedelta,date
from django.db.models import Avg

class Command(BaseCommand):
    def handle(self,*args,**options):
        """ Initializing variables """
        daily_rate = []
        daily_projects=[]
        point_list=[]
        start = date(2015,8,1)
        end = datetime.today()
        y = end.year
        m = end.month
        d = end.day
        end = date(y,m,d)
        dateList = date_range(start, end)

        """ Recolect data for daily_rate & daily_projects """

        for n in dateList:
            #mydates.append(n.strftime("%d/%m")) #used for x axis in stats
            files = File.objects.filter(time=n)
            daily_rate.append(files.aggregate(Avg("score"))["score__avg"])
            for k in daily_rate:
                if k == None:
                    daily_rate[daily_rate.index(k)]= 0

            for i in files:
                #mastery_list.append(i.score)
                point_list.append(i.score)
            daily_projects.append(len(files))
        """ Stats by CT level """

        master = 0
        development = 0
        basic = 0

        totalProjects = File.objects.count()
        for i in point_list:
            if i >= 15:
                master = master + 1
            elif i > 7:
                development = development + 1
            else:
                basic = basic + 1
        basic = basic*100/totalProjects
        development=development*100/totalProjects
        master=master*100/totalProjects
        """This section calculates the average score by programming skill """

        parallelism = File.objects.all().aggregate(Avg("parallelization"))
        parallelism = int(parallelism["parallelization__avg"])
        abstraction = File.objects.all().aggregate(Avg("abstraction"))
        abstraction = int(abstraction["abstraction__avg"])
        logic = File.objects.all().aggregate(Avg("logic"))
        logic = int(logic["logic__avg"])
        synchronization = File.objects.all().aggregate(Avg("synchronization"))
        synchronization = int(synchronization["synchronization__avg"])
        flowControl = File.objects.all().aggregate(Avg("flowControl"))
        flowControl = int(flowControl["flowControl__avg"])
        userInteractivity = File.objects.all().aggregate(Avg("userInteractivity"))
        userInteractivity = int(userInteractivity["userInteractivity__avg"])
        dataRepresentation = File.objects.all().aggregate(Avg("dataRepresentation"))
        dataRepresentation = int(dataRepresentation["dataRepresentation__avg"])

        """This section calculates the average score by code smell"""
        deadCode = File.objects.all().aggregate(Avg("deadCode"))
        deadCode = int(deadCode["deadCode__avg"])
        duplicateScript = File.objects.all().aggregate(Avg("duplicateScript"))
        duplicateScript = int(duplicateScript["duplicateScript__avg"])
        spriteNaming = File.objects.all().aggregate(Avg("spriteNaming"))
        spriteNaming = int(spriteNaming["spriteNaming__avg"])
        initialization = File.objects.all().aggregate(Avg("initialization"))
        initialization = int(initialization["initialization__avg"])

        """This section calculates the average score by code smell"""

        self.stdout.write("Doing all the stats!")

        stats_today = Stats(daily_score=daily_rate,
                            basic= basic,
                            development = development,
                            master = master,
                            daily_projects=daily_projects,
                            parallelism=parallelism,
                            abstraction = abstraction,
                            logic = logic,
                            synchronization = synchronization,
                            flowControl = flowControl,
                            userInteractivity = userInteractivity,
                            dataRepresentation = dataRepresentation,
                            deadCode = deadCode,
                            duplicateScript = duplicateScript,
                            spriteNaming = spriteNaming,
                            initialization = initialization
                            )

        stats_today.save()
