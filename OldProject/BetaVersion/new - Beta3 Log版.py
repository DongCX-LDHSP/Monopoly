import pygame
import sys
from pygame.locals import *
from random import randint


# 角色
class PC:
    def __init__(self, name, image):
        self.name = name
        self.position = 0   # 初始位置
        self.money = 1000   # 初始资金
        self.image = image   # 外观图片
        self.transportation = "无"    # 装备
        self.status = "正常"    # 状态
        self.engine = 0     # 每回合额外移动一格，需激活
        self.chance = False     # 互换资金的机会，需激活
        self.item = "无"    # 持有道具
        self.ill = 0        # 生病冷却，需激活
        self.wind = False   # 传送冷却，需激活
        self.free = False   # 免费冷却，需激活
        self.messageBoardLocation = [(5 * 25, 4 * 25 + 12), (5 * 25, 8 * 25)]

    def move(self):
        file.write("\nPC进入move函数\n")
        if self.status == "监禁":
            self.status = "保释"
            return
        elif self.status == "保释":
            self.status = "正常"

        # 掷骰子
        roll = randint(1, 6) if self.transportation == "无" else randint(2, 12)

        if self.ill > 0:
            roll = roll // 2    # 感冒移动速度减半
            if roll == 0:
                roll = 1
            self.ill -= 1
            if self.ill == 0:
                self.status = "正常"
            file.write("PC因疾病移动速度减半\n")
        if self.wind is True:
            roll = randint(1, 50)   # 遭遇大风，随机落地
            self.wind = not self.wind
            file.write("PC遭遇大风，随机落地\n")

        # 坐标变化
        if self.position + roll < 50:
            self.position += roll
        else:
            self.position = self.position + roll - 50
            self.money += 300   # 绕地图一圈奖励
        file.write("PC移动了" + str(roll) + "格\n\n")

    def display(self, Ls):
        self.__display_base()
        self.__display_incidents(Ls.lands, Ls.incidents)

    def __display_base(self):
        # 准备工作
        messages = list()
        for i in range(3):
            messages.append(list())
        messages[0].append(font.render("昵称: %s" % self.name, True, [0, 0, 0]))
        messages[0].append(font.render("坐标: %d" % self.position, True, [0, 0, 0]))
        messages[1].append(font.render("状态: %s" % self.status, True, [0, 0, 0]))
        messages[1].append(font.render("装备: %s" % self.transportation, True, [0, 0, 0]))
        messages[2].append(font.render("物品: %s" % self.item, True, [0, 0, 0]))
        messages[2].append(font.render("资金: %d金币" % self.money, True, [0, 0, 0]))
        # 信息输出
        for i in range(len(messages)):
            for j in range(len(messages[i])):
                screen.blit(messages[i][j],
                            (self.messageBoardLocation[0][0] + j * 25 * 6,
                             self.messageBoardLocation[0][1] + i * 25))

    def __display_incidents(self, L, incidents):
        # 准备工作
        messages = list()
        location = self.position
        # 购买或升级地块
        if L[location].owner != "事件":
            level = L[location].level
            if L[location].owner == "系统":
                messages.append(font.render("这里是一片无主的荒地", True, [0, 0, 255]))
                messages.append(font.render("按B键花费%d金币建立城堡" % ((level + 1) * 100), True, [0, 0, 255]))
                if self.free is True:
                    messages.append(font.render("你可以免费建立城堡（仅限一次）", True, [0, 0, 255]))
            elif L[location].owner == self.name:
                messages.append(font.render("城墙上的卫兵向你举旗致敬", True, [0, 0, 255]))
                if L[location].level < 5:
                    messages.append(font.render("按B键花费%d金币升级城堡" % ((level + 1) * 100), True, [0, 0, 255]))
                    if self.free is True:
                        messages.append(font.render("你可以免费升级城堡（仅限一次）", True, [0, 0, 255]))
                else:
                    messages.append(font.render("城堡已经很豪华了！", True, [0, 0, 255]))
            else:
                messages.append(font.render("高耸的城堡阴沉地矗立于前方", True, [0, 0, 255]))
                messages.append(font.render("你到了别人的地盘，不得不支付%d金币过路费" % (level * 100), True, [0, 0, 255]))
                # 炸药使用提示
                if self.item == "炸药":
                    messages.append(font.render("按B键使用炸药炸毁城堡", True, [0, 0, 255]))
        # 事件0：到达起点
        elif L[location].incident == incidents[0]:
            messages.append(font.render("事件：你到达了起点", True, [0, 0, 255]))
        # 事件1: 到达马场
        elif L[location].incident == incidents[1]:
            messages.append(font.render("事件：你来到了马场", True, [0, 0, 255]))
            # 走路状态想买马
            if self.transportation == "无":
                messages.append(font.render("按B键花费1000金币购买一匹战马", True, [0, 0, 255]))
                messages.append(font.render("现在你以双倍速度进行移动！", True, [0, 0, 255]))
            # 买了马想升级
            elif self.transportation == "战马":
                messages.append(font.render("按B键花费2000金币将战马升级为千里马", True, [0, 0, 255]))
                messages.append(font.render("骑上千里马的你可以进行额外行动！", True, [0, 0, 255]))
                messages.append(font.render("按A键向前一格，按D键向后一格", True, [0, 0, 255]))
            # 战马升级完毕
            elif self.transportation == "千里马":
                messages.append(font.render("这里已经没有值得购买的好马了", True, [0, 0, 255]))
                messages.append(font.render("你失望地离开了马场", True, [0, 0, 255]))
        # 事件2：遭遇小偷
        elif L[location].incident == incidents[2]:
            messages.append(font.render("事件：走在大街上的你遇到了小偷", True, [0, 0, 255]))
            if self.transportation == "无":
                messages.append(font.render("你失去了500金币", True, [0, 0, 255]))
            else:
                messages.append(font.render("幸运的是，骑在马上的你没有成为小偷的目标", True, [0, 0, 255]))
        # 事件3：逮捕入狱
        elif L[location].incident == incidents[3]:
            if self.status == "正常" or self.status == "监禁":
                messages.append(font.render("事件: 你被卷入一场谋杀案，暂时无法脱身", True, [0, 0, 255]))
                messages.append(font.render("你本回合无法移动", True, [0, 0, 255]))
            elif self.status == "保释":
                messages.append(font.render("事件: 你已被保释，本回合将正常移动", True, [0, 0, 255]))
            elif self.status == "感冒":
                messages.append(font.render("事件: 你因生病而在医院修养，渡过了平静的一天", True, [0, 0, 255]))
                messages.append(font.render("你幸运地避开了谋杀案的牵连", True, [0, 0, 255]))
        # 事件4：资金互换
        elif L[location].incident == incidents[4]:
            messages.append(font.render("事件: 你碰巧获得了一个与他人互换财富的机会", True, [0, 0, 255]))
            messages.append(font.render("按B键与敌人互换资金", True, [0, 0, 255]))
        # 事件5：获得炸药
        elif L[location].incident == incidents[5]:
            messages.append(font.render("事件: 你在路边捡到了炼金术士丢弃的炸药", True, [0, 0, 255]))
            messages.append(font.render("在敌人的城堡中按B键使用炸药，仅限一次", True, [0, 0, 255]))
        # 事件6：资产暴增
        elif L[location].incident == incidents[6]:
            messages.append(font.render("事件: 你在山间偶然发现了一座金矿", True, [0, 0, 255]))
            messages.append(font.render("你得到了1000金币", True, [0, 0, 255]))
        # 事件7：生病
        elif L[location].incident == incidents[7]:
            messages.append(font.render("事件: 你发现自己得了感冒，还好病得不算严重", True, [0, 0, 255]))
            messages.append(font.render("你在三回合内的移动速度减半", True, [0, 0, 255]))
        # 事件8：遭遇大风
        elif L[location].incident == incidents[8]:
            messages.append(font.render("事件:你被一阵狂风卷起，身不由己地飞了起来", True, [0, 0, 255]))
            messages.append(font.render("你下次移动后将在随机位置出现", True, [0, 0, 255]))
        # 事件9：领主结好
        elif L[location].incident == incidents[9]:
            messages.append(font.render("事件:你与本地领主建立友谊，得到了他的承诺", True, [0, 0, 255]))
            messages.append(font.render("你下次修建或升级城堡完全免费", True, [0, 0, 255]))
        # 信息输出
        for i in range(len(messages)):
            screen.blit(messages[i], (self.messageBoardLocation[1][0], self.messageBoardLocation[1][1] + i * 25))

    def buy(self, L):
        file.write("\nPC进入buy函数\n")
        location = self.position
        # 购买地块
        price = L[location].price(self.name)
        if price != 0:
            self.money -= price if self.free is False else 0
            self.free = not self.free if self.free is True else self.free
            L[location].changeProperty(self.name)
            file.write("PC花费" + str(price) + "购买或升级了房屋\n\n")
        # 买马以及升级
        elif L[location].incident == "马场":
            if self.money > 1000 and self.transportation == "无":
                self.money -= 1000
                self.transportation = "战马"
                file.write("PC购买了战马\n\n")
            elif self.money > 2000 and self.transportation == "战马":
                self.money -= 2000
                self.transportation = "千里马"
                file.write("PC购买了千里马\n\n")
                self.engine = 1

    def incidents(self, Ls):
        L = Ls.lands
        incidents = Ls.incidents
        location = self.position
        # 1.路过敌人房子
        if L[location].owner != self.name and L[location].owner != "事件" and L[location].owner != "系统":
            self.money -= L[location].level * 100
            file.write("PC路过NPC房子，付了租金" + str(L[location].level * 100) + "金币\n")
            return L[location].level * 100
        # 特殊事件房间
        elif L[location].owner == "事件":
            # 2.遭遇小偷
            if L[location].incident == incidents[2] and self.transportation == "无":
                self.money -= 500
                file.write("PC遭遇小偷，损失了500金币\n")
            # 3.被囚禁
            elif L[location].incident == incidents[3]:
                if self.status != "保释":
                    self.status = "监禁"
                    file.write("PC被监禁了\n")
                elif self.status == "保释":
                    file.write("PC被保释了\n")
            # 4.资金互换
            elif L[location].incident == incidents[4]:
                self.chance = True
            # 5.炸药
            elif L[location].incident == incidents[5]:
                self.item = "炸药"
            # 6.捡钱
            elif L[location].incident == incidents[6]:
                self.money += 1000
                file.write("PC到达了金矿，获得了1000金币\n")
            # 7.生病
            elif L[location].incident == incidents[7]:
                self.status = "感冒"
                self.ill = 3
                file.write("PC住院了，3个回合内速度减半\n")
            # 8.传送
            elif L[location].incident == incidents[8]:
                self.wind = True
            # 9.免费
            elif L[location].incident == incidents[9]:
                self.free = True
                file.write("PC与当地领主结好，获得了免费修建或升级城堡的承诺\n")
        return 0


class NPC:
    def __init__(self, name, image):
        self.name = name
        self.position = 0   # 初始位置
        self.money = 1000   # 初始资金
        self.image = image   # 外观图片
        self.houseCounter = [0, 0, 0, 0, 0]
        self.transportation = "无"    # 装备
        self.status = "正常"    # 状态
        self.engine = 0     # 每回合额外移动一格，需激活
        self.chance = False     # 互换资金的机会，需激活
        self.item = "无"    # 持有道具
        self.ill = 0        # 生病冷却，需激活
        self.wind = False   # 传送冷却，需激活
        self.free = False   # 免费冷却，需激活
        self.cheat = [0, 0, 0]
        self.messageBoardLocation = [(27 * 25, 4 * 25 + 12), (27 * 25, 8 * 25)]

    def move(self):
        file.write("\nNPC进入了move函数\n")
        if self.status == "监禁":
            self.status = "保释"
            return
        elif self.status == "保释":
            self.status = "正常"

        # 掷骰子
        roll = randint(1, 6) if self.transportation == "无" else randint(2, 12)

        if self.ill > 0:
            roll = roll // 2    # 感冒移动速度减半
            if roll == 0:
                roll = 1
            self.ill -= 1
            if self.ill == 0:
                self.status = "正常"
            file.write("NPC因生病移动速度减半\n")
        if self.wind is True:
            roll = randint(1, 50)   # 遭遇大风，随机落地
            self.wind = not self.wind
            file.write("NPC因遭遇大风，将随机落地\n")

        # 坐标变化
        if self.position + roll < 50:
            self.position += roll
        else:
            self.position = self.position + roll - 50
            self.money += 300   # 绕地图一圈奖励
        file.write("NPC移动了" + str(roll) + "格\n\n")

    def check(self):
        if self.cheat[0] * self.cheat[1] * self.cheat[2] == 1:
            return True
        return False

    def display(self, Ls):
        if self.check() is True:
            self.__display_base()
            self.__display_incidents(Ls.lands, Ls.incidents)
        else:
            screen.blit(font.render("依次按下DWQ进入开发者模式", True, [0, 0, 255]), (27 * 25, 7 * 25))
            screen.blit(font.render("查看NPC的状态", True, [0, 0, 255]), (27 * 25, 8 * 25))

    def __display_base(self):
        # 准备工作
        messages = list()
        for i in range(3):
            messages.append(list())
        messages[0].append(font.render("昵称: %s" % self.name, True, [0, 0, 0]))
        messages[0].append(font.render("坐标: %d" % self.position, True, [0, 0, 0]))
        messages[1].append(font.render("状态: %s" % self.status, True, [0, 0, 0]))
        messages[1].append(font.render("装备: %s" % self.transportation, True, [0, 0, 0]))
        messages[2].append(font.render("物品: %s" % self.item, True, [0, 0, 0]))
        messages[2].append(font.render("资金: %d金币" % self.money, True, [0, 0, 0]))
        # 信息输出
        for i in range(len(messages)):
            for j in range(len(messages[i])):
                screen.blit(messages[i][j],
                            (self.messageBoardLocation[0][0] + j * 25 * 6,
                             self.messageBoardLocation[0][1] + i * 25))

    def __display_incidents(self, L, incidents):
        # 准备工作
        messages = list()
        location = self.position
        # 购买或升级地块
        if L[location].owner != "事件":
            level = L[location].level
            if L[location].owner == "系统":
                messages.append(font.render("这里是一片无主的荒地", True, [0, 0, 255]))
                messages.append(font.render("花费%d金币建立城堡" % ((level + 1) * 100), True, [0, 0, 255]))
                if self.free is True:
                    messages.append(font.render("你可以免费建立城堡（仅限一次）", True, [0, 0, 255]))
            elif L[location].owner == self.name:
                messages.append(font.render("城墙上的卫兵向你举旗致敬", True, [0, 0, 255]))
                if L[location].level < 5:
                    messages.append(font.render("花费%d金币升级城堡" % ((level + 1) * 100), True, [0, 0, 255]))
                    if self.free is True:
                        messages.append(font.render("你可以免费升级城堡（仅限一次）", True, [0, 0, 255]))
                else:
                    messages.append(font.render("城堡已经很豪华了！", True, [0, 0, 255]))
            else:
                messages.append(font.render("高耸的城堡阴沉地矗立于前方", True, [0, 0, 255]))
                messages.append(font.render("你到了别人的地盘，不得不支付%d金币过路费" % (level * 100), True, [0, 0, 255]))
                # 炸药使用提示
                if self.item == "炸药":
                    messages.append(font.render("使用炸药炸毁城堡", True, [0, 0, 255]))
        # 事件0：到达起点
        elif L[location].incident == incidents[0]:
            messages.append(font.render("事件：你到达了起点", True, [0, 0, 255]))
        # 事件1: 到达马场
        elif L[location].incident == incidents[1]:
            messages.append(font.render("事件：你来到了马场", True, [0, 0, 255]))
            # 走路状态想买马
            if self.transportation == "无":
                messages.append(font.render("花费1000金币购买一匹战马", True, [0, 0, 255]))
                messages.append(font.render("现在你以双倍速度进行移动！", True, [0, 0, 255]))
            # 买了马想升级
            elif self.transportation == "战马":
                messages.append(font.render("花费2000金币将战马升级为千里马", True, [0, 0, 255]))
                messages.append(font.render("骑上千里马的你可以进行额外行动！", True, [0, 0, 255]))
            # 战马升级完毕
            elif self.transportation == "千里马":
                messages.append(font.render("这里已经没有值得购买的好马了", True, [0, 0, 255]))
                messages.append(font.render("你失望地离开了马场", True, [0, 0, 255]))
        # 事件2：遭遇小偷
        elif L[location].incident == incidents[2]:
            messages.append(font.render("事件：走在大街上的你遇到了小偷", True, [0, 0, 255]))
            if self.transportation == "无":
                messages.append(font.render("你失去了500金币", True, [0, 0, 255]))
            else:
                messages.append(font.render("幸运的是，骑在马上的你没有成为小偷的目标", True, [0, 0, 255]))
        # 事件3：逮捕入狱
        elif L[location].incident == incidents[3]:
            if self.status == "正常" or self.status == "监禁":
                messages.append(font.render("事件: 你被卷入一场谋杀案，暂时无法脱身", True, [0, 0, 255]))
                messages.append(font.render("你本回合无法移动", True, [0, 0, 255]))
            elif self.status == "保释":
                messages.append(font.render("事件: 你已被保释，本回合将正常移动", True, [0, 0, 255]))
            elif self.status == "感冒":
                messages.append(font.render("事件: 你因生病而在医院修养，渡过了平静的一天", True, [0, 0, 255]))
                messages.append(font.render("你幸运地避开了谋杀案的牵连", True, [0, 0, 255]))
        # 事件4：资金互换
        elif L[location].incident == incidents[4]:
            messages.append(font.render("事件: 你碰巧获得了一个与他人互换财富的机会", True, [0, 0, 255]))
        # 事件5：获得炸药
        elif L[location].incident == incidents[5]:
            messages.append(font.render("事件: 你在路边捡到了炼金术士丢弃的炸药", True, [0, 0, 255]))
            messages.append(font.render("在敌人的城堡中使用炸药，仅限一次", True, [0, 0, 255]))
        # 事件6：资产暴增
        elif L[location].incident == incidents[6]:
            messages.append(font.render("事件: 你在山间偶然发现了一座金矿", True, [0, 0, 255]))
            messages.append(font.render("你得到了1000金币", True, [0, 0, 255]))
        # 事件7：生病
        elif L[location].incident == incidents[7]:
            messages.append(font.render("事件: 你发现自己得了感冒，还好病得不算严重", True, [0, 0, 255]))
            messages.append(font.render("你在三回合内的移动速度减半", True, [0, 0, 255]))
        # 事件8：遭遇大风
        elif L[location].incident == incidents[8]:
            messages.append(font.render("事件:你被一阵狂风卷起，身不由己地飞了起来", True, [0, 0, 255]))
            messages.append(font.render("你下次移动后将在随机位置出现", True, [0, 0, 255]))
        # 事件9：领主结好
        elif L[location].incident == incidents[9]:
            messages.append(font.render("事件:你与本地领主建立友谊，得到了他的承诺", True, [0, 0, 255]))
            messages.append(font.render("你下次修建或升级城堡完全免费", True, [0, 0, 255]))
        # 信息输出
        for i in range(len(messages)):
            screen.blit(messages[i], (self.messageBoardLocation[1][0], self.messageBoardLocation[1][1] + i * 25))

    def buy(self, L):
        file.write("\nNPC进入buy函数\n")
        location = self.position
        if self.money > 500 or self.free is True:
            # 购买及升级地块
            price = L[location].price(self.name)
            if price != 0:
                level = L[location].level
                if level == 0 or self.free or (level == 1 and self.houseCounter[0] > 15) or \
                  (level == 2 and self.houseCounter[1] > 10) or (level == 3 and self.houseCounter[2] > 7) or level >= 4:
                    self.houseCounter[L[location].level] += 1
                    self.money -= price if self.free is False else 0
                    self.free = not self.free if self.free is True else self.free
                    L[location].changeProperty(self.name)
                    file.write("NPC花费" + str(price) + "购买或升级了房屋\n\n")
            # 买马以及升级
            elif L[location].incident == "马场":
                if self.money > 1600 and self.transportation == "无":
                    self.money -= 1000
                    self.transportation = "战马"
                    file.write("NPC购买了战马\n")
                elif self.money > 2600 and self.transportation == "战马":
                    self.money -= 2000
                    self.transportation = "千里马"
                    file.write("NPC购买了千里马\n")
                    self.engine = 1

    def incidents(self, Ls):
        L = Ls.lands
        incidents = Ls.incidents
        location = self.position
        # 1.路过敌人房子
        if L[location].owner != self.name and L[location].owner != "事件" and L[location].owner != "系统":
            self.money -= L[location].level * 100
            file.write("NPC路过了PC的房子，付了租金" + str(L[location].level * 100) + "金币\n")
            return L[location].level * 100
        # 特殊事件房间
        elif L[location].owner == "事件":
            # 2.遭遇小偷
            if L[location].incident == incidents[2] and self.transportation == "无":
                self.money -= 500
                file.write("NPC遭遇小偷，损失了500金币\n")
            # 3.被囚禁
            elif L[location].incident == incidents[3]:
                if self.status != "保释":
                    self.status = "监禁"
                    file.write("NPC被监禁了\n")
                elif self.status == "保释":
                    file.write("NPC被保释了\n")
            # 4.资金互换
            elif L[location].incident == incidents[4]:
                self.chance = True
            # 5.炸药
            elif L[location].incident == incidents[5]:
                self.item = "炸药"
            # 6.捡钱
            elif L[location].incident == incidents[6]:
                self.money += 1000
                file.write("NPC到达了金矿，获得了1000金币\n")
            # 7.生病
            elif L[location].incident == incidents[7]:
                self.status = "感冒"
                self.ill = 3
                file.write("NPC因住院3回合内的移动速度减半\n")
            # 8.传送
            elif L[location].incident == incidents[8]:
                self.wind = True
            # 9.免费
            elif L[location].incident == incidents[9]:
                self.free = True
                file.write("NPC与当地领主结好，获得了免费修建或升级城堡的承诺\n")
        return 0


class landmasses:
    def __init__(self, PCName, NPCName):
        self.cattleOfPC = list()
        self.cattleOfNPC = list()
        self.wasteland = pygame.image.load("./source/wasteland.png")
        self.incidents = ["起点", "马场", "小偷", "监狱", "资金互换", "炸药", "资产暴增", "感冒", "大风", "领主"]
        self.lands = list()
        self.PCName = str(PCName)
        self.NPCName = str(NPCName)

        self.cattleOfPC.append(self.wasteland)
        self.cattleOfPC.append(pygame.image.load("./source/houseA1.png"))
        self.cattleOfPC.append(pygame.image.load("./source/houseA2.png"))
        self.cattleOfPC.append(pygame.image.load("./source/houseA3.png"))
        self.cattleOfPC.append(pygame.image.load("./source/houseA4.png"))
        self.cattleOfPC.append(pygame.image.load("./source/houseA5.png"))

        self.cattleOfNPC.append(self.wasteland)
        self.cattleOfNPC.append(pygame.image.load("./source/houseB1.png"))
        self.cattleOfNPC.append(pygame.image.load("./source/houseB2.png"))
        self.cattleOfNPC.append(pygame.image.load("./source/houseB3.png"))
        self.cattleOfNPC.append(pygame.image.load("./source/houseB4.png"))
        self.cattleOfNPC.append(pygame.image.load("./source/houseB5.png"))

        class OneLand:
            def __init__(self, position, image=self.wasteland, owner="系统", incident="无"):
                self.owner = str(owner)
                self.position = position
                self.level = 0
                self.image = image
                self.incident = incident

            def price(self, who):
                if (who == self.owner and self.level < 5) or self.owner == "系统":
                    return (self.level + 1) * 100
                return 0

            def changeProperty(self, who, pcName=self.PCName, cattlePC=self.cattleOfPC, cattleNPC=self.cattleOfNPC):
                self.owner = who
                self.level += 1
                self.incident = who + "的房间"
                if who == pcName:
                    self.image = cattlePC[self.level]
                else:
                    self.image = cattleNPC[self.level]
                file.write(who + "购买或升级了第" + str(self.position) + "地块\n")

            def bang(self, wasteland=self.wasteland):
                self.owner = "系统"
                self.level = 0
                self.image = wasteland
                self.incident = "无"
                file.write("第" + str(self.position) + "地块的城堡被炸毁掉了\n")

        counter = 0
        for i in range(50):
            if (i + 1) % 5 == 1:
                self.lands.append(OneLand(i, owner="事件", incident=self.incidents[counter]))
                counter += 1
            else:
                self.lands.append(OneLand(i))


def location_convert(position):
    position += 1
    if position <= 16:
        return (position - 1) * 75, 0
    if position <= 26:
        return 15 * 75, (position - 16) * 75
    if position <= 41:
        return (15 - (position - 26)) * 75, 10 * 75
    if position <= 50:
        return 0, (9 - (position - 42)) * 75


# 测试代码
file = open("./log.txt", "w")

# pygame初始化
pygame.init()
file.write("Pygame初始化\n")
# 载入图片
icon = pygame.image.load("./source/dog.ico")
start = pygame.image.load("./source/start.png")
gameOver = pygame.image.load("./source/gameover.png")
gameWin = pygame.image.load("./source/gamewin.png")
gameMap = pygame.image.load("./source/map.png")

PCImage = pygame.image.load("./source/PC.png")
PCFixImage = pygame.image.load("./source/PCBeginning.png")
NPCImage = pygame.image.load("./source/NPC.png")
NPCFixImage = pygame.image.load("./source/NPCBeginning.png")
file.write("载入各种图片完成\n")
# 游戏字体
font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 20)
file.write("游戏字体预设完成\n")

# 帧率控制
clock = pygame.time.Clock()
file.write("时钟设置完成\n")
# 窗口初始化
pygame.display.init()
file.write("窗口初始化\n")
try:
    pygame.display.set_icon(icon)
    file.write("设置图标成功\n")
except:
    file.write("设置图标失败\n")
    pass
screen = pygame.display.set_mode((1200, 825))
pygame.display.set_caption("大富翁")
file.write("窗口大小设置及标题完成\n")

# 游戏角色
hero = PC("Naruto", PCImage)
enemy = NPC("Sasuki", NPCImage)
file.write("游戏角色创建完成\n")

# 地块初始化
lands = landmasses(hero.name, enemy.name)
file.write("地块初始化完成\n")

# 开始界面
for i in range(75):
    clock.tick(90)
    screen.blit(gameMap, (0, 0))
    screen.blit(PCFixImage, (6 * 25 + 13 + i * 2 - 10, 6 * 25 + 13 - 10))
    screen.blit(NPCFixImage, (38 * 25 + 13 - i * 2 - 10, 6 * 25 + 13 - 10))
    screen.blit(start, (175, 325))
    pygame.display.update()
file.write("开始动画结束\n")
order = False
while order is False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            file.close()
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                order = True
            if event.key == K_e:
                file.close()
                pygame.quit()
                sys.exit()
file.write("进入游戏界面\n")

# 行动回合
heroTurn, enemyTurn = True, False

# 游戏界面
while True:
    clock.tick(10)      # 帧数
    screen.blit(gameMap, (0, 0))
    # 地块绘制
    for land in lands.lands:
        screen.blit(land.image, location_convert(land.position))
    # 人物绘制
    screen.blit(enemy.image, location_convert(enemy.position))
    screen.blit(hero.image, location_convert(hero.position))
    # 固定位置人物绘制
    screen.blit(PCFixImage, (19 * 25 - 21, 4 * 25))
    screen.blit(NPCFixImage, (41 * 25 - 21, 4 * 25))
    # 信息显示
    hero.display(lands)
    enemy.display(lands)
    # 结束判定
    if hero.money <= 0 or enemy.money <= 0:
        winner = enemy.name if hero.money <= 0 else hero.name
        file.write(winner + "取得了游戏的胜利\n")
        break

    # 按键操作
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            file.write("游戏退出\n")
            file.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # 开发者模式
            if enemy.check() is False:
                if event.key == K_d:
                    enemy.cheat[0] = 1
                if enemy.cheat[0] == 1 and event.key == K_w:
                    enemy.cheat[1] = 1
                if enemy.cheat[1] == 1 and event.key == K_q:
                    enemy.cheat[2] = 1
                    file.write("开发者模式启用\n")
            # 掷骰子
            if heroTurn is True:
                file.write("进入PC的回合\n")
                file.write("坐标：" + str(hero.position) + "\n")
                file.write("资金：" + str(hero.money) + "\n")
                if hero.transportation != "无":
                    file.write("交通工具：" + hero.transportation)
                if hero.status != "正常":
                    file.write("状态：" + hero.status)
                if hero.item != "无":
                    file.write("装备：" + hero.item)
                if hero.free is True:
                    file.write("PC结好")
                if event.key == K_SPACE:
                    hero.move()
                    back = hero.incidents(lands)
                    if back != 0:
                        enemy.money += back
                        file.write("NPC收到了PC的房租" + str(back) + "金币\n")
                    heroTurn, enemyTurn = not heroTurn, not enemyTurn
                    hero.engine = 0
            # 购买地块、交换金钱、使用炸药
            if event.key == K_b:
                if (lands.lands[hero.position].owner != enemy.name and lands.lands[hero.position].owner != "事件")\
                        or lands.lands[hero.position].incident == "马场":
                    hero.buy(lands.lands)
                elif lands.lands[hero.position].incident == "资金互换" and hero.chance is True:
                    temp = hero.money
                    hero.money = enemy.money
                    enemy.money = temp
                    hero.chance = not hero.chance
                    file.write("PC与NPC进行了资金交换\n")
                elif lands.lands[hero.position].owner == enemy.name and hero.item == "炸药":
                    for i in range(lands.lands[hero.position].level):
                        enemy.houseCounter[i] -= 1
                    lands.lands[hero.position].bang()
                    hero.item = "无"
                    file.write("PC使用了炸药，炸毁了NPC的一座城堡\n")
            # 退出游戏
            elif event.key == K_e:
                file.write("游戏退出\n")
                file.close()
                pygame.quit()
                sys.exit()
            # 引擎移动
            if hero.transportation == "千里马":
                if event.key == K_a:        # 后退
                    if hero.engine == 0 or hero.engine == 1:
                        if hero.position > 1:
                            hero.position -= 1
                            hero.engine -= 1
                            file.write("PC使用千里马的技能前进了1格\n")
                elif event.key == K_d:      # 前进
                    if hero.engine == 0 or hero.engine == -1:
                        if hero.position < 50:
                            hero.position += 1
                            hero.engine += 1
                            file.write("PC使用千里马的技能后退了1格\n")

    if enemyTurn is True:
        file.write("进入NPC的回合\n")
        back = enemy.incidents(lands)
        file.write("坐标：" + str(enemy.position) + "\n")
        file.write("资金：" + str(enemy.money) + "\n")
        if enemy.transportation != "无":
            file.write("交通工具：" + enemy.transportation)
        if enemy.status != "正常":
            file.write("状态：" + enemy.status)
        if enemy.item != "无":
            file.write("装备：" + enemy.item)
        if enemy.free is True:
            file.write("NPC结好")
        if back != 0:
            hero.money += back
            file.write("PC收到了NPC的房租" + str(back) + "金币\n")
        if enemy.chance is True and hero.money > enemy.money:
            temp = hero.money
            hero.money = enemy.money
            enemy.money = temp
            enemy.chance = not enemy.chance
            file.write("NPC与PC进行了资金互换\n")
        elif lands.lands[enemy.position].owner == hero.name and enemy.item == "炸药":
            lands.lands[enemy.position].bang()
            enemy.item = "无"
            file.write("NPC使用了炸药炸毁了PC的一座城堡\n")
        enemy.move()
        enemy.buy(lands.lands)
        if enemy.transportation == "千里马" and enemy.money > 900:
            # 利用千里马多买房子
            now = enemy.position
            forward = now + 1 if now < 49 else 0
            backward = now - 1 if now > 0 else 49
            if lands.lands[forward].owner == "系统" or lands.lands[forward].owner == enemy.name:
                enemy.position = forward
                file.write("NPC使用千里马的技能前进了1格\n")
                enemy.buy(lands.lands)
            if lands.lands[backward].owner == "系统" or lands.lands[forward].owner == enemy.name:
                enemy.position = backward
                file.write("NPC使用千里马的技能后退了1格\n")
                enemy.buy(lands.lands)
            enemy.position = now
            file.write("NPC使用千里马的技能回到了原地\n")
        heroTurn, enemyTurn = not heroTurn, not enemyTurn
        enemy.engine = 0

    pygame.display.update()

# 结束界面
if winner == hero.name:
    screen.blit(gameWin, (175, 325))
else:
    screen.blit(gameOver, (175, 325))
file.write("游戏结束图片展示完毕\n")
pygame.display.update()

order = False
while order is False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            file.write("游戏退出\n")
            file.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                order = True

pygame.quit()
file.write("游戏退出\n")
file.close()
