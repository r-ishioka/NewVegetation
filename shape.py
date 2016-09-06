#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:03:34 2016

@author: test2
"""

import os
import veg_util as ut
import conv_util as conv
import numpy as np
import cv2
import sys

param=sys.argv
if len(param)!=2:
    print 'Usage: shape.py file_name'

f=open(param[1])
lines=f.readlines()
f.close()

for line in lines:
  if(line.find('xs') != -1):
    _,temp=line.split() 
    xs = float(temp)
  if(line.find('xe') != -1):
    _,temp=line.split() 
    xe = float(temp)
  if(line.find('ys') != -1):
    _,temp=line.split() 
    ys = float(temp)
  if(line.find('ye') != -1):
    _,temp=line.split() 
    ye = float(temp)
  if(line.find('dx') != -1):
    _,temp=line.split() 
    dx = float(temp)
  if(line.find('dy') != -1):
    _,temp=line.split() 
    dy = float(temp)
  print line,

lat0,lon0=conv.utm2bl([xs,ye])
lat1,lon1=conv.utm2bl([xe,ye])
lat2,lon2=conv.utm2bl([xs,ys])
lat3,lon3=conv.utm2bl([xe,ys])

def mcode(lat,lon):
  b0=int(1.5*lat)
  b1=int(8*(1.5*lat-b0))
  l0=int(lon-100.0)
  l1=int(8*(lon-100.0-l0))
  return [100*b0+l0,10*b1+l1]

code1,code2=mcode(lat0,lon0)
fname0='shp{}{}'.format(code1,code2)
code1,code2=mcode(lat1,lon1)
fname1='shp{}{}'.format(code1,code2)
code1,code2=mcode(lat2,lon2)
fname2='shp{}{}'.format(code1,code2)
code1,code2=mcode(lat3,lon3)
fname3='shp{}{}'.format(code1,code2)

fname=[fname0,fname1,fname2,fname3]
image=np.zeros((1000,1000),np.uint16)

os.chdir('SHAPE')

for fnum in range(4):
    os.chdir(str(fname[fnum]))
    fin='p'+str(fname[fnum][3:])+'.dbf'
    ut.rdb2(fin,'../../temp.txt')
    fin='p'+str(fname[fnum][3:])+'.shp'
    fin2='p'+str(fname[fnum][3:])+'.dbf'
    fout=('test.bl')
    ut.rshape3(fin,fin2,fout)
    f=open('test.bl')
    lines=f.readlines()
    f.close()
    f=open('utm2.txt','w')
    for line in lines:
        if len(line) > 20:
            temp=line.split()
            lon=float(temp[0])
            lat=float(temp[1])
            xy=conv.bl2utm([lat,lon])
            f.write('{0:.2f} {1:.2f}\n'.format(xy[0],xy[1]))
        else:
            x=0
            a=lines.index(line)
            count=0
            while True:
                x = x + 1
                if a+x==len(lines):
                    break
                if len(lines[a+x]) > 20:
                    count = count + 1
                else:
                    break
            b=line.split()
            f.write(b[0]+' '+format(count)+'  '+b[2]+'\n')
    
    f.close()
    f=open('utm2.txt')
    lines=f.readlines()
    f.close()
    for line in lines:
        if len(line)<20:
            a=line.split()
            b=int(a[1])
            c=lines.index(line)
            d=np.zeros(2*b).reshape((b,2))
            for z in range(int(a[1])):
                d[z][0]=float(lines[c+z+1].split()[0])
                d[z][1]=float(lines[c+z+1].split()[1])
            d[:,0]=(d[:,0]-xs)/dx
            d[:,1]=(ye-d[:,1])/dy
            F=np.int32(d)
            cv2.fillPoly(image,[F],int(a[2][:4]))
    
    os.chdir('..')


cv2.imshow('image',image*10)
cv2.waitKey(0)

os.chdir('..')
conv.xs=xs
conv.xe=xe
conv.ys=ys
conv.ye=ye
conv.dx=dx
conv.dy=dy
conv.write_tifC('test.tif',image,1)

#gt,proj,img=conv.read_tif('test.tif')