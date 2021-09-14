from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import numpy as np
import pytesseract
import dunglib
from pywauto import pywinhtmlw, HideandResume
from pathlib import Path
import theminit
import themcontrols


def loadfile(file):
    with open(file, 'rb') as file:
        return file.read()
        
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        theminit.urlinfo=urlparse(self.path)
        q=parse_qs(theminit.urlinfo.query)

        d=dunglib.dung()
        d.setdicttolist(q, [['p1'], ['p2'], ['p3'], ['p4'], ['p5']], [''])

        if theminit.urlinfo.path=='/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            outstr=''
            with open('head.hi') as f:
                outstr=f.read()

            f.closed

            outstr+=theminit.themhtml.defaultsettings()

            outstr+=pywinhtmlw(theminit.pywa.windows(),False)
            outstr+=theminit.themhtml.keylisthtml()


            with open('footer.hi') as f:
                outstr+=f.read()
            self.wfile.write(bytes(outstr,'utf8'))
        elif theminit.urlinfo.path.endswith('/getchildrenbyid'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            controlid=q['id'][0]
            c=themcontrols.ctrls.get(controlid)
            self.wfile.write(bytes(pywinhtmlw(c.children(),False),'utf8'))
        elif theminit.urlinfo.path.endswith('/getformoutline'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            sys=['System','Input','Info','Waits','Asserts']
            controlid=q['id'][0]
            c=themcontrols.ctrls.get(controlid)
            outstr='<form id="actionform" action="/actionform" controlid="{0}">\n'.format(controlid)
            outstr+='<label for="systemlevel" class="formlabel">System Level:</label>\n'
            outstr+='<select name="systemlevel" id="p1" onchange="eventsystemlevel()" value="">\n'
            outstr+='<option value=""></option>\n'
            for i in theminit.actions.keys():
              outstr+='<option value="{0}">{0}</option>\n'.format(i)
            outstr+='</select>\n'
            outstr+='<div id="formph01"></div>\n'
            outstr+='<div id="formph02"></div>\n'
            outstr+='<div id="formph03"></div>\n'
            outstr+='<div id="formph04"></div>\n'
            outstr+='<div id="formphERROR"></div>\n'
            outstr+='</form>\n'
            self.wfile.write(bytes(outstr,'utf8'))
        elif theminit.urlinfo.path.endswith('/getactions'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if q["p1"][0] in theminit.actions.keys():
                act=['Launch Application','Launch Browser']
                outstr='<label for="Action" class="formlabel">Action:</label>\n'
                outstr+='<select name="Action" id="p2" onchange="eventaction()">\n'
                outstr+='<option value=""></option>\n'
                for i in theminit.actions[q["p1"][0]].keys():
                  outstr+='<option value="{0}">{0}</option>\n'.format(i)
                outstr+='</select>\n'
            else:
                outstr='{0} not yet supported'.format(q["p1"][0])
            self.wfile.write(bytes(outstr,'utf8'))
        elif theminit.urlinfo.path.endswith('/getactionfields'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            outstr=''
            if q["p2"][0] in theminit.actions[q["p1"][0]].keys():
              loc=theminit.actions[q["p1"][0]][q["p2"][0]]
              for idx, field in enumerate(loc['Fields']):
                outstr+='<label for="{0}" class="formlabel">{0}:</label>'.format(field)
                if not 'Options' in loc.keys():
                    if not 'Default' in loc.keys():
                        outstr+='<input type="text" id="p{0}" name="{1}" class="{2}"><br>'.format(idx+3,field,theminit.actions[q["p1"][0]][q["p2"][0]]['Class'][idx])
                    else:
                        outstr+='<input type="text" id="p{0}" name="{1}" class="{2}" value="{3}"><br>'.format(
                            idx+3,
                            field,
                            theminit.actions[q["p1"][0]][q["p2"][0]]['Class'][idx],
                            theminit.actions[q["p1"][0]][q["p2"][0]]['Default'][idx],
                        )
                else:
                    outstr+='<select name="{1}" id="p{0}" class="{2}"">\n'.format(idx+3,field,theminit.actions[q["p1"][0]][q["p2"][0]]['Class'][idx])

                    outstr+='<option value=""></option>\n'
                    for i in loc['Options'][0]:
                        if not 'Default' in loc.keys():
                            outstr+='<option value="{0}">{0}</option>\n'.format(i)
                        else:
                            if i != theminit.actions[q["p1"][0]][q["p2"][0]]['Default'][idx]:
                                outstr+='<option value="{0}">{0}</option>\n'.format(i)
                            else:
                                outstr+='<option value="{0}" selected>{0}</option>\n'.format(i)

              #outstr+='<label for="Application" class="formlabel">Application:</label>'
              #outstr+='<input type="text" id="p3" name="Application" class=""><br>'
              #outstr+='<label for="Path"class="formlabel">Path:</label>'
              #outstr+='<input type="text" id="p4" name="Path" class="forminput"><br>'
              #outstr+='<label for="Parameters"class="formlabel">Parameters:</label>'
              #outstr+='<input type="text" id="p5" name="Parameters" class="forminput"><br>'
              outstr+='<input type="button" class="button" id="getbutton" value="Send">'
            else:
                outstr='{0} not yet supported'.format(q["p1"][0]+"/"+q["p2"][0])
            self.wfile.write(bytes(outstr,'utf8'))

        elif theminit.urlinfo.path.endswith('/action'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            hr = HideandResume()
            try:
#                hr.hideall(controlid=q["id"][0])
                outstr=''
                outstr+=theminit.themactions.action(q['id'], q['p1'], q['p2'], q['p3'], q['p4'], q['p5'])
                self.wfile.write(bytes('<p>'+outstr+'</p>','utf8'))
 #               hr.resume()
            except:
                self.wfile.write(bytes('<p>Unable to process Action({0},{1},{2},{3},{4},{5})</p>'.format(q['id'],q['p1'],q['p2'],q['p3'],q['p4'],q['p5']),'utf8'))
  #              hr.resume()
            finally:
   #             hr.resume()
                pass

        elif theminit.urlinfo.path.endswith('/getpic'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            outstr = ''

            hr = HideandResume()
            try:
                hr.hideall(controlid=q["id"][0])
                img1=themcontrols.ctrls.get(q["id"][0]).capture_as_image()

                exportpath=Path('temp/'+ q["id"][0]+'.png')
                img1.save(exportpath)
            except:
                hr.resume()
            finally:
                hr.resume()
            outstr += '<img src="temp/'+q["id"][0]+'.png" class="screenshot">'

            img2 = np.asarray(img1.convert('L'))

            #img3 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

            #try:
            outstr += '<div>'+pytesseract.image_to_pdf_or_hocr(img2, extension='hocr').decode()+'</div>'
            #except:
            #    pass

            self.wfile.write(bytes(outstr,'utf8'))
            img1.close()

        elif theminit.urlinfo.path.endswith('.png') or theminit.urlinfo.path.endswith('.ico'):
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            filepath=Path('./'+theminit.urlinfo.path)
            outstr=loadfile(filepath)
            self.wfile.write(bytes(outstr))
        else:
            con=themcontrols.ctrls.get(id=str(theminit.urlinfo.path).strip('/'))
            if isinstance(con, list):
                con=con[0]
            if con:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                outstr = ''
                with open('head.hi') as f:
                    outstr = f.read()

                f.closed

                outstr += theminit.themhtml.defaultsettings()

                try:
                    outstr += pywinhtmlw([con], True)
                except:
                    outstr += 'DOH!!'

                outstr += theminit.themhtml.keylisthtml()

                with open('footer.hi') as f:
                    outstr += f.read()
                self.wfile.write(bytes(outstr, 'utf8'))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('Cannot find:'+theminit.urlinfo.path,'utf8'))
