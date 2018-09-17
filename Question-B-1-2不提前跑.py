import time
import csv
import codecs

f = codecs.open('./二道工序.csv', 'a+', 'gbk')
writer = csv.writer(f)
# 总数
total = 0

# #第一组
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

# 第二组
# 移动1个单位所需时间
oneMovetime = 23
# 移动2个单位所需时间
twoMovetime = 41
# 移动3个单位所需时间
threeMovetime = 59
# CNC加工完一道工序的物料所需时间
oneProcessMaterialtime = 560
# 两道工序第一道
twoProcess_1 = 280
# 两道工序第二道
twoProcess_2 = 500
# RGV 为 奇数上料所需时间
oddMtltime = 30
# RGV 为 偶数上料所需时间
evenMtltime = 35
# 清洗时间
washtime = 30

# # 第三组
# # 移动1个单位所需时间
# oneMovetime = 18
# # 移动2个单位所需时间
# twoMovetime = 32
# # 移动3个单位所需时间
# threeMovetime = 46
# # CNC加工完一道工序的物料所需时间
# oneProcessMaterialtime = 560
# # 两道工序第一道
# twoProcess_1 = 455
# # 两道工序第二道
# twoProcess_2 = 182
# # RGV 为 奇数上料所需时间
# oddMtltime = 27
# # RGV 为 偶数上料所需时间
# evenMtltime = 32
# # 清洗时间
# washtime = 25



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
cnc2 = CNC(1, False ,2  , 2)
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
    # 检测是否有空闲第一道工序cnc
    availableCNC = []
    for cnc in firstlist:
        if cnc.working == False:
            availableCNC.append(cnc)
    # 如果有空闲的第一道工序cnc
    if availableCNC != []:
        # 寻找最近的空闲cnc
        closestCNC = availableCNC[0]
        for cnc in availableCNC:
            if RGV.distance(closestCNC) > RGV.distance(cnc):
                closestCNC = cnc
        # 移动到最近的空闲第一道工序cnc
        RGV.move(closestCNC.position)
        # 加料
        if closestCNC.isOdd == True:
            writer.writerow(['一道工序', closestCNC.index, timePassed])
            RGV.addMtl_odd(closestCNC)
        if closestCNC.isOdd == False:
            writer.writerow(['一道工序', closestCNC.index, timePassed])
            RGV.addMtl_even(closestCNC)

    # 如果没有空闲的第一道工序CNC
    else:
        # 检测是否有已完成的CNC
        finishedCNC = []
        for cnc in firstlist:
            if timePassed > cnc.finishtime():
                finishedCNC.append(cnc)
        # 如果有已完成的cnc
        if finishedCNC != []:
            closestCNC = finishedCNC[0]
            for cnc in finishedCNC:
                if RGV.distance(cnc) < RGV.distance(closestCNC):
                    closestCNC = cnc
            # 移动到最近的已完成CNC
            RGV.move(closestCNC.position)
            # 换料
            if closestCNC.isOdd == True:
                writer.writerow(['一道工序', closestCNC.index, timePassed])
                RGV.rmvMtl_odd(closestCNC)
                print('完成时间:', timePassed)
                # 检测是否有空闲的CNC2
                availableCNC2 = []
                for cnc in secondlist:
                    if cnc.working == False:
                        availableCNC2.append(cnc)
                # 如果有空闲的CNC2
                if availableCNC2 != []:
                    # 寻找最近的空闲CNC2
                    closestCNC2 = availableCNC2[0]
                    for cnc in availableCNC2:
                        if RGV.distance(closestCNC2) > RGV.distance(cnc):
                            closestCNC2 = cnc
                    # 判断是否需要等待
                    if timePassed < closestCNC2.finishtime():
                        print('需要等待:', closestCNC2.finishtime() - timePassed)
                        timePassed += closestCNC2.finishtime() - timePassed
                    # 移动
                    RGV.move(closestCNC2.position)
                    # 换料
                    if closestCNC2.isOdd == True:
                        writer.writerow(['二道工序', closestCNC2.index, timePassed])
                        RGV.rmvMtl_odd(closestCNC2)
                    if closestCNC2.isOdd == False:
                        writer.writerow(['二道工序', closestCNC2.index, timePassed])
                        RGV.rmvMtl_even(closestCNC2)
                # 如果没有空闲的CNC2
                if availableCNC2 == []:
                    # 检测是否有已完成的CNC2
                    finishedCNC2 = []
                    for cnc in secondlist:
                        if timePassed > cnc.finishtime():
                            finishedCNC2.append(cnc)
                    # 如果有已完成的CNC2
                    if finishedCNC2 != []:
                        closestCNC2 = finishedCNC2[0]
                        # 寻找最近的完成的CNC2
                        for cnc in finishedCNC2:
                            if RGV.distance(cnc) < RGV.distance(closestCNC2):
                                closestCNC2 = cnc
                        # 移动
                        RGV.move(closestCNC2.position)
                        # 换料
                        if closestCNC2.isOdd == True:
                            writer.writerow(['二道工序', closestCNC2.index, timePassed])
                            RGV.rmvMtl_odd(closestCNC2)
                            timePassed += washtime
                        if closestCNC2.isOdd == False:
                            writer.writerow(['二道工序', closestCNC2.index, timePassed])
                            RGV.rmvMtl_even(closestCNC2)
                            timePassed += washtime
                        continue
                    # 如果没有已完成的CNC2
                    # 寻找最先完成的CNC2
                    quickestCNC2 = secondlist[0]
                    for cnc in secondlist:
                        if cnc.finishtime() < quickestCNC2.finishtime():
                            quickestCNC2 = cnc
                    # 等待
                    if timePassed < quickestCNC2.finishtime():
                        print('需等待:', quickestCNC2.finishtime() - timePassed)
                        timePassed += quickestCNC2.finishtime() - timePassed
                    # 移动
                    RGV.move(quickestCNC2.position)
                    # 换料
                    if quickestCNC2.isOdd == True:
                        writer.writerow(['二道工序', quickestCNC2.index, timePassed])
                        RGV.rmvMtl_odd(quickestCNC2)
                        timePassed += washtime
                    if quickestCNC2.isOdd == False:
                        writer.writerow(['二道工序', quickestCNC2.index, timePassed])
                        RGV.rmvMtl_even(quickestCNC2)
                        timePassed += washtime
            if closestCNC.isOdd == False:
                writer.writerow(['一道工序', quickestCNC.index, timePassed])
                RGV.rmvMtl_even(closestCNC)
                print('完成时间:', timePassed)
                # 检测是否有空闲的CNC2
                availableCNC2 = []
                for cnc in secondlist:
                    if cnc.working == False:
                        availableCNC2.append(cnc)
                # 如果有空闲的CNC2
                if availableCNC2 != []:
                    # 寻找最近的空闲CNC2
                    closestCNC2 = availableCNC2[0]
                    for cnc in availableCNC2:
                        if RGV.distance(closestCNC2) > RGV.distance(cnc):
                            closestCNC2 = cnc
                    # 判断是否需要等待
                    if timePassed < closestCNC2.finishtime():
                        print('需要等待:', closestCNC2.finishtime() - timePassed)
                        timePassed += closestCNC2.finishtime() - timePassed
                    # 移动
                    RGV.move(closestCNC2.position)
                    # 换料
                    if closestCNC2.isOdd == True:
                        writer.writerow(['二道工序', closestCNC2.index, timePassed])
                        RGV.rmvMtl_odd(closestCNC2)
                    if closestCNC2.isOdd == False:
                        writer.writerow(['二道工序', closestCNC2.index, timePassed])
                        RGV.rmvMtl_even(closestCNC2)
                # 如果没有空闲的CNC2
                if availableCNC2 == []:
                    # 检测是否有已完成的CNC2
                    finishedCNC2 = []
                    for cnc in secondlist:
                        if timePassed > cnc.finishtime():
                            finishedCNC2.append(cnc)
                    # 如果有已完成的CNC2
                    if finishedCNC2 != []:
                        closestCNC2 = finishedCNC2[0]
                        # 寻找最近的完成的CNC2
                        for cnc in finishedCNC2:
                            if RGV.distance(cnc) < RGV.distance(closestCNC2):
                                closestCNC2 = cnc
                        # 移动
                        RGV.move(closestCNC2.position)
                        # 换料
                        if closestCNC2.isOdd == True:
                            writer.writerow(['二道工序', closestCNC2.index, timePassed])
                            RGV.rmvMtl_odd(closestCNC2)
                            timePassed += washtime
                        if closestCNC2.isOdd == False:
                            writer.writerow(['二道工序', closestCNC2.index, timePassed])
                            RGV.rmvMtl_even(closestCNC2)
                            timePassed += washtime
                        continue
                    # 如果没有已完成的CNC2
                    # 寻找最先完成的CNC2
                    quickestCNC2 = secondlist[0]
                    for cnc in secondlist:
                        if cnc.finishtime() < quickestCNC2.finishtime():
                            quickestCNC2 = cnc
                    # 等待
                    if timePassed < quickestCNC2.finishtime():
                        print('需等待:', quickestCNC2.finishtime() - timePassed)
                        timePassed += quickestCNC2.finishtime() - timePassed
                    # 移动
                    RGV.move(quickestCNC2.position)
                    # 换料
                    if quickestCNC2.isOdd == True:
                        writer.writerow(['二道工序', quickestCNC2.index, timePassed])
                        RGV.rmvMtl_odd(quickestCNC2)
                        timePassed += washtime
                    if quickestCNC2.isOdd == False:
                        writer.writerow(['二道工序', quickestCNC2.index, timePassed])
                        RGV.rmvMtl_even(quickestCNC2)
                        timePassed += washtime

        # 如果没有已完成的cnc
        # 寻找最先完成的第一道工序cnc:
        quickestCNC = firstlist[0]
        for cnc in firstlist:
            if cnc.finishtime()<quickestCNC.finishtime():
                quickestCNC = cnc

        # 判断是否需要等待
        if timePassed < quickestCNC.finishtime():
            print('需等待:', quickestCNC.finishtime() - timePassed)
            timePassed += quickestCNC.finishtime() - timePassed
        # 移动
        RGV.move(quickestCNC.position)
        # 换料
        if quickestCNC.isOdd == True:
            writer.writerow(['一道工序', quickestCNC.index, timePassed])
            RGV.addMtl_odd(quickestCNC)
            # 检测是否有空闲的CNC2
            availableCNC2 = []
            for cnc in secondlist:
                if cnc.working == False:
                    availableCNC2.append(cnc)
            # 如果有空闲的CNC2
            if availableCNC2 != []:
                # 寻找最近的空闲CNC2
                closestCNC2 = availableCNC2[0]
                for cnc in availableCNC2:
                    if RGV.distance(closestCNC2) > RGV.distance(cnc):
                        closestCNC2 = cnc
                # 判断是否需要等待
                if timePassed < closestCNC2.finishtime():
                    print('需要等待:', closestCNC2.finishtime() - timePassed)
                    timePassed += closestCNC2.finishtime() - timePassed
                # 移动
                RGV.move(closestCNC2.position)
                # 换料
                if closestCNC2.isOdd == True:
                    writer.writerow(['二道工序', closestCNC2.index, timePassed])
                    RGV.rmvMtl_odd(closestCNC2)
                if closestCNC2.isOdd == False:
                    writer.writerow(['二道工序', closestCNC2.index, timePassed])
                    RGV.rmvMtl_even(closestCNC2)
            # 如果没有空闲的CNC2
            if availableCNC2 == []:
                # 检测是否有已完成的CNC2
                finishedCNC2 = []
                for cnc in secondlist:
                    if timePassed > cnc.finishtime():
                        finishedCNC2.append(cnc)
                # 如果有已完成的CNC2
                if finishedCNC2 != []:
                    closestCNC2 = finishedCNC2[0]
                    # 寻找最近的完成的CNC2
                    for cnc in finishedCNC2:
                        if RGV.distance(cnc) < RGV.distance(closestCNC2):
                            closestCNC2 = cnc
                    # 移动
                    RGV.move(closestCNC2.position)
                    # 换料
                    if closestCNC2.isOdd == True:
                        writer.writerow(['二道工序', closestCNC2.index, timePassed])
                        RGV.rmvMtl_odd(closestCNC2)
                        timePassed += washtime
                    if closestCNC2.isOdd == False:
                        writer.writerow(['二道工序', closestCNC2.index, timePassed])
                        RGV.rmvMtl_even(closestCNC2)
                        timePassed += washtime
                    continue
                # 寻找最先完成的CNC2
                quickestCNC2 = secondlist[0]
                for cnc in secondlist:
                    if cnc.finishtime() < quickestCNC2.finishtime():
                        quickestCNC2 = cnc
                # 等待
                if timePassed < quickestCNC2.finishtime():
                    print('需等待:', quickestCNC2.finishtime() - timePassed)
                    timePassed += quickestCNC2.finishtime() - timePassed
                # 移动
                RGV.move(quickestCNC2.position)
                # 换料

                if quickestCNC2.isOdd == True:
                    writer.writerow(['二道工序', quickestCNC2.index, timePassed])
                    RGV.rmvMtl_odd(quickestCNC2)
                    timePassed += washtime
                if quickestCNC2.isOdd == False:
                    writer.writerow(['二道工序', quickestCNC2.index, timePassed])
                    RGV.rmvMtl_even(quickestCNC2)
                    timePassed += washtime

        if quickestCNC.isOdd == False:
            writer.writerow(['一道工序', quickestCNC.index, timePassed])
            RGV.addMtl_even(quickestCNC)
            # 检测是否有空闲的CNC2
            availableCNC2 = []
            for cnc in secondlist:
                if cnc.working == False:
                    availableCNC2.append(cnc)

            # 如果有空闲的CNC2
            if availableCNC2 != []:
                # 寻找最近的空闲CNC2
                closestCNC2 = availableCNC2[0]
                for cnc in availableCNC2:
                    if RGV.distance(closestCNC2) > RGV.distance(cnc):
                        closestCNC2 = cnc
                # 判断是否需要等待
                if timePassed < closestCNC2.finishtime():
                    print('需要等待:', closestCNC2.finishtime() - timePassed)
                    timePassed += closestCNC2.finishtime() - timePassed
                # 移动
                RGV.move(closestCNC2.position)
                # 换料
                if closestCNC2.isOdd == True:
                    writer.writerow(['二道工序', closestCNC2.index, timePassed])
                    RGV.rmvMtl_odd(closestCNC2)
                if closestCNC2.isOdd == False:
                    writer.writerow(['二道工序', closestCNC2.index, timePassed])
                    RGV.rmvMtl_even(closestCNC2)

            # 如果没有空闲的CNC2
            if availableCNC2 == []:
                # 检测是否有已完成的CNC2
                finishedCNC2 = []
                for cnc in secondlist:
                    if timePassed > cnc.finishtime():
                        finishedCNC2.append(cnc)
                # 如果有已完成的CNC2
                if finishedCNC2 != []:
                    closestCNC2 = finishedCNC2[0]
                    # 寻找最近的完成的CNC2
                    for cnc in finishedCNC2:
                        if RGV.distance(cnc) < RGV.distance(closestCNC2):
                            closestCNC2 = cnc
                    # 移动
                    RGV.move(closestCNC2.position)
                    # 换料
                    if closestCNC2.isOdd == True:
                        writer.writerow(['二道工序', closestCNC2.index, timePassed])
                        RGV.rmvMtl_odd(closestCNC2)
                        timePassed += washtime
                    if closestCNC2.isOdd == False:
                        writer.writerow(['二道工序', closestCNC2.index, timePassed])
                        RGV.rmvMtl_even(closestCNC2)
                        timePassed += washtime
                    continue
                # 寻找最先完成的CNC2
                quickestCNC2 = secondlist[0]
                for cnc in secondlist:
                    if cnc.finishtime() < quickestCNC2.finishtime():
                        quickestCNC2 = cnc
                # 等待
                if timePassed < quickestCNC2.finishtime():
                    print('需等待:', quickestCNC2.finishtime() - timePassed)
                    timePassed += quickestCNC2.finishtime() - timePassed
                # 移动
                RGV.move(quickestCNC2.position)
                # 换料
                if quickestCNC2.isOdd == True:
                    writer.writerow(['二道工序', quickestCNC2.index, timePassed])
                    RGV.rmvMtl_odd(quickestCNC2)
                    timePassed += washtime
                if quickestCNC2.isOdd == False:
                    writer.writerow(['二道工序', quickestCNC2.index, timePassed])
                    RGV.rmvMtl_even(quickestCNC2)
                    timePassed += washtime
    if timePassed >= 28800:
        break
