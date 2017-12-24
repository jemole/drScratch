import urllib2
from urllib import urlopen
import zipfile
from StringIO import StringIO
from hairball.myhairball import Hairball

SERVER_GETSB2 = "http://drscratch.cloudapp.net:8080/"

def get_sb2(project_id):
    url_getsb2 = SERVER_GETSB2 + project_id
    sb2_file = urlopen(url_getsb2)
    # sb2_file = urllib2.urlopen(url_getsb2).read()
    zf = zipfile.ZipFile(StringIO(sb2_file.read()))
    return zf

project_id = '194044875'
plugins = ['mastery.Mastery', 'blocks.DeadCode']
scratch_project = get_sb2(project_id)
scratchs = [scratch_project]

hb = Hairball(plugins, scratchs)
hb.initialize_plugins()
hb.process()
hb.finalize()
