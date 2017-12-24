from hairball.myhairball import Hairball


class DrScratchPlugin():

    SERVER_GETSB2 = "http://drscratch.cloudapp.net:8080/"

    def __init__(self, plugins, files):
        self.hairball = self._create_hairball(plugins, files)

    def _create_hairball(self, plugins, files):
        hairball = Hairball(self.plugins, self.scratches)
        hairball.initialize_plugins()
        return hairball
        #self.hairball.process()
        #self.hairball.finalize()

    def _get_scratchs(self):
        scratchs = []
        for filename in self.files:
            scratchs.append(self._get_sb2(filename))
        return scratchs

    def call(self):
        d = analyzeProject(scratch_project, file)
        return "holi"

    def _get_sb2(project_id):
        url_getsb2 = SERVER_GETSB2 + project_id
        return urllib2.urlopen(url_getsb2)

    def _analyze(request, file_sb2, ):
        dictionary = {}
        metricMastery = "hairball -p mastery.Mastery " + file_name
        resultMastery = os.popen(metricMastery).read()
        dictionary.update(procMastery(request,resultMastery, fileName))
        return dictionary