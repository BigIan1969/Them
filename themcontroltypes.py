
#each type has a list click, send keys, select

class DefDict(dict):
    # dictionary that returns zero for missing keys
    # keys with zero values are not stored

    def __missing__(self,key):
        return(None)
        

controltypes=DefDict()
controltypes['Button']      =   [True,False,False]
controltypes['CheckBox']    =   [True,False,False]
controltypes['ComboBox']    =   [True,True,True]
controltypes['Edit']        =   [True,True,False]
controltypes['Image']       =   [True,False,False]
controltypes['List']        =   [True,True,True]
controltypes['ListItem']    =   [True,True,True]
controltypes['Menu']        =   [True,True,True]
controltypes['MenuBar']     =   [True,True,True]
controltypes['MenuItem']    =   [True,True,True]
controltypes['Pane']        =   [True,True,False]
controltypes['RadioButton'] =   [True,False,False]
controltypes['Spinner']     =   [True,True,True]
controltypes['Tab']         =   [True,False,True]
controltypes['TabItem']     =   [True,False,True]
controltypes['Table']       =   [True,True,True]
controltypes['Text']        =   [True,True,False]
controltypes['Tree']        =   [True,True,True]
controltypes['DataItem']    =   [True,True,True]
controltypes['TreeItem']    =   [True,True,True]
controltypes['Window']      =   [True,True,True]

