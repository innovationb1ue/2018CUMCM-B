import time
import csv
import codecs
from random import random

f = codecs.open('./1-3.csv', 'a+', 'gbk')
writer = csv.writer(f)

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
#
# # 第二组
# # 移动1个单位所需时间
# oneMovetime = 23
# # 移动2个单位所需时间
# twoMovetime = 41
# # 移动3个单位所需时间
# threeMovetime = 59
# # CNC加工完一道工序的物料所需时间
# oneProcessMaterialtime = 580
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
oneProcessMaterialtime = 545
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

    # 不考虑连续爆炸的情况，上一次爆炸则这次自动设置为正常
    def randomBoom(self, cnc):
        if cnc.boom == True:
            cnc.boom = False
            return False
        p = random()
        if p <= 0.01:
            print('爆炸了')
            writer.writerow(['爆炸了', cnc.index, timePassed, timePassed+1200])
            cnc.boom = True
            return True

    def addMtl_odd(self, cnc):
        global timePassed, oddMtltime, washtime
        cnc.working = True
        timePassed += oddMtltime
        cnc.starttime = timePassed
        self.randomBoom(cnc)


    def addMtl_even(self, cnc):
        global timePassed, evenMtltime, washtime
        cnc.working = True
        timePassed += evenMtltime
        cnc.starttime = timePassed
        self.randomBoom(cnc)


    def rmvMtl_odd(self, cnc):
        global timePassed, oddMtltime, washtime
        # 换料时间
        timePassed += oddMtltime
        cnc.starttime = timePassed
        self.randomBoom(cnc)



    def rmvMtl_even(self, cnc):
        global timePassed, evenMtltime, washtime
        # 换料时间
        timePassed += evenMtltime
        cnc.starttime = timePassed
        self.randomBoom(cnc)



    def distance(self, cnc):
        return abs(cnc.position - (self.position.index(1)+1))


    def move(self, dst):
        print('移动到:', dst)
        global timePassed, oneMovetime, twoMovetime, threeMovetime
        moveD = abs(self.position.index(1)+1 - dst)
        print('移动距离：', moveD)
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
    def __init__(self, pos, isOdd,index):
        self.boom = False
        self.starttime = -1
        self.isOdd = isOdd
        self.position = pos
        self.working = False
        self.index = index
    def finishtime(self):
        if self.boom == False:
            return self.starttime + oneProcessMaterialtime
        if self.boom == True:
            return self.starttime + 1200



# 实例化RGV和cnc
RGV = RGV_obj()

cnc1 = CNC(1, True, 1)
cnc2 = CNC(1, False,2)
cnc3 = CNC(2, True,3)
cnc4 = CNC(2, False,4)
cnc5 = CNC(3, True,5)
cnc6 = CNC(3, False,6)
cnc7 = CNC(4, True,7)
cnc8 = CNC(4, False,8)


MtlCount = 0
# cnc集合
waitlist = [cnc1,cnc2,cnc3,cnc4,cnc5,cnc6,cnc7,cnc8]

while 1:
    # 检测是否有空闲cnc
    availableCNC = []
    for cnc in waitlist:
        if cnc.working == False:
            availableCNC.append(cnc)
    # 如果有空闲的cnc
    if availableCNC != []:
        closestCNC = availableCNC[0]
        for cnc in availableCNC:
            if RGV.distance(cnc) < RGV.distance(closestCNC):
                closestCNC = cnc
        # 移动到最近的CNC
        RGV.move(closestCNC.position)
        # 上料
        if closestCNC.isOdd == True:
            writer.writerow(['开始上料', closestCNC.index, timePassed])
            print('上料给:', closestCNC.index)
            RGV.addMtl_odd(closestCNC)
            print('完成时间:', timePassed)
        if closestCNC.isOdd == False:
            writer.writerow(['开始上料', closestCNC.index, timePassed])
            print('上料给:', closestCNC.index)
            RGV.addMtl_even(closestCNC)
            print('完成时间:', timePassed)
    # 没有空闲的cnc
    if availableCNC == []:
        # 保存最先完成的cnc
        quickestCNC = waitlist[0]
        for cnc in waitlist:
            if cnc.finishtime()< quickestCNC.finishtime():
                quickestCNC = cnc
        # 如果需要等待
        if timePassed < quickestCNC.finishtime():
            print('需等待:', quickestCNC.finishtime() - timePassed)
            timePassed += quickestCNC.finishtime() - timePassed
        # 移动到最先完成的CNC处
        RGV.move(quickestCNC.position)
        # 换料
        if quickestCNC.isOdd == True:
            print('换料给:', quickestCNC.index)
            a = quickestCNC.boom
            if a:
                print('爆炸了')
            writer.writerow(['开始换料', quickestCNC.index, timePassed])
            RGV.rmvMtl_odd(quickestCNC)
            # 如果是好料，则需要清洗
            if a == False:
                timePassed += washtime
            print('完成时间:', timePassed)
        if quickestCNC.isOdd == False:
            a = quickestCNC.boom
            if a:
                print('爆炸了')
            print('换料给:', quickestCNC.index)
            writer.writerow(['开始换料', quickestCNC.index, timePassed])
            RGV.rmvMtl_even(quickestCNC)
            if a == False:
                timePassed += washtime
            print('完成时间:', timePassed)
    if timePassed >= 28800:
        break
