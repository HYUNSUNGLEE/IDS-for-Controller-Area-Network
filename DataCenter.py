from collections import OrderedDict, defaultdict
from numpy import corrcoef

class ll(list):
    def check(self):
        if self.__len__() >= 5000:
            del self[0:1000]

    def append(self, i):
        self.check()
        super(ll, self).append(i)

class DataCenter(object):
    def __init__(self, data_list):
        self.center = defaultdict(lambda: OrderedDict([('order', ll()), ('interval', ll()), ('instant', 0), ('loss', 0), ('total', 0)]))
        for data in data_list:
            self.center[data.id] = data.store

    def getInstantRatio(self, id):
        tmp = self.center[id]
        return (tmp['instant'] / float(tmp['total']))

    def getLossRatio(self, id):
        tmp = self.center[id]
        return (tmp['loss'] / float(tmp['total']))

    def getCorr(self, id):
        tmp = self.center[id]
        return corrcoef(tmp['order'], tmp['interval'])[0, 1]

    def getAver(self, id):
        tmp = self.center[id]['interval']
        return float(sum(tmp)/len(tmp))

class Data(object):
    def __init__(self, id):
        self.id = id
        self.store = OrderedDict([('order', ll()), ('interval', ll()), ('instant', 0), ('loss', 0), ('total', 0)])

    def putStore(self, tup):
        tmp = self.store
        tmp['total'] += 1
        if tup[0] == 0:
            tmp['loss'] += 1
        else:
            if tup[0] == 1:
                tmp['instant'] += 1
            tmp['order'].append(tup[0])
            tmp['interval'].append(tup[1])


data_0153, data_0164, data_01f1, data_0220, data_02c0, data_04b0, data_04b1, data_05a0, data_05a2 = Data('0153'), Data('0164'), Data('01f1'), Data('0220'), Data('02c0'), Data('04b0'), Data('04b1'), Data('05a0'), Data('05a2')
data_list = [data_0153, data_0164, data_01f1, data_0220, data_02c0, data_04b0, data_04b1, data_05a0, data_05a2]
data_center = DataCenter(data_list)