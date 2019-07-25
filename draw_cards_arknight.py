# author:ietar
# contact me at 410473517@qq.com
# 明日方舟模拟抽卡器 调用draw()抽1次 draw(10)则为10次 10次触发保底
# 也可以draw()其他次数 但只有10次时触发保底
# 很明显 还有其他功能正在写
# 写类时稍微检查了输入 抽卡模拟没怎么照顾这个=.=
# 该寻访为双up 能天使 推进之王各25% 我在想peach?
import random

typedict = {0:'先锋', 1:'近卫', 2:'狙击', 3:'医疗', 4:'术士',\
            5:'特种', 6:'重装', 7:'辅助'}
RATE = {6:0.02, 5:0.08, 4:0.4, 3:0.5, 2:0, 1:0}
pool = []


class Official(object):
    '''明日方舟干员
Official((str)name, (int)stars, uprate=0[, (int)otype])'''
    
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
        elif len(value)>12:
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
        self._rate = RATE[self._stars]

    @property
    def otype(self):
        return self._otype

    @otype.setter
    def otype(self, value):
        if not isinstance(value, str):
            raise TypeError("otype should be str!")
        elif value not in typedict.values():
            raise ValueError("unvalid otype!not in typedict.values().")
        self._otype = value

    @property
    def uprate(self):
        return self._uprate

    @uprate.setter
    def uprate(self, value):
        if not isinstance(value, float):
            raise TypeError("uprate should be float!")
        elif value >= 1 or value <= 0:
            raise ValueError("uprate should be in [0, 1].")
        self._uprate = value

    def info(self):
        return '{} {}星干员 {} uprate:{}'.format(\
            self._name, self._stars, self._otype, self._uprate)

    def __str__(self):
        return self._name

    __repr__ = __str__


def addo(*args):
    pool.append(Official(*args))
    
def draw(times=1):
    
    pool6 = {}
    pool5 = {}
    pool4 = {}
    pool3 = {}
    count6, count5, count4, count3 = 0, 0, 0, 0
    # 分别对应6, 5, 4, 3星 干员出货数量
    ratemax6, ratemax5, ratemax4, ratemax3 = 1, 1, 1, 1
    nonup6, nonup5, nonup4, nonup3 = 0, 0, 0, 0
    # 分别对应6, 5, 4, 3星 非up干员数量
    res = []
    #初始化完成
    
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
    # 将干员按星级加入对应池子 完成
    
    # if干员的uprate不为0 将其直接设为权重
    # else 使其平分剩下的rate 分的人数+1

    # nweight == normal weight
    nweight6 = ratemax6/nonup6
    nweight5 = ratemax5/nonup5
    nweight4 = ratemax4/nonup4
    nweight3 = ratemax3/nonup3

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
    # 这里uprate的处理还有问题 加起来不等于1 待处理
    # 处理完成
    
    # test
    # print(pool6,pool5,pool4,pool3,sep='\n')
    for _ in range(times):
        a = random.random()
        if a <= RATE[6]:
            out = random.choices(list(pool6.keys()),list(pool6.values()))[0]
            res.append(out)
            count6+=1
        elif a <= RATE[5]:
            out = random.choices(list(pool5.keys()),list(pool5.values()))[0]
            res.append(out)
            count5+=1
        elif a <= RATE[4]:
            out = random.choices(list(pool4.keys()),list(pool4.values()))[0]
            res.append(out)
            count4+=1
        else:
            out = random.choices(list(pool3.keys()),list(pool3.values()))[0]
            res.append(out)
            count3+=1
    # 正式抽卡 完成

    
    # 保底考虑直接重抽10次 只在10连抽时触发 
    if times==10 and not (count6 + count5):
        print("保底机制使您免收紫气东来困扰 1次")
        return draw(10)
    return res

'''addo('推进之王',6,0.25,'先锋')
addo('能天使',6,0.25,'狙击')
addo('星熊',6)
addo('闪灵',6)
addo('伊芙利特',6)
addo('塞雷娅',6)
addo('银灰',6)
addo('夜莺',6)
addo('艾雅法拉',6)
addo('安洁莉娜',6)
addo('斯卡蒂',6)
addo('杜宾',4)
addo('深海色',4)
addo('白雪',4)
addo('芬',3)
addo('克洛丝',3)
addo('炎熔',3)
# 慢慢加干员就是了'''

Official6 = r"推进之王/能天使/星熊/闪灵/伊芙利特/塞雷娅/\
银灰/夜莺/艾雅法拉/安洁莉娜/斯卡蒂"
Official5 = r"白面鸮/幽灵鲨/芙兰卡/\
德克萨斯/凛冬/蓝毒/普罗旺斯/临光/红/\
赫默/雷蛇/夜魔/天火/初雪/拉普兰德/华法琳/\
守林人/狮蝎/真理/陨星/白金/梅尔/可颂/崖心/食铁兽/空"
Official4 = r"杜宾/深海色/白雪/远山/夜烟/流星/\
蛇屠箱/末药/猎蜂/慕斯/砾/暗索/地灵/调香师/霜叶/\
清道夫/角峰/古米/缠丸/阿消/红豆/杰西卡"
Official3 = r"芬/克洛丝/炎熔/米格鲁/芙蓉/\
卡缇/史都华德/香草/玫兰莎/安赛尔/梓兰/翎羽/空爆/月见夜"

for i in Official6.split(r'/'):
    addo(i,6)
for i in Official5.split(r'/'):
    addo(i,5)
for i in Official4.split(r'/'):
    addo(i,4)
for i in Official3.split(r'/'):
    addo(i,3)
# 不行 太蠢了 程序员就得用程序员的手法
# 字符串来自http://wiki.joyme.com/arknights/干员寻访模拟器

while 1:
    user_input = input("输入抽卡数量(或q退出),建议直接回车开启带保底的10连:") or '10'
    if user_input == 'q':
        break
    try:
        numbers = int(user_input)
    except ValueError:
        print("输入的不是整型,不太好抽啊")
        continue
    if numbers not in range(0,1001):
        print("亲亲建议您输入0-1000的数量呢(呕)")
        continue
    print('\n')
    print(draw(numbers),'\n')



        

        
