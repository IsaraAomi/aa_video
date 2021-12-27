from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
import os

# https://qiita.com/Cartelet/items/542fe3f966b8fa98437a

# tqdm's bar_format
short_progress_bar="{l_bar}{bar:10}{r_bar}{bar:-10b}"


def make_map(str_list):
    l=[]
    font = ImageFont.truetype('../fonts/msgothic.ttc', 20)
    for i in str_list:
        im = Image.new("L",(20,20),"white")
        draw = ImageDraw.Draw(im)
        draw.text((0,0),i,font=font)
        l.append(np.asarray(im).mean())
    l_as = np.argsort(l)
    lenl = len(l)
    l2256 = np.r_[np.repeat(l_as[:-(256%lenl)],256//lenl),np.repeat(l_as[-(256%lenl):],256//lenl+1)]
    chr_map = np.array(str_list)[l2256]
    return chr_map


def output(chr_map, imarray, isOutText, out_path):
    aa = chr_map[imarray].tolist()
    if isOutText:
        with open(out_path,"w") as f:
            for i in range(len(imarray)):
                f.write(''.join(aa[i])+"\n")
    else:
        for i in range(len(imarray)):
            print(''.join(aa[i]))


def make_AA(file_path, 
            str_list="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz +-*/%'"+'"!?#&()~^|@;:.,[]{}<>_0123456789',
            width=150, isOutText=False, out_path="aa.txt", isFW=False):
    imag = Image.open(file_path).convert('L')
    if isFW:str_list=list(str_list.translate(str.maketrans({chr(0x0021 + i):
        chr(0xFF01 + i) for i in range(94)})))
    else:
        str_list=list(str_list)
    imarray = np.asarray(imag.resize((width, width*imag.height//imag.width//(2-int(isFW)))))
    output(make_map(str_list), imarray, isOutText, out_path)


def task_get_rgb_array(file_path, width=150, isFW=False):
    imag = Image.open(file_path).convert('RGB')
    imarray = np.asarray(imag.resize((width, width*imag.height//imag.width//(2-int(isFW)))), dtype='uint8')
    return imarray


def task_get_rgb_array_wrapper(args):
    return task_get_rgb_array(*args)


def get_4d_array(flist, t_width, t_height, frame, isFW=False):
    new_flist = []
    for file_path in flist:
        new_flist.append((file_path, t_width, isFW))
    # multiprocessing by Pool
    # used (Number of Logical CPUs - 1)
    varray = np.zeros((frame, t_height, t_width, 3), dtype='uint8')
    with Pool(os.cpu_count() - 1) as pool:
        imap = pool.imap(task_get_rgb_array_wrapper, new_flist)
        vlist = list(tqdm(imap, total=len(new_flist), bar_format=short_progress_bar))
    varray = np.array(vlist)
    return varray


def main():
    file_path = '../data/image/Shortcake_SONG_shorts_1080pFHR/img_0500.png'
    make_AA(file_path=file_path)
    # print(get_rgb_array(file_path=file_path))


if __name__ == '__main__':
    main()
