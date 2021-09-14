from pywinauto import Desktop
import themcontrols
import themhtml
import themactions
from themhook import themhook as rec

#import shelve

themcontrols.ctrls = themcontrols.Controls()

try:
    pywa=Desktop(backend=themcontrols.ctrls.settings["tech"])
except:
    themcontrols.ctrls.settings["tech"]='uia'
    pywa=Desktop(backend=themcontrols.ctrls.settings["tech"])

foregroundwindow = int()
targetlist = []
urlinfo = ""
orgtech = themcontrols.ctrls.settings["tech"]
themhtml = themhtml.Themhtml()
themactions =themactions.Actions()
actions={}
recorder = rec()

actions['System']={}
actions['System']['Launch Application']={}
actions['System']['Launch Application']['Fields']=['Application','Path','Parammeters']
actions['System']['Launch Application']['Class']=['','forminput','forminput']

#actions['System']['Launch Browser']={}
#actions['System']['Launch Browser']['Fields']=['Browser']
#actions['System']['Launch Browser']['Options']=[['Chrome', 'Firefox', 'Edge','Safari']]
#actions['System']['Launch Browser']['Class']=['']

actions['System']['Exec']={}
actions['System']['Exec']['Fields']=['Command']
actions['System']['Exec']['Class']=['forminput']

actions['System']['Record']={}
actions['System']['Record']['Fields']=[]
actions['System']['Record']['Class']=[]

actions['System']['Stop']={}
actions['System']['Stop']['Fields']=[]
actions['System']['Stop']['Class']=[]

actions['Input']={}
actions['Input']['Click']={}
actions['Input']['Click']['Fields']=[]
actions['Input']['Click']['Class']=[]

actions['Input']['Send Keys']={}
actions['Input']['Send Keys']['Fields']=["Text"]
actions['Input']['Send Keys']['Class']=["forminput"]

actions['Settings']={}
actions['Settings']['Coordinates']={}
actions['Settings']['Coordinates']['Fields']=["Force"]
actions['Settings']['Coordinates']['Options']=[["true", "false"]]
actions['Settings']['Coordinates']['Class']=[""]
actions['Settings']['Coordinates']['Default']=[themcontrols.ctrls.settings["forcecoords"]]

actions['Settings']['Hash Size']={}
actions['Settings']['Hash Size']['Fields']=["Size"]
actions['Settings']['Hash Size']['Class']=[""]
actions['Settings']['Hash Size']['Default']=[themcontrols.ctrls.settings["hashsize"]]

actions['Settings']['Load Mode']={}
actions['Settings']['Load Mode']['Fields']=["Mode"]
actions['Settings']['Load Mode']['Options']=[["Lazy", "Full"]]
actions['Settings']['Load Mode']['Class']=[""]
actions['Settings']['Load Mode']['Default']=[themcontrols.ctrls.settings["loadmode"]]

actions['Settings']['Auto Expand Children']={}
actions['Settings']['Auto Expand Children']['Fields']=["Expand"]
actions['Settings']['Auto Expand Children']['Options']=[["Yes", "No"]]
actions['Settings']['Auto Expand Children']['Class']=[""]
actions['Settings']['Auto Expand Children']['Default']=[themcontrols.ctrls.settings["autoexpand"]]

actions['Settings']['Technology']={}
actions['Settings']['Technology']['Fields']=["Technology"]
actions['Settings']['Technology']['Options']=[["uia", "win32"]]
actions['Settings']['Technology']['Class']=[""]
actions['Settings']['Technology']['Default']=[themcontrols.ctrls.settings["tech"]]
