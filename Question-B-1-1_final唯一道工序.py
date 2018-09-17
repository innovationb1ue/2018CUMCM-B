import time
import csv
import codecs

f = codecs.open('./1-1.csv', 'a+', 'gbk')
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
#
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
        global timePassed, oddMtltime, washtime
        # 换料时间
        timePassed += oddMtltime
        cnc.starttime = timePassed
        # 清洗时间
        timePassed += washtime


    def rmvMtl_even(self, cnc):
        global timePassed, evenMtltime, washtime
        # 换料时间
        timePassed += evenMtltime
        cnc.starttime = timePassed
        # 清洗时间
        timePassed += washtime


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
        self.starttime = -1
        self.isOdd = isOdd
        self.position = pos
        self.working = False
        self.index = index
    def finishtime(self):
        return self.starttime + oneProcessMaterialtime



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
waitlist = [cnc2,cnc1,cnc4,cnc3,cnc6,cnc5,cnc8,cnc7]

while 1:
    minDistance = 3
    closestCNC = []
    # 遍历所有cnc， 保存最近的空闲cnc位置
    for cnc in waitlist:
        # 检测工作状态
        if cnc.working == False:
            # 检测最短距离
            if RGV.distance(cnc) <= minDistance:
                minDistance = RGV.distance(cnc)
                closestCNC =[cnc]

    # 如果有空闲的cnc
    if closestCNC != []:
        closestCNC = closestCNC[0]
        MtlCount += 1
        # 移动RGV到最近的空闲cnc位置
        RGV.move(closestCNC.position)
        print('上第', MtlCount, '个料','给:',closestCNC.position ,',开始时间：', timePassed)
        # 给空闲cnc上料
        if closestCNC.isOdd == True:
            writer.writerow(['开始上料', closestCNC.index, timePassed])
            RGV.addMtl_odd(closestCNC)
        if closestCNC.isOdd == False:
            writer.writerow(['开始上料', closestCNC.index, timePassed])
            RGV.addMtl_even(closestCNC)
        print('上料结束时间：', timePassed)

    # 如果没有空闲的cnc
    if closestCNC == []:
        finishedCNCs = []
        # 检测是否有已完成的CNC
        for cnc in waitlist:
            if timePassed >= cnc.finishtime():
                finishedCNCs.append(cnc)
        # 如果有已经完成等待换料的CNC
        if finishedCNCs != []:
            print('有已完成的CNC')
            # 初始化检测数据
            closestCNC = finishedCNCs[0]
            minDistance = RGV.distance(finishedCNCs[0])
            # 寻找最近的已完成的CNC
            for cnc in finishedCNCs:
                if RGV.distance(cnc) < minDistance:
                    minDistance = RGV.distance(cnc)
                    closestCNC = cnc
            print('最近的已完成CNC是:', closestCNC.index)
            # 移动到最近的需要换料的CNC处
            RGV.move(closestCNC.position)
            print('使用了最近匹配法')
            # 进行换料
            if closestCNC.isOdd == True:
                writer.writerow(['开始换料', closestCNC.index, timePassed])
                RGV.rmvMtl_odd(closestCNC)
            if closestCNC.isOdd == False:
                writer.writerow(['开始换料', closestCNC.index, timePassed])
                RGV.rmvMtl_even(closestCNC)
            if timePassed >= 38800:
                break
            continue

        # 没有已经完成的CNC
        print('没有已完成CNC')
        minFinishtime = waitlist[0].finishtime()
        quickestCNC = [waitlist[0]]
        # 遍历所有cnc，保存最先完成的cnc位置
        for cnc in waitlist:
            if cnc.finishtime() <= minFinishtime:
                minFinishtime = cnc.finishtime()
                quickestCNC = [cnc]
        quickestCNC = quickestCNC[0]
        # RGV移动到最先完成的CNC处
        RGV.move(quickestCNC.position)
        # 判断是否需要等待
        if timePassed < quickestCNC.finishtime():
            print('需等待：', quickestCNC.finishtime() - timePassed)
            timePassed +=  quickestCNC.finishtime() - timePassed

        print('开始换料时间:', timePassed)
        # 执行换料操作
        if quickestCNC.isOdd == True:
            writer.writerow(['开始换料', quickestCNC.index, timePassed])
            RGV.rmvMtl_odd(quickestCNC)
        if quickestCNC.isOdd == False:
            writer.writerow(['开始换料', quickestCNC.index, timePassed])
            RGV.rmvMtl_even(quickestCNC)
        print('下料结束时间:', timePassed)
    if timePassed >= 28800:
        break
