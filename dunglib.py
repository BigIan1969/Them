class dung:

    def setdicttolist(self, target, source, default):

        for i in source:
            if not i[0] in target:
                target[i[0]] = default

