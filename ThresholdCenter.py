from collections import OrderedDict, defaultdict

class ThresholdCenter(object):
    def __init__(self, threshold_list):
        self.center = defaultdict(lambda: OrderedDict([('corr', 0.0), ('instant', 0.0), ('loss', 0.0)]))
        for threshold in threshold_list:
            self.center[threshold.id] = threshold.store

    def setInstantThreshold(self, id, instant):
        self.center[id]['instant'] = instant

    def setLossThreshold(self, id, loss):
        self.center[id]['loss'] = loss

    def setCorrThreshold(self, id, corr):
        self.center[id]['corr'] = corr

    def getInstantThreshold(self, id):
        return self.center[id]['instant']

    def getLossThreshold(self, id):
        return self.center[id]['loss']

    def getCorrThreshold(self, id):
        return self.center[id]['corr']


class Threshold(object):
    def __init__(self, id):
        self.id = id
        self.store = OrderedDict([('corr', 0.0), ('instant', 0.0), ('loss', 0.0)])

    def setThreshold(self, corr, instant, loss):
        self.store['corr'] = corr
        self.store['instant'] = instant
        self.store['loss'] = loss


thrshld_0153, thrshld_0164, thrshld_01f1, thrshld_0220, thrshld_02c0, thrshld_04b0, thrshld_04b1, thrshld_05a0, thrshld_05a2 = Threshold('0153'), Threshold('0164'), Threshold('01f1'), Threshold('0220'), Threshold('02c0'), Threshold('04b0'), Threshold('04b1'), Threshold('05a0'), Threshold('05a2')
threshold_list = [thrshld_0153, thrshld_0164, thrshld_01f1, thrshld_0220, thrshld_02c0, thrshld_04b0, thrshld_04b1, thrshld_05a0, thrshld_05a2]
threshold_center = ThresholdCenter(threshold_list)