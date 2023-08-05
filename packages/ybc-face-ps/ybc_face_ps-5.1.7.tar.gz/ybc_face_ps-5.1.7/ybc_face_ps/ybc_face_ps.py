import requests
import json
import base64
import os
import math
import time
from PIL import Image


def _resize_img(filepath,max_size=512000):
    # MAX_FILE_SIZE = max_size
    filesize = os.path.getsize(filepath)
    # if filesize > MAX_FILE_SIZE :
    im = Image.open(filepath)
    src_w = im.size[0]
    src_h = im.size[1]
    dst_w = 460
    dst_h = (src_h/src_w) * 460
    dst_size = dst_w , dst_h
    im.thumbnail(dst_size)
    im.save(filepath)
    return filepath


def meizhuang(filename='', meitype='日系妆-芭比粉'):
    '''人脸美妆'''
    cosmetic_type = meizhuang_type()
    cosmetic = cosmetic_type.index(meitype) + 1
    if not filename:
        return -1
    if cosmetic < 1:
        cosmetic = 1
    if cosmetic > 23:
        cosmetic = 23
    filepath = os.path.abspath(filename)
    filepath = _resize_img(filepath)
    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceCosmetic.php'
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['cosmetic'] = cosmetic
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        new_file = os.path.splitext(filename)[0] +  '_' + str(int(time.time())) + '_meizhuang' + os.path.splitext(filename)[1]
        with open(new_file,'wb') as f:
            f.write(base64.b64decode(res['data']['image']))
        return new_file
    else:
        return -1

def meizhuang_type(flag=1):
    '''获取美妆类型'''
    MEIZHUANG_TYPE = {
    1:'日系妆-芭比粉',
    2:'日系妆-清透',
    3:'日系妆-烟灰',
    4:'日系妆-自然',
    5:'日系妆-樱花粉',
    6:'日系妆-原宿红',
    7:'韩妆-闪亮',
    8:'韩妆-粉紫',
    9:'韩妆-粉嫩',
    10:'韩妆-自然',
    11:'韩妆-清透',
    12:'韩妆-大地色',
    13:'韩妆-玫瑰',
    14:'裸妆-自然',
    15:'裸妆-清透',
    16:'裸妆-桃粉',
    17:'裸妆-橘粉',
    18:'裸妆-春夏',
    19:'裸妆-秋冬',
    20:'主题妆-经典复古',
    21:'主题妆-性感混血',
    22:'主题妆-炫彩明眸',
    23:'主题妆-紫色魅惑',
    }
    if flag == 1:
        return list(MEIZHUANG_TYPE.values())
    else:
        return MEIZHUANG_TYPE

'''人脸变妆'''
def bianzhuang(filename='', biantype='灰姑娘妆'):
    decoration_type = bianzhuang_type()
    decoration = decoration_type.index(biantype) + 1
    if not filename:
        return -1
    if decoration < 1:
        decoration = 1
    if decoration > 22:
        decoration = 22
    filepath = os.path.abspath(filename)
    filepath = _resize_img(filepath)
    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceDecoration.php'
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['decoration'] = decoration
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + '_bianzhuang'+os.path.splitext(filename)[1]
        with open(new_file,'wb') as f:
            f.write(base64.b64decode(res['data']['image']))
        return new_file
    else:
        return -1

def bianzhuang_type(flag=1):
    '''获取美妆类型'''
    BIANZHUANG_TYPE = {
    1:'埃及妆',
    2:'巴西土著妆',
    3:'灰姑娘妆',
    4:'恶魔妆',
    5:'武媚娘妆',
    6:'星光薰衣草',
    7:'花千骨',
    8:'僵尸妆',
    9:'爱国妆',
    10:'小胡子妆',
    11:'美羊羊妆',
    12:'火影鸣人妆',
    13:'刀马旦妆',
    14:'泡泡妆',
    15:'桃花妆',
    16:'女皇妆',
    17:'权志龙',
    18:'撩妹妆',
    19:'印第安妆',
    20:'印度妆',
    21:'萌兔妆',
    22:'大圣妆'
    }
    if flag == 1:
        return list(BIANZHUANG_TYPE.values())
    else:
        return BIANZHUANG_TYPE

def ronghe(filename='', rongtype='元气新春'):

    '''人脸融合'''
    if not filename:
        return -1
    model_type = ronghe_type()
    model = model_type.index(rongtype) + 1
    if model < 1:
        model = 1
    if model > 10:
        model = 10

    filepath = os.path.abspath(filename)
    filepath = _resize_img(filepath)
    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceMerge.php'
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['model'] = model
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) +  '_ronghe' + '.png'
        with open(new_file,'wb') as f:
            f.write(base64.b64decode(res['data']['image']))
        return _resize_img(new_file)
    else:
        return -1

def __ronghe_type(flag=1):
    RONGHE_TYPE = {
	1: '奇迹',
	2: '压岁钱',
	3: '范蠡',
	4: '李白',
	5: '孙尚香',
	6: '花无缺',
	7: '西施',
	8: '杨玉环',
	9: '白浅',
	10: '凤九',
	11: '夜华',
	12: '年年有余',
	13: '新年萌萌哒',
	14: '王者荣耀荆轲',
	15: '王者荣耀李白',
	16: '王者荣耀哪吒',
	17: '王者荣耀王昭君',
	18: '王者荣耀甄姬',
	19: '王者荣耀诸葛亮',
	20: '赵灵儿',
	21: '李逍遥',
	22: '爆炸头',
	23: '村姑',
	24: '光头',
	25: '呵呵哒',
	26: '肌肉',
	27: '肉山',
	28: '机智',
	29: '1927年军装（男）',
	30: '1927年军装（女）',
	31: '1929年军装（男）',
	32: '1929年军装（女）',
	33: '1937年军装（男）',
	34: '1937年军装（女）',
	35: '1948年军装（男）',
	36: '1948年军装（女）',
	37: '1950年军装（男）',
	38: '1950年军装（女）',
	39: '1955年军装（男）',
	40: '1955年军装（女）',
	41: '1965年军装（男）',
	42: '1965年军装（女）',
	43: '1985年军装（男）',
	44: '1985年军装（女）',
	45: '1987年军装（男）',
	46: '1987年军装（女）',
	47: '1999年军装（男）',
	48: '1999年军装（女）',
	49: '2007年军装（男）',
	50: '2007年军装（女）'
    }
    if flag == 1:
        return list(RONGHE_TYPE.values())
    else:
        return RONGHE_TYPE

def ronghe_type(flag=1):
    RONGHE_TYPE = {
	1: '元气新春',
	2: '岁岁烟火',
	3: '夜华',
	4: '李白',
	5: '凤九',
	6: '白浅',
	7: '侠客',
	8: '爆炸头',
	9: '机智',
	10: '村姑'
    }
    if flag == 1:
        return list(RONGHE_TYPE.values())
    else:
        return RONGHE_TYPE

def datoutie(filename='', sticker='NewDay'):
    '''制作大头贴'''
    if not filename:
        return -1
    sticker_type = datoutie_type()
    sticker = sticker_type.index(sticker) + 1
    if sticker < 1:
        sticker = 1
    if sticker > 31:
        sticker = 31
    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceSticker.php'
    filepath = os.path.abspath(filename)
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['sticker'] = sticker
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + '_datoutie'+os.path.splitext(filename)[1]
        with open(new_file,'wb') as f:
            f.write(base64.b64decode(res['data']['image']))
        return new_file
    else:
        return -1

'''返回大头贴背景类型'''
def datoutie_type(flag=1):
    STICKER_TYPE = {
    1:	'NewDay',
    2:	'欢乐球吃球1:',
    3:	'Bonvoyage',
    4:	'Enjoy',
    5:	'ChickenSpring',
    6:	'ChristmasShow',
    7:	'ChristmasSnow',
    8:	'CircleCat',
    9:	'CircleMouse',
    10:	'CirclePig',
    11:	'Comicmn',
    12:	'CuteBaby',
    13:	'Envolope',
    14:	'Fairytale',
    15:	'GoodNight',
    16:	'HalloweenNight',
    17:	'LovelyDay',
    18:	'Newyear2017',
    19:	'PinkSunny',
    20:	'KIRAKIRA',
    21:	'欢乐球吃球2:',
    22:	'SnowWhite',
    23:	'SuperStar',
    24:	'WonderfulWork',
    25:	'Cold',
    26:	'狼人杀守卫',
    27:	'狼人杀猎人',
    28:	'狼人杀预言家',
    29:	'狼人杀村民',
    30:	'狼人杀女巫',
    31:	'狼人杀狼人'
    }
    if flag == 1:
        return list(STICKER_TYPE.values())
    else:
        return STICKER_TYPE

def main():
    # res = meizhuang('1.jpg','日系妆-烟灰')
    # print(res)
    # res = bianzhuang('1.jpg')
    # print(res)
    # res = ronghe('1.jpg')
    # print(res)
    res = datoutie('1.jpg','狼人杀狼人')
    print(res)
    print(datoutie_type())
if __name__ == '__main__':
    main()
