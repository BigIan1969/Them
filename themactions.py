from subprocess import Popen
from pywinauto import Desktop
from pywauto import HideandResume
import sys
import io
import contextlib
import theminit
import themcontrols


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

class Actions:

    def action(self, id,p1,p2,p3,p4,p5):
        hr =HideandResume()
        if p1[0]=='System' and p2[0]=="Launch Application":
          exepath = p4[0]+p3[0]
          params=[exepath,p5[0]]
          Popen(params, shell=True)
          return('')
        elif p1[0]=='System' and p2[0]=="Exec":
          if p3[0]=='':
              return(str(dir(themcontrols.ctrls.get(id[0]))))
          elif p3[0][0]==".":
            with stdoutIO() as s:
                exec("themcontrols.ctrls.get([id[0])"+p3[0],globals(),locals())
          else:
            with stdoutIO() as s:
                exec(p3[0],globals(),locals())
          return(s.getvalue())
        elif p1[0]=='Input' and p2[0]=='Click':
          hr.hideall(id[0])
          themcontrols.ctrls.get(id[0]).draw_outline()
          if p3[0]=="" or p4[0]=="":
            themcontrols.ctrls.get(id[0]).click_input()
          else:
            themcontrols.ctrls.get(id[0]).click_input(coords=(int(float(p3[0])),int(float(p4[0]))))
          hr.resume()
          return('')
        elif p1[0]=='Input' and p2[0]=='Send Keys':
          themcontrols.ctrls.get(id[0]).draw_outline()
          themcontrols.ctrls.get(id[0]).type_keys(p3[0],with_spaces=True)
          return('')
        elif p1[0]=='Settings' and p2[0]=='Coordinates':
          themcontrols.ctrls.settings['forcecoords']=str(p3[0])
          return(theminit.themhtml.defaultsettings())
        elif p1[0] == 'Settings' and p2[0] == 'Hash Size':
          themcontrols.ctrls.settings['hashsize'] = str(p3[0])
          return (theminit.themhtml.defaultsettings())
        elif p1[0] == 'Settings' and p2[0] == 'Load Mode':
          themcontrols.ctrls.settings['loadmode'] = str(p3[0])
          return (theminit.themhtml.defaultsettings())
        elif p1[0] == 'Settings' and p2[0] == 'Auto Expand Children':
          themcontrols.ctrls.settings['autoexpand'] = str(p3[0])
          return (theminit.themhtml.defaultsettings())
        elif p1[0] == 'Settings' and p2[0] == 'Technology':
          themcontrols.ctrls.settings['tech'] = str(p3[0])
          theminit.pywa = Desktop(backend=themcontrols.ctrls.settings["tech"])
          return (theminit.themhtml.defaultsettings())
        elif p1[0] == 'System' and p2[0] == 'Record':
          theminit.recorder.start()
          return 'Recording in progress'
        elif p1[0] == 'System' and p2[0] == 'Stop':
          theminit.recorder.stop()
          return 'Recording stopped'
        else:
          return("ERROR")
