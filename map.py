# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 15:35:41 2021

@author: sj
"""

from PIL import Image,ImageDraw,ImageFont
import random as ra


n=20
cov=[1,3,9,14]
rest=[1,4,12,14,15,19]
col=[(0, 0,255, 125)]*n
for i in range(0,n):
    if i+1 in cov:
        col[i]=(255, 0, 0, 125)
xx=[]
yy=[]
xx.append([])
yy.append([])
for i in range(0,n):

    xx[-1].append(ra.randint(100,900))
    yy[-1].append(ra.randint(100,900))
for i in range(0,4):
    a=xx[0].copy()
    b=yy[0].copy()
    for i in range(0,len(a)):
        if i+1 not in rest:
            a[i]+=ra.randint(-100,300)
            b[i]+=ra.randint(-100,300)
    xx.append(a.copy())
    yy.append(b.copy())

xx=[[851, 806, 740, 624, 791, 310, 141, 147, 351, 651, 714, 860, 547, 666, 481, 745, 697, 269, 895, 320], [851, 903, 754, 624, 801, 588, 126, 338, 409, 946, 757, 860, 633, 666, 481, 746, 801, 479, 895, 456], [851, 718, 861, 624, 823, 442, 134, 264, 392, 613, 709, 860, 488, 666, 481, 794, 805, 329, 895, 417], [851, 856, 980, 624, 777, 446, 61, 197, 371, 671, 731, 860, 725, 666, 481, 1012, 812, 238, 895, 227], [851, 813, 666, 624, 1018, 301, 60, 407, 526, 755, 689, 860, 758, 666, 481, 768, 983, 495, 895, 271]]
yy=[[625, 265, 545, 574, 670, 567, 463, 334, 555, 888, 459, 175, 694, 374, 356, 798, 747, 740, 693, 859], [625, 425, 823, 574, 677, 764, 494, 472, 696, 1018, 714, 175, 889, 374, 356, 854, 891, 925, 693, 1085], [625, 528, 560, 574, 835, 538, 729, 425, 655, 1132, 372, 175, 890, 374, 356, 870, 810, 776, 693, 1025], [625, 318, 559, 574, 800, 820, 717, 387, 813, 994, 527, 175, 618, 374, 356, 1085, 716, 691, 693, 806], [625, 337, 663, 574, 791, 642, 576, 544, 555, 996, 583, 175, 853, 374, 356, 904, 814, 900, 693, 1121]]
for j in range(0,5):
    im = Image.open("map.png")
    im = im.convert('RGB')
    draw = ImageDraw.Draw(im,'RGBA')
    x=xx[j]
    y=yy[j]
    width, height = im.size
    draw.rectangle(xy=[(2, 2), (300,200)],fill=None, outline='black', width=1)
    r=23
    ccc=0
    for i in col:
        if i==(255, 165, 0, 125):
            ccc+=1
    font = ImageFont.truetype("arial.ttf", 25)
    draw.text((3,4),'Color-Code','black',font=font)            
    draw.text((220,4),'Count','black',font=font)            
    draw.ellipse((30-r, 50-r, 30+r, 50+r), col[0])
    draw.text((60,40),'Covid-19 +ive        '+str(len(cov)),'black',font=font)         
    
    draw.ellipse((30-r, 100-r, 30+r, 100+r),(255, 165, 0, 125) )
    draw.text((60,90),'Suspected +ive      '+str(ccc),'black',font=font)         
    
    draw.ellipse((30-r, 150-r, 30+r, 150+r), (0, 0, 255, 125))
    draw.text((60,140),'Covid-19 -ive        '+str(n-(len(cov))-ccc),'black',font=font)   
    for i in range(0,n):
        r=25
        q=x[i]
        w=y[i]
        draw.ellipse((q-r, w-r, q+r, w+r), col[i])
        font = ImageFont.truetype("arial.ttf", 40)
        if i>=10:
            draw.text(xy=(q-24,w-19), text= str(i+1),fill= "black",font=font)
        else:
            draw.text(xy=(q-13,w-18), text= str(i+1),fill= "black",font=font)    
    cc=45
    for i in range(0,n):
        for jj in range(i+1,n):
            if abs(x[jj]-x[i])<cc and abs(y[i]-y[jj])<cc:
                if col[i]==(255, 0, 0, 125):
                    if col[jj]!=(255, 0, 0, 125):
                        col[jj]=(255, 165, 0, 125)
                if col[jj]==(255, 0, 0, 125):
                    if col[i]!=(255, 0, 0, 125):
                        col[i]=(255, 165, 0, 125)
      
    
    
    im.save('mapop'+str(j)+'.pdf')
