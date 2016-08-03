# coding: utf8

class ReportItem:
    
    def __init__(self, name = None, debug = None):
        self.debug = debug
        self.data = {}
        self.data["name"] = name

    def set(self, name, uvalue):
        self.data[name] = uvalue

    def show(self):
        print self.data


class Report:
    def __init__(self, debug = None):
        self.debug = debug
        self.reportItem = []
        self.data = {}
    
    def add(self, reportItem):
        self.reportItem.append(reportItem)

    def set(self, name, uvalue):
        self.data[name] = uvalue

    def show(self):
        print "Report\n"
        print "Parameters: \n%s\n" % self.data
        print "Hosts:"
        for i in self.reportItem:
            i.show()
