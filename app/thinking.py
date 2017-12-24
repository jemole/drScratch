

class Analysis():
    def __init__(self, plugins):
        self.plugins =  plugins

    def start(self, plugins):
        plugins = []
        for plugin in plugins:
            plugins.append(get_plugin_name(plugin))


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

        resultMastery = os.popen(metricMastery).read()
        resultDuplicateScript = os.popen(metricDuplicateScript).read()
        resultSpriteNaming = os.popen(metricSpriteNaming).read()
        resultDeadCode = os.popen(metricDeadCode).read()
        resultInitialization = os.popen(metricInitialization).read()

        dictionary.update(procMastery(request,resultMastery, fileName))
        dictionary.update(procDuplicateScript(resultDuplicateScript, fileName))
        dictionary.update(procSpriteNaming(resultSpriteNaming, fileName))
        dictionary.update(procDeadCode(resultDeadCode, fileName))
        dictionary.update(procInitialization(resultInitialization, fileName))
        code = {'dupCode':DuplicateScriptToScratchBlock(resultDuplicateScript)}
        dictionary.update(code)
        code = {'dCode':DeadCodeToScratchBlock(resultDeadCode)}
        dictionary.update(code)
        return dictionary
    else:
        return HttpResponseRedirect('/')

def get_plugin_name(description):
    plugins = []
    if description == "mastery":
        plugins.append("mastery.Mastery")
    if description == "duplicate":
        plugins.append("duplicate.DuplicateScripts")
    if description == "sprite":
        plugins.append("convention.SpriteNaming")
    if description == "deadcode":
        plugins.append("blocks.DeadCode")
    if description == "init":
        plugins.append("initialization.AttributeInitialization")

    return plugins