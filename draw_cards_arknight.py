# email: 410473517@qq.com
# 明日方舟模拟抽卡器 调用draw()抽1次 draw10()则为10次 10次触发保底
# 也可以draw()其他次数 但只有10次时触发保底
# 很明显 还有其他功能正在写
# v2.0 模块化 加入了标准池子STANDARD_POOL(无up, 包含限定干员) 自定义up池 池子检查等功能
# v2.1 紧急修复了6星出率过高的bug(由10连保底机制产生)
# v2.2 pep8 修复Official类定义中的几个漏洞
# v2.3 增加了Draw类 将draw()和draw10()封装其中 并增加了6星出率50抽不出后递增功能(与游戏一致)
# 新卡池前10抽必出5星计划鸽了(这个提升也不大) 计划活动开了更新卡池


__author__ = 'ietar'
__version__ = '2.2'

import random

Official6 = ['推进之王', '能天使', '星熊', '闪灵', '伊芙利特', '银灰', '塞雷娅', '夜莺', '艾雅法拉', '陈', '安洁莉娜', '斯卡蒂']
Official5 = ['白面鸮', '幽灵鲨', '芙兰卡', '德克萨斯', '凛冬', '普罗旺斯', '蓝毒', '雷蛇', '临光', '红', '赫默', '夜魔', '天火', '初雪', '拉普兰德', '华法琳',
             '守林人', '狮蝎', '真理', '白金', '陨星', '梅尔', '可颂', '崖心', '空', '食铁兽', '诗怀雅']
Official4 = ['杜宾', '深海色', '白雪', '远山', '夜烟', '流星', '蛇屠箱', '末药', '猎蜂', '慕斯', '砾', '暗索', '地灵', '调香师', '霜叶', '清道夫', '角峰',
             '古米', '缠丸', '阿消', '红豆', '杰西卡']
Official3 = ['芬', '克洛丝', '炎熔', '米格鲁', '芙蓉', '卡缇', '史都华德', '香草', '玫兰莎', '安赛尔', '梓兰', '翎羽', '空爆', '月见夜']


# 干员数据来自http://wiki.joyme.com/arknights/干员寻访模拟器
# 5星也太多了 我没搞错吧


def makepool():
    pool = []

    def addo(**kw):
        """add Official"""
        pool.append(Official(**kw))

    for i in Official6:
        addo(name=i, stars=6)
    for i in Official5:
        addo(name=i, stars=5)
    for i in Official4:
        addo(name=i, stars=4)
    for i in Official3:
        addo(name=i, stars=3)

    return pool


def checkpool(pool):
    """检查池子内各星级up率是否溢出"""
    current = {3: 0, 4: 0, 5: 0, 6: 0}
    for i in pool:
        if i.stars == 6:
            current[6] += i.uprate
        if i.stars == 5:
            current[5] += i.uprate
        if i.stars == 4:
            current[4] += i.uprate
        if i.stars == 3:
            current[3] += i.uprate

    for i in current:
        if current[i] > 1:
            return 0

    return 1


def set_uprate(pool, name, uprate):
    """自定义池子 修改干员up率 重复调用可修改多个 注意每个星级up率之和不能超过1"""

    if uprate > 1 or uprate < 0:
        raise ValueError('up率必须在0-1之间!')
    current = {3: 0, 4: 0, 5: 0, 6: 0}
    stars = 0
    flag = 0
    temp = None
    for i in pool:
        if i.name == name:
            stars = i.stars
            temp = i
            flag = 1
            break

    if not flag:
        raise ValueError('池子中找不到该干员,无法修改up率!')

    assert stars != 0

    for i in pool:
        if i.stars == 6:
            current[6] += i.uprate
        if i.stars == 5:
            current[5] += i.uprate
        if i.stars == 4:
            current[4] += i.uprate
        if i.stars == 3:
            current[3] += i.uprate

    after_update = uprate - temp.uprate + current[stars]
    if after_update > 1:
        raise ValueError('up率设置过高, 当前{}星up率之和为{}'.format(stars, current[stars]))

    temp.uprate = uprate


class Official(object):
    """明日方舟干员
Official((str)name, (int)stars, uprate=0[, (int)otype])"""

    def __init__(self, name, stars, uprate=0, otype=''):
        self._name = name
        self._stars = stars
        self._uprate = uprate
        self._otype = otype

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be string!")
        elif len(value) > 12:
            raise ValueError("The max length of name is 12.")
        self._name = value

    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self, value):
        if not isinstance(value, int):
            raise TypeError("stars should be integer!")
        elif value not in range(1, 7):
            raise ValueError("value should be in range(1,7).")
        self._stars = value

    @property
    def otype(self):
        return self._otype

    @otype.setter
    def otype(self, value):
        typedict = {0: '先锋', 1: '近卫', 2: '狙击', 3: '医疗', 4: '术士', 5: '特种', 6: '重装', 7: '辅助'}
        if not isinstance(value, str):
            raise TypeError("otype should be str!")
        elif value not in typedict.values():
            raise ValueError("invalid otype!not in typedict.values().")
        self._otype = value

    @property
    def uprate(self):
        return self._uprate

    @uprate.setter
    def uprate(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("uprate should be 0 or float!")
        elif value > 1 or value < 0:
            raise ValueError("uprate should be in (0, 1).")
        self._uprate = value

    def info(self):
        return '{} {}星干员 {} uprate:{}'.format(self._name, self._stars, self._otype, self._uprate)

    def __str__(self):
        return self._name

    __repr__ = __str__


STANDARD_POOL = makepool()


class Draw(object):
    def __init__(self):
        self.count_no_6 = 0
        self.count_no_5 = 0
        self.debug = False

    def draw(self, times=1, pool=None):
        if pool is None:
            pool = STANDARD_POOL
        pool6 = {}
        pool5 = {}
        pool4 = {}
        pool3 = {}
        temp6 = 0
        temp5 = 0
        rate = {6: 0.02, 5: 0.08, 4: 0.5, 3: 0.4, 2: 0, 1: 0}
        count6, count5, count4, count3 = 0, 0, 0, 0
        # 分别对应6, 5, 4, 3星 干员出货数量
        ratemax6, ratemax5, ratemax4, ratemax3 = 1, 1, 1, 1
        nonup6, nonup5, nonup4, nonup3 = 0, 0, 0, 0
        # 分别对应6, 5, 4, 3星 非up干员数量
        res = []
        # pool6,5,4,3 = {干员名:同星级内抽取率}
        # 初始化完成

        # if干员的uprate不为0 将其直接设为权重
        # else 使其平分剩下的rate 分的人数+1
        for i in pool:
            if i.stars == 6:
                pool6[i] = i.uprate
                if i.uprate:
                    ratemax6 -= i.uprate
                else:
                    nonup6 += 1
            elif i.stars == 5:
                pool5[i] = i.uprate
                if i.uprate:
                    ratemax5 -= i.uprate
                else:
                    nonup5 += 1
            elif i.stars == 4:
                pool4[i] = i.uprate
                if i.uprate:
                    ratemax4 -= i.uprate
                else:
                    nonup4 += 1
            elif i.stars == 3:
                pool3[i] = i.uprate
                if i.uprate:
                    ratemax3 -= i.uprate
                else:
                    nonup3 += 1

        # nweight == normal weight
        nweight6 = ratemax6 / nonup6
        nweight5 = ratemax5 / nonup5
        nweight4 = ratemax4 / nonup4
        nweight3 = ratemax3 / nonup3

        for i in pool6:
            if not i.uprate:
                pool6[i] = nweight6
        for i in pool5:
            if not i.uprate:
                pool5[i] = nweight5
        for i in pool4:
            if not i.uprate:
                pool4[i] = nweight4
        for i in pool3:
            if not i.uprate:
                pool3[i] = nweight3

        for _ in range(times):
            a = random.random()
            # temp6 += 1
            # temp5 += 1
            self.count_no_5 += 1
            self.count_no_6 += 1

            # 50后6星抽率增加
            if self.count_no_6 > 50:
                rate[6] = 0.02 + 0.02 * (self.count_no_6 - 50)
                rate[5] = (1-rate[6])*0.08/0.98
                rate[4] = (1-rate[6])*0.5/0.98
                rate[3] = (1-rate[6])*0.4/0.98
            else:
                rate = {6: 0.02, 5: 0.08, 4: 0.4, 3: 0.5, 2: 0, 1: 0}
            assert abs(1-(rate[6] + rate[5] + rate[4] + rate[3])) < 0.00001

            if a <= rate[6]:
                out = random.choices(list(pool6.keys()), list(pool6.values()))[0]
                res.append(out)
                count6 += 1
                self.count_no_5 = 0
                self.count_no_6 = 0

            elif a <= rate[5]:
                out = random.choices(list(pool5.keys()), list(pool5.values()))[0]
                res.append(out)
                count5 += 1
                self.count_no_5 = 0

            elif a <= rate[4]:
                out = random.choices(list(pool4.keys()), list(pool4.values()))[0]
                res.append(out)
                count4 += 1

            else:
                out = random.choices(list(pool3.keys()), list(pool3.values()))[0]
                res.append(out)
                count3 += 1
        # 正式抽卡 完成

        # 保底考虑直接重抽10次 只在10连抽时触发
        if times == 10 and not (count6 + count5 + count4):
            # print("保底机制使您免收紫气东来困扰 1次")
            return self.draw(10, pool)
        else:
            self.count_no_5 += temp5
            self.count_no_6 += temp6

            if self.debug:
                print('已有 {} 抽未出6星'.format(self.count_no_6))
                print('已有 {} 抽未出5星'.format(self.count_no_5))
                print(rate)
            return res

    def draw10(self):
        return self.draw(times=10)


if __name__ == '__main__':
    d = Draw()
    mode = input('输入d进入调试模式 输入其他进入用户友好模式:')
    if mode.lower() != 'd':
        while 1:
            user_input = input("输入抽卡数量(或q退出),建议直接回车开启带保底的10连:") or '10'
            if user_input.lower() == 'q':
                break
            try:
                numbers = int(user_input)
            except ValueError:
                print("输入的不是整型,不太好抽啊")
                continue
            if numbers not in range(0, 1001):
                print("亲亲建议您输入0-1000的数量呢(呕)")
                continue
            print('\n')
            print(d.draw(numbers, STANDARD_POOL), '\n')
    else:
        d.debug = True
        print(d.draw())
        print(d.draw10())
        while 1:
            confirm = input('输入q退出 输入其他继续10连:')
            if confirm.lower() == 'q':
                break
            print(d.draw10())
