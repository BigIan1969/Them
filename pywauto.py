#badly needs refactoring
from pywinauto import Desktop
import time
import win32gui
import hashlib
import os
import theminit
import themcontrols
import themcontroltypes

def pywinhtmlw(src, root):
    retval = ''
    for i in src:
        vars = {}
        try:
            vars["parent"] = i.parent().element_info.name
        except:
            vars["parent"] = 'Not Available'
        try:
            vars["auto_id"] = i.automation_id()
        except:
            vars["auto_id"] = 'Not Available'
            # Unable to access this control
        try:
            vars["title"] = i.element_info.name
        except:
            vars["title"] = 'Not Available'
        try:
            vars["windowtext"] = i.window_text()  # no search
        except:
            vars["windowtext"] = 'Not Available'
        try:
            vars["class_name"] = i.class_name()
        except:
            vars["class_name"] = 'Not Available'
        try:
            vars["control_type"] = i.element_info.control_type
        except:
            vars["control_type"] = 'Not Available'
        try:
            vars["control_id"] = i.control_id()
        except:
            vars["control_id"] = 'Not Available'
        try:
            vars["handle"] = i.element_info.handle
        except:
            vars["handle"] = 'Not Available'
        try:
            vars["processid"] = i.element_info.process_id  # no search
        except:
            vars["processid"] = 'Not Available'
        try:
            vars["framework_id"] = i.element_info.framework_id
        except:
            vars["framework_id"] = 'Not Available'
        try:
            vars["backend"] = i.backend.name
        except:
            vars["backend"] = 'Not Available'
        try:
            vars["rectangle"] = i.rectangle()  # no search
        except:
            vars["rectangle"] = 'Not Available'
        try:
            vars["visible"] = i.element_info.visible  # no search
        except:
            vars["visible"] = 'Not Available'
        try:
            vars["children"] = i.control_count()  # no search
        except:
            vars["children"] = 'Not Available'
        idvar = u"""Auto:{0}
        Parent:{1}
        Title:{2}
        Type:{3}
        Class{4}
        """.format(vars["auto_id"],
                   vars["parent"],
                   vars["title"],
                   vars["control_type"],
                   vars["class_name"])
        idhash = hashlib.sha1(idvar.encode("utf-8")).hexdigest().encode()[0 : int(themcontrols.ctrls.settings['hashsize'])]
        # idhash.digest_size=8

        themcontrols.ctrls.add(cid=idhash.decode(), obj=i, searchcrit=vars)
        # theminit.controls[idhash.decode()]=i
        retval += '  <section class="controlselector {0}">\n'.format(vars["backend"])

        if (vars["windowtext"] != ""):
            displaytext = vars["windowtext"]
        else:
            displaytext = "Class=" + vars["class_name"]
        retval += '  <li><span id="{1}" class="selectable caret">{0}</span>\n'.format(displaytext.replace('<', '&lt;'),
                                                                                      idhash.decode()).encode('ascii',
                       'xmlcharrefreplace').decode()

        if root or themcontrols.ctrls.settings['autoexpand']=='Yes':
            addclass = 'active'
        else:
            addclass = ''

        retval += '    <ul class="nested {0}">\n'.format(addclass)

        #top level buttons
        #retval += '    <br><a href="/">Root</a> - <a href="/{1}/">This Control</a>\n'.format(theminit.urlinfo.netloc , idhash.decode())

        retval += '       <li><span class="caret properties">Properties</span>\n'
        retval += '         <ul class="nested">\n'
        retval += '''<table>
                 <tr>
                    <th>Property</th>
                    <th>Value</th>
                 </tr>\n '''
        for d in vars.keys():
            l = vars[d]
            retval += '            <tr>\n'
            retval += '              <td>{0}</td>\n'.format(str(d).replace('<', '&lt;')).encode('ascii',
                                                                                                'xmlcharrefreplace').decode()
            retval += '              <td>{0}</td>\n'.format(str(l).replace('<', '&lt;')).encode('ascii',
                                                                                                'xmlcharrefreplace').decode()
            retval += '            </tr>\n'
            # retval+='           <li>{0}:{1}</li>\n'.format(d,l))
        retval += '         </table>\n'
        retval += '         </ul>\n'
        retval += '       </li>\n'

        # Picture
        retval += '       <li><span  class="caret pic">Picture</span>\n'
        retval += '         <ul class="nested">\n'
        retval += '            <div id=PIC{0} controlid="{0}"></div>\n'.format(idhash.decode('utf-8'))
        retval += '         </ul>\n'
        retval += '      </li>\n'

        if i.control_count() != 0:
            if themcontrols.ctrls.settings['autoexpand']=='No':
                retval += '       <li><span  class="caret children">Children</span>\n'
                retval += '         <ul class="nested">\n'
            else:
                retval += '       <li><span  class="caret caret-down children">Children</span>\n'
                retval += '         <ul class="nested active">\n'

            # retval+=pywinhtmlw(i.children())
            if themcontrols.ctrls.settings["loadmode"]=='Lazy':
                retval += '            <div id={0}></div>'.format("PH" + idhash.decode('utf-8'))
            else:
                retval += '            <div id={0}>{1}</div>'.format("PH" + idhash.decode('utf-8'),pywinhtmlw(i.children(),False))
            #            for d in dir(i):
            #              retval+="<p>",d,"</p>")

            retval += '         </ul>\n'
            retval += '      </li>\n'

        retval += '      <form id="controlform{0}" controlid="{0}" onsubmit="return">\n'.format(idhash.decode())
        t = themcontroltypes.controltypes[vars['control_type']]
        if t is None:
            t = [True, True, True]
        if t[0]:  ### CLICK ###
            retval += '<input type="text" id="XPOS{0}" class="controlform controlxpos" title="Enter Xpos within control to click." aria-label="Xpos"><br>'.format(
                idhash.decode('utf-8'))
            retval += '<input type="text" id="YPOS{0}" class="controlform controlypos" title="Enter Ypos within control to click."><br>'.format(
                idhash.decode('utf-8'))
            retval += '          <button type="button" controlid="{0}" id="BUT{0}" class="controlform controlbutton" onclick="return" title="Click on this control.">Click</button>\n'.format(
                idhash.decode('utf-8'))
        if t[1]:  ### INPUT ###
            retval += '<input type="text" id="INP{0}" class="controlform controlinput" title="Enter text to send to this control.\n+=Shift ^=CTRL %=Alt"><br>'.format(
                idhash.decode('utf-8'))
            retval += '<input type="text" id ="SEL{0}" list="themkeys" class="selectinput" title="Send one of these special keys to the control." />'.format(
                idhash.decode('utf-8'))

        retval += '      </form>\n'

        retval += '    </ul>\n'

        retval += '  </li>\n'
        retval += '  </section>\n'

    return (retval)


class HideandResume:


    def hideall(self, controlid):
        PID = themcontrols.ctrls.get(id=controlid).top_level_parent().element_info.process_id
        w = Desktop(backend=themcontrols.ctrls.settings['tech']).windows()
        theminit.targetlist=[]
        currentfocus=object
        theminit.foregroundwindow=win32gui.GetForegroundWindow()
        for i in w:
            if i.element_info.process_id != PID:
               if i.element_info.handle!=win32gui.GetForegroundWindow():
                    theminit.targetlist.append([i.element_info.handle])
                    win32gui.ShowWindow(i.element_info.handle,0)
               else:
                    currentfocus=i
                    win32gui.ShowWindow(i.element_info.handle,0)
        theminit.targetlist.append([currentfocus.element_info.handle])
        time.sleep(0.4)
    def resume(self):
        time.sleep(0.4)
        for i in theminit.targetlist:
            win32gui.ShowWindow(i[0],5) #restore window to former state
        #win32gui.SetForegroundWindow(theminit.foregroundwindow)
