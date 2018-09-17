import time
import csv
import codecs

f = codecs.open('./1-2B.csv', 'a+', 'gbk')
writer = csv.writer(f)
# 总数
total = 0

# # 第一组
# # 移动1个单位所需时间
# oneMovetime = 20
# # 移动2个单位所需时间
# twoMovetime = 33
# # 移动3个单位所需时间
# threeMovetime = 46
# # CNC加工完一道工序的物料所需时间
# oneProcessMaterialtime = 560
# # 两道工序第一道
# twoProcess_1 = 400
# # 两道工序第二道
# twoProcess_2 = 378
# # RGV 为 奇数上料所需时间
# oddMtltime = 28
# # RGV 为 偶数上料所需时间
# evenMtltime = 31
# # 清洗时间
# washtime = 25

# # 第二组
# # 移动1个单位所需时间
# oneMovetime = 23
# # 移动2个单位所需时间
# twoMovetime = 41
# # 移动3个单位所需时间
# threeMovetime = 59
# # CNC加工完一道工序的物料所需时间
# oneProcessMaterialtime = 560
# # 两道工序第一道
# twoProcess_1 = 280
# # 两道工序第二道
# twoProcess_2 = 500
# # RGV 为 奇数上料所需时间
# oddMtltime = 30
# # RGV 为 偶数上料所需时间
# evenMtltime = 35
# # 清洗时间
# washtime = 30

# 第三组
# 移动1个单位所需时间
oneMovetime = 18
# 移动2个单位所需时间
twoMovetime = 32
# 移动3个单位所需时间
threeMovetime = 46
# CNC加工完一道工序的物料所需时间
oneProcessMaterialtime = 560
# 两道工序第一道
twoProcess_1 = 455
# 两道工序第二道
twoProcess_2 = 182
# RGV 为 奇数上料所需时间
oddMtltime = 27
# RGV 为 偶数上料所需时间
evenMtltime = 32
# 清洗时间
washtime = 25


# 计算过去的秒数
timePassed = 0

#定义RGV类
class RGV_obj(object):
    global timePassed
    def __init__(self):
        self.position = [1,0,0,0]

    def addMtl_odd(self, cnc):
        global timePassed, oddMtltime, washtime
        cnc.working = True
        timePassed += oddMtltime
        cnc.starttime = timePassed

    def addMtl_even(self, cnc):
        global timePassed, evenMtltime, washtime
        cnc.working = True
        timePassed += evenMtltime
        cnc.starttime = timePassed

    def rmvMtl_odd(self, cnc):
        print('给', cnc.index, '换料')
        global timePassed, oddMtltime, washtime
        cnc.working = True
        # 换料时间
        timePassed += oddMtltime
        print('完成时间:',timePassed )
        cnc.starttime = timePassed


    def rmvMtl_even(self, cnc):
        print('给', cnc.index, '换料')
        global timePassed, evenMtltime, washtime
        cnc.working = True
        # 换料时间
        timePassed += evenMtltime
        print('完成时间:',timePassed )
        cnc.starttime = timePassed


    def distance(self, cnc):
        return abs(cnc.position - (self.position.index(1)+1))

    def move(self, dst):
        print('移动到:', dst)
        global timePassed, oneMovetime, twoMovetime, threeMovetime
        moveD = abs(self.position.index(1)+1 - dst)
        # print('移动距离：', moveD)
        if moveD == 0:
            timePassed += 0
        if moveD == 1:
            timePassed += oneMovetime
        if moveD == 2:
            timePassed += twoMovetime
        if moveD == 3:
            timePassed += threeMovetime
        print('移动完时间：', timePassed)
        self.position = [0,0,0,0]
        self.position[dst-1] = 1

# 定义cnc类
class CNC(object):
    def __init__(self, pos, isOdd,index, ProcessType): # 位置  奇偶数编号  编号  工序序号
        self.starttime = -1
        self.isOdd = isOdd
        self.position = pos
        self.working = False
        self.index = index
        self.ProcessType = ProcessType

    def finishtime(self):
        # 判断是处理第一道还是第二道工序的机器
        if self.ProcessType == 1:
            return self.starttime + twoProcess_1
        if self.ProcessType == 2:
            return self.starttime + twoProcess_2


# 实例化RGV和cnc
RGV = RGV_obj()

# 位置  奇偶数编号（True为奇数）  编号  工序序号
cnc1 = CNC(1, True  ,1  , 1)
cnc2 = CNC(1, False ,2  , 1)
cnc3 = CNC(2, True  ,3  , 1)
cnc4 = CNC(2, False ,4  , 2)
cnc5 = CNC(3, True  ,5  , 1)
cnc6 = CNC(3, False ,6  , 2)
cnc7 = CNC(4, True  ,7  , 1)
cnc8 = CNC(4, False ,8  , 2)


MtlCount = 0
# cnc集合
waitlist = [cnc1,cnc2,cnc3,cnc4,cnc5,cnc6,cnc7,cnc8]

firstlist = [cnc for cnc in waitlist if cnc.ProcessType == 1]
print(firstlist)
secondlist = [cnc for cnc in waitlist if cnc.ProcessType == 2]
print(secondlist)

while 1:
    if timePassed >= 28800:
        break
    # 遍历第一道工序的机器，寻找最近的空闲第一道工序机器
    closestCNC = []
    minDistance = 3
    for cnc in firstlist:
        if cnc.working == False:
            if RGV.distance(cnc) <= minDistance:
                minDistance = RGV.distance(cnc)
                closestCNC = cnc
    # 如果有空闲的第一道工序CNC
    if closestCNC != []:
        print('有空闲的第一道工序CNC')
        if closestCNC.working ==False:
            # RGV移动到最近的空闲的第一道工序机器
            RGV.move(closestCNC.position)
            # 上料
            if closestCNC.isOdd == True:
                RGV.addMtl_odd(closestCNC)
                print('上料给：', closestCNC.index)
                print('完成时间:',timePassed )
            if closestCNC.isOdd == False:
                RGV.addMtl_even(closestCNC)
                print('上料给：', closestCNC.index)
                print('完成时间:',timePassed )

    # 如果没有空闲的第一道工序CNC
    if closestCNC == []:
        print('没有空闲的第一道工序CNC')
        # 遍历所有的第一道工序CNC，检测是否有已完成的CNC
        finishedCNCs = []
        for cnc in firstlist:
            if timePassed >= cnc.finishtime():
                finishedCNCs.append(cnc)
        # 如果没有已完成第一道工序的CNC
        if finishedCNCs == []:
            quickestCNC = firstlist[0]
            # 遍历所有工作中CNC，寻找最先完成的
            for cnc in firstlist:
                if cnc.finishtime() < quickestCNC.finishtime():
                    quickestCNC = cnc
            # RGV移动到最先完成的CNC处
            RGV.move(quickestCNC.position)
            # 判断是否需要等待
            if timePassed < quickestCNC.finishtime():
                print('需等待:', quickestCNC.finishtime()-timePassed, '秒')
                timePassed += quickestCNC.finishtime() - timePassed
            if quickestCNC.isOdd == True:
                RGV.rmvMtl_odd(quickestCNC)
                # 寻找是否有空闲的第二道工序机器
                availableCNC2 = []
                # 遍历寻找空闲的第二道工序机器
                for cnc in secondlist:
                    if cnc.working == False:
                        availableCNC2.append(cnc)
                # 如果有空闲的第二道工序机器
                if availableCNC2 != []:
                    minDistance = RGV.distance(availableCNC2[0])
                    closestCNC = availableCNC2[0]
                    # 遍历空闲的第二道工序机器，寻找最近的
                    for cnc in availableCNC2:
                        if RGV.distance(cnc) < minDistance:
                            minDistance = RGV.distance(cnc)
                            closestCNC = cnc
                    # RGV移动到最近的空闲第二道工序CNC处
                    RGV.move(closestCNC.position)
                    # 换料
                    if closestCNC.isOdd == True:
                        writer.writerow(['开始上料', closestCNC.index, timePassed])
                        RGV.rmvMtl_odd(closestCNC)
                    if closestCNC.isOdd == False:
                        writer.writerow(['开始上料', closestCNC.index, timePassed])
                        RGV.rmvMtl_even(closestCNC)
                # 如果没有空闲的第二道工序机器
                if availableCNC2 == []:
                    quickestCNC = secondlist[0]
                    # 检测最先完成的第二道工序机器
                    for cnc in secondlist:
                        if cnc.finishtime() < quickestCNC.finishtime():
                            quickestCNC = cnc
                    # 移动到最先完成的第二道工序处
                    RGV.move(quickestCNC.position)
                    # 判断是否需要等待
                    if timePassed < quickestCNC.finishtime():
                        print('需等待:', quickestCNC.finishtime() - timePassed, '秒')
                        timePassed += quickestCNC.finishtime() - timePassed
                    # 换料
                    if quickestCNC.isOdd == True:
                        writer.writerow(['开始换料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_odd(quickestCNC)
                        timePassed += washtime
                        total += 1
                        print('总共：', total)

                    if quickestCNC.isOdd == False:
                        writer.writerow(['开始换料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_even(quickestCNC)
                        timePassed += washtime
                        total += 1
                        print('总共：', total)
            # 换偶数
            else:
                RGV.rmvMtl_even(quickestCNC)
                # 寻找是否有空闲的第二道工序机器
                availableCNC2 = []
                # 遍历寻找空闲的第二道工序机器
                for cnc in secondlist:
                    if cnc.working == False:
                        availableCNC2.append(cnc)
                # 如果有空闲的第二道工序机器
                if availableCNC2 != []:
                    minDistance = RGV.distance(availableCNC2[0])
                    closestCNC = availableCNC2[0]
                    # 遍历空闲的第二道工序机器，寻找最近的
                    for cnc in availableCNC2:
                        if RGV.distance(cnc) < minDistance:
                            minDistance = RGV.distance(cnc)
                            closestCNC = cnc
                    # RGV移动到最近的空闲第二道工序CNC处
                    RGV.move(closestCNC.position)
                    # 换料
                    if closestCNC.isOdd == True:
                        writer.writerow(['开始上料', closestCNC.index, timePassed])
                        RGV.rmvMtl_odd(closestCNC)
                    if closestCNC.isOdd == False:
                        writer.writerow(['开始上料', closestCNC.index, timePassed])
                        RGV.rmvMtl_even(closestCNC)
                # 如果没有空闲的第二道工序机器
                if availableCNC2 == []:
                    quickestCNC = secondlist[0]
                    # 检测最先完成的第二道工序机器
                    for cnc in secondlist:
                        if cnc.finishtime() < quickestCNC.finishtime():
                            quickestCNC = cnc
                    # 移动到最先完成的第二道工序机器处
                    RGV.move(quickestCNC.position)
                    # 判断是否需要等待
                    if timePassed < quickestCNC.finishtime():
                        print('需等待:', quickestCNC.finishtime() - timePassed, '秒')
                        timePassed += quickestCNC.finishtime() - timePassed
                    # 换料
                    if quickestCNC.isOdd == True:
                        writer.writerow(['开始换料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_odd(quickestCNC)
                        timePassed += washtime
                        total += 1
                        print('总共：', total)
                    if quickestCNC.isOdd == False:
                        writer.writerow(['开始换料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_even(quickestCNC)
                        timePassed += washtime
                        total += 1
                        print('总共：', total)


        # 如果有已完成的第一道工序CNC
        else:
            # 初始化监测数据
            closestCNC = finishedCNCs[0]
            minDistance = RGV.distance(closestCNC)
            # 寻找最近的已完成的CNC
            for cnc in finishedCNCs:
                if RGV.distance(cnc) < minDistance:
                    minDistance = RGV.distance(cnc)
                    closestCNC = cnc
            # 移动到最近的需要换料的CNC处
            RGV.move(closestCNC.position)
            # 换奇数料
            if closestCNC.isOdd == True:
                RGV.rmvMtl_odd(closestCNC)
                # 寻找是否有空闲的第二道工序机器
                availableCNC2 = []
                # 遍历寻找空闲的第二道工序机器
                for cnc in secondlist:
                    if cnc.working == False:
                        availableCNC2.append(cnc)
                # 如果有空闲的第二道工序机器
                if availableCNC2 != []:
                    minDistance = RGV.distance(availableCNC2[0])
                    closestCNC = availableCNC2[0]
                    # 遍历空闲的第二道工序机器，寻找最近的
                    for cnc in availableCNC2:
                        if RGV.distance(cnc) < minDistance:
                            minDistance = RGV.distance(cnc)
                            closestCNC = cnc
                    # RGV移动到最近的空闲第二道工序CNC处
                    RGV.move(closestCNC.position)
                    # 换料
                    if closestCNC.isOdd == True:
                        writer.writerow(['开始上料', closestCNC.index, timePassed])
                        RGV.rmvMtl_odd(closestCNC)
                    if closestCNC.isOdd == False:
                        writer.writerow(['开始上料', closestCNC.index, timePassed])
                        RGV.rmvMtl_even(closestCNC)
                # 如果没有空闲的第二道工序机器
                print('availableCNC2', availableCNC2)
                if availableCNC2 == []:
                    quickestCNC = secondlist[0]
                    # 检测最先完成的第二道工序机器
                    for cnc in secondlist:
                        if cnc.finishtime() < quickestCNC.finishtime():
                            quickestCNC = cnc
                    # 移动到最先完成的第二道工序处
                    print('这里', quickestCNC.index)
                    RGV.move(quickestCNC.position)
                    # 判断是否需要等待
                    if timePassed < quickestCNC.finishtime():
                        print('需等待:', quickestCNC.finishtime() - timePassed, '秒')
                        timePassed += quickestCNC.finishtime() - timePassed
                    print('332211', quickestCNC.isOdd)
                    print('332211',quickestCNC.isOdd)
                    # 换料
                    if quickestCNC.isOdd == True:
                        writer.writerow(['开始换料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_odd(quickestCNC)
                        timePassed += washtime
                        total += 1
                        print('总共：', total)
                    if quickestCNC.isOdd == False:
                        writer.writerow(['开始换料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_even(quickestCNC)
                        timePassed += washtime
                        total += 1
                        print('总共：', total)
            # 换偶数料
            else :
                RGV.rmvMtl_even(closestCNC)
                # 寻找是否有空闲的第二道工序机器
                availableCNC2 = []
                # 遍历寻找空闲的第二道工序机器
                for cnc in secondlist:
                    if cnc.working == False:
                        availableCNC2.append(cnc)
                # 如果有空闲的第二道工序机器
                if availableCNC2 != []:
                    minDistance = RGV.distance(availableCNC2[0])
                    closestCNC = availableCNC2[0]
                    # 遍历空闲的第二道工序机器，寻找最近的
                    for cnc in availableCNC2:
                        if RGV.distance(cnc) < minDistance:
                            minDistance = RGV.distance(cnc)
                            closestCNC = cnc
                    # RGV移动到最近的空闲第二道工序CNC处
                    RGV.move(closestCNC.position)
                    # 换料
                    if closestCNC.isOdd == True:
                        writer.writerow(['开始上料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_odd(closestCNC)
                    if closestCNC.isOdd == False:
                        writer.writerow(['开始上料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_even(closestCNC)
                # 如果没有空闲的第二道工序机器
                if availableCNC2 == []:
                    quickestCNC = secondlist[0]
                    # 检测最先完成的第二道工序机器
                    for cnc in secondlist:
                        if cnc.finishtime() < quickestCNC.finishtime():
                            quickestCNC = cnc
                    # 移动到最先完成的第二道工序处
                    RGV.move(quickestCNC.position)
                    # 判断是否需要等待
                    if timePassed < quickestCNC.finishtime():
                        print('需等待:', quickestCNC.finishtime() - timePassed, '秒')
                        timePassed += quickestCNC.finishtime() - timePassed
                    # 换料
                    if quickestCNC.isOdd == True:
                        writer.writerow(['开始换料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_odd(quickestCNC)
                        timePassed += washtime
                        total += 1
                        print('总共：', total)
                    if quickestCNC.isOdd == False:
                        writer.writerow(['开始换料', quickestCNC.index, timePassed])
                        RGV.rmvMtl_even(quickestCNC)
                        timePassed += washtime
                        total += 1
                        print('总共：', total)
