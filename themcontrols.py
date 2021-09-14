from pywinauto import Desktop
import copy
import shelve


class Expresions():
    def not_in(self, sourcestr, sourcedict):
        return(not sourcestr in sourcedict)
    def is_in(self, sourcestr, sourcedict):
        return(sourcestr in sourcedict)
    def not_parent_and_not_blank(self, element_parent, property_parent):
        return(element_parent!=property_parent and property_parent!="")
    def key1_equals_key2_or_either_equals_string(self, key1, key2, sourcestr):
        return(key1==key2 or key1==sourcestr or key2==sourcestr)


class Controls:
    exp = Expresions()
    control={}
    controlids={}
    search={}
    settings={}

    def __init__(self):
        self.search = shelve.open('Search.db', writeback=True)
        self.settings= shelve.open('Settings', writeback=True)
        if self.exp.not_in('forcecoords', self.settings):
            self.settings['forcecoords'] = 'false'
        if self.exp.not_in('hashsize', self.settings):
            self.settings['hashsize'] = '12'
        if self.exp.not_in('loadmode', self.settings):
            self.settings['loadmode'] = 'Lazy'
        if self.exp.not_in('autoexpand', self.settings):
            self.settings['autoexpand'] = 'No'
        if self.exp.not_in('tech', self.settings):
            self.settings['tech'] = 'uia'

        pass

    def add(self, cid, obj, searchcrit):
        searchc=copy.copy(searchcrit)
        for i in ['windowtext','processid','rectangle','visible','children']:
          searchc.pop(i)
        self.control[cid] = obj
        self.controlids[id(obj)] = cid
        self.search[cid] = searchc

    def get(self, id):
        if self.exp.is_in(id, Controls.control.keys()):
          return(Controls.control[id])
        else:
          print("SEARCHING...")
          s=self.search[str(id)]
          backend=s['backend']
          parentc = s['parent']
          for k,v in s.items():
            x=[]
            if k == 'title':
              x=Desktop(backend=backend).windows(title=v)
            elif k == 'parent':
              continue
            elif k == 'class':
              x=Desktop(backend=backend).windows(class_name=v)
            elif k == 'controltype':
              x=Desktop(backend=backend).windows(control_type=v)
            elif k == 'id':
              x=Desktop(backend=backend).windows(control_id=v)
            elif k == 'backend':
                continue
            if x is None:
                continue
            if len(x) == 0:
                continue
            for i in x:
              if self.exp.not_parent_and_not_blank(i.parent().element_info.name, parentc):
                x.pop()
            if len(x) == 1:
              self.control[id] = x
              return(x)
    
          for rk,rv in s.items():
            if rv=="":
              continue
            for k,v in s.items():
              if v=="":
                continue
              if self.exp.key1_equals_key2_or_either_equals_string(rk,k, 'backend'):
                continue
              s1={}
              s1[rk]=rv
              s1[k]=v
              x=Desktop(backend = backend).windows(**s1)

              for i in x:
                  if i.parent().element_info.name != parentc:
                      x.pop()
              if len(x)==1:
                self.control[id]=x
                return(x)
          print("...Not Found")
    def __del__(self):
      self.search.close()
      self.settings.close()

ctrls = Controls