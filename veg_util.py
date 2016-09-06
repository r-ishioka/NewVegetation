import struct

def rdb(fin,n):
  f=open(fin)
  temp=f.read(480)
  for i in range(n):
    temp2=f.read(1303)
    print temp2[8:14]
  f.close()

def rdb2(fin,fout):
  f=open(fin)
  g=open(fout,'w')
  temp=f.read(480)
  while True:
    temp2=f.read(1303)
    #if not temp2:
    if len(temp2)!=1303:
      break
    g.write(temp2[8:14]+'\n')
  f.close()
  g.close()

def rshape(fin,n):
  f=open(fin,'r')
  temp=f.read(28)
  print struct.unpack(">LLLLLLL",temp)
  temp=f.read(8)
  print struct.unpack("<LL",temp)
  temp=f.read(64)
  print struct.unpack("8d",temp)
  for k in range(n):
    temp=f.read(8)
    print struct.unpack(">LL",temp)
    temp=f.read(4)
    print struct.unpack("<L",temp)
    temp=f.read(32)
    print struct.unpack("4d",temp)
    temp=f.read(8)
    a4=struct.unpack("<LL",temp); print a4
    for i in range(a4[0]):
      temp=f.read(4)
      #print struct.unpack("<L",temp)
    for i in range(a4[1]):
      temp=f.read(16)
      #print struct.unpack("2d",temp)   
  f.close()

def rshape2(fin):
  f=open(fin,'r')
  temp=f.read(28)
  print struct.unpack(">LLLLLLL",temp)
  temp=f.read(8)
  print struct.unpack("<LL",temp)
  temp=f.read(64)
  print struct.unpack("8d",temp)
  while True:
    temp=f.read(8)
    if len(temp)!=8:
      break 
    print struct.unpack(">LL",temp)
    temp=f.read(4)
    print struct.unpack("<L",temp)
    temp=f.read(32)
    print struct.unpack("4d",temp)
    temp=f.read(8)
    a4=struct.unpack("<LL",temp); print a4
    for i in range(a4[0]):
      temp=f.read(4)
      #print struct.unpack("<L",temp)
    for i in range(a4[1]):
      temp=f.read(16)
      #print struct.unpack("2d",temp)   
  f.close()

def rshape3(fin,fin2,fout):
  f=open(fin,'r')
  d=open(fin2,'r')
  dtemp=d.read(480)
  g=open(fout,'w')
  temp=f.read(28)
  #print struct.unpack(">LLLLLLL",temp)
  temp=f.read(8)
  #print struct.unpack("<LL",temp)
  temp=f.read(64)
  #print struct.unpack("8d",temp)
  kk=1
  while True:
    dtemp2=d.read(1303)
    #print dtemp2[8:14]   
    temp=f.read(8)
    if len(temp)!=8:
      break 
    #print struct.unpack(">LL",temp)
    temp=f.read(4)
    #print struct.unpack("<L",temp)
    temp=f.read(32)
    #print struct.unpack("4d",temp)
    temp=f.read(8)
    a4=struct.unpack("<LL",temp); #print a4
    cc=[]
    for i in range(a4[0]):
      temp=f.read(4)
      #print struct.unpack("<L",temp)
      cc.append(struct.unpack("<L",temp)[0])
    cc.append(a4[1])
    #print cc
    for i in range(a4[0]):
      #print kk,cc[i+1]-cc[i]
      #print cc[i],cc[i+1]
      #if i == 0: print kk,cc[i]-cc[i],'  '+dtemp2[8:14]
      #else: print kk,cc[i+1]-cc[i],' -'+dtemp2[8:14]
      if i == 0: g.write('{0:} {1:}  {2}\n'.format(kk,cc[i]-cc[i],dtemp2[8:14]))
      else: g.write('{0:} {1:} -{2}\n'.format(kk,cc[i]-cc[i],dtemp2[8:14]))
      kk=kk+1
      for k in range(cc[i+1]-cc[i]):
        temp=f.read(16)
        xx=struct.unpack("2d",temp)
        #print '{0:.6f} {1:.6f}'.format(xx[0],xx[1]) 
        g.write('{0:.6f} {1:.6f}\n'.format(xx[0],xx[1]))
  f.close()
  d.close()
