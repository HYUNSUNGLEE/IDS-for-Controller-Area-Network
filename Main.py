from QueueAndWorker import *
from decimal import Decimal
from DataCenter import *
from ThresholdCenter import *

def storeData(tup):
    global current
    flag = True if current != int(tup[1]) else False
    current = int(tup[1])
    id = tup[0]
    order = tup[2]
    interval = tup[3] - tup[1]
    var = 'data_' + id
    exec("%s.putStore((%d, %.6f))" % (var, order, interval))
    return (flag, current)

settingFlag = True
def check(tup):
    global settingFlag
    def setThreshold():
        for k, v in threshold_center.center.items():
            threshold_center.setCorrThreshold(k, data_center.getCorr(k) - 0.03)
            threshold_center.setInstantThreshold(k, data_center.getInstantRatio(k) - 0.03)
            threshold_center.setLossThreshold(k, data_center.getLossRatio(k) + 0.03)
    if tup[1] - startTime > 100:
        if tup[0]:
            anomaly_id = []
            for k, v in data_center.center.items():
                if data_center.getCorr(k) < threshold_center.getCorrThreshold(k):
                    anomaly_id.append((k, 1, data_center.getCorr(k)))
                if data_center.getInstantRatio(k) < threshold_center.getInstantThreshold(k):
                    anomaly_id.append((k, 2, data_center.getInstantRatio(k)))
                if data_center.getLossRatio(k) > threshold_center.getLossThreshold(k):
                    anomaly_id.append((k, 3, data_center.getLossRatio(k)))
            return (True, anomaly_id, tup[1])
    elif tup[1] - startTime > 99 and settingFlag:
        settingFlag = False
        setThreshold()
    return (False, 0, tup[1])

def alarm(tup):
    if tup[0]:
        if tup[1]:
            print('======================================')
            for id, flag, k in tup[1]:
                if flag == 1:
                    print('%d --- ID:%s Corr Error -> %f' % (tup[2], id, k))
                elif flag == 2:
                    print('%d --- ID:%s Inst Error -> %f' % (tup[2], id, k))
                elif flag == 3:
                    print('%d --- ID:%s Loss Error -> %f' % (tup[2], id, k))
        else:
            print('%d: Normal' % tup[2])

if __name__ == '__main__':
    current = 0.0

    storeData_queue = ClosableQueue()
    check_queue = ClosableQueue()
    alarm_queue = ClosableQueue()
    done_queue = ClosableQueue()

    threads = [
        StoppableWorker(storeData, storeData_queue, check_queue),
        StoppableWorker(check, check_queue, alarm_queue),
        StoppableWorker(alarm, alarm_queue, done_queue)
    ]

    for thread in threads:
        thread.start()

    lines = open('Dataset.txt').read().splitlines()
    remoteFlag, order, target, tup = False, 0, '', ()
    startTime = int(Decimal(lines[0].split()[1]))
    for line in lines:
        words = line.split()
        id, timestamp, ctrl = words[3], Decimal(words[1]), words[4]
        if remoteFlag:
            order += 1
            if (order > 6):
                remoteFlag = False
                tup += (0, 0)
                storeData_queue.put(tup)
                continue
            if (target == id):
                remoteFlag = False
                tup += (order, timestamp)
                storeData_queue.put(tup)
                continue
            if ctrl == '100':
                tup += (0, 0)
                storeData_queue.put(tup)
                order = 0
                target = id
                tup = (id, timestamp,)
                continue
        if ctrl == '100':
            remoteFlag = True
            order = 0
            target = id
            tup = (id, timestamp,)

    storeData_queue.close()
    storeData_queue.join()
    check_queue.close()
    check_queue.join()
    alarm_queue.close()
    alarm_queue.join()

    print('Done queue size is ' + str(done_queue.qsize()))