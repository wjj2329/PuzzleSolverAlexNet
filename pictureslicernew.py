import numpy as np
import scipy.misc
import os
from PIL import Image
import random

class newsegs:
 def __init__(self, size,folder, save):
   self.folder=folder
   self.size=size
   self.save=save
   self.files=[]
   self.foldername=""
 def calcgoodsegments(self, data, shape):
      attempt=0
      while True:
          if (shape[0]-(self.size-1)<=0 or (shape[1]-(self.size-1))<=0 ):
            return (-1, -1)
          x=random.randint(0,(shape[0]-(self.size)-1))
          y=random.randint(0,(shape[1]-(self.size)-1))
          if attempt==10:
             return (-1, -1)
          if np.all(data[x][y+(self.size/2)]==(0,0,0)) or np.all(data[x+self.size][y+(self.size/2)]==(0,0,0)) or np.all(data[x+self.size][y]==(0,0,0) ) or np.all(data[x][y]==(0,0,0)) :
           attempt+=1
           continue
          else:
           return (x, y)

 def calcbadsegments(self, data, shape):
      attempt=0
      while True:
          if (shape[0]-(self.size-1)<=0):
           return (-1, -1)
          x=random.randint(0,(shape[0]-self.size)-1)
          y=random.randint(0,(shape[1]-self.size)-1)
          if attempt==10:
             return (-1, -1, -1, -1)
          if np.all(data[x][y+(self.size/2)]==(0,0,0)) or np.all(data[x+self.size][y+(self.size/2)]==(0,0,0)) or np.all(data[x+self.size][y]==(0,0,0) ) or np.all(data[x][y]==(0,0,0)) :
           attempt+=1
           continue
          else:
            attempt2=0
            while True:          
               if (shape[0]-(self.size-1)<=0):
                   return (-1, -1)
               x2=random.randint(0,((shape[0]-self.size)-1))
               y2=random.randint(0,(shape[1]-(self.size)-1))
               if attempt2==10:
                 return (-1, -1, -1, -1)
               if np.all(data[x2][y2+(self.size/2)]==(0,0,0)) or np.all(data[x2+self.size][y2+(self.size/2)]==(0,0,0)) or np.all(data[x2+self.size][y2]==(0,0,0) ) or np.all(data[x2][y2]==(0,0,0)) :
                 attempt2+=1
                 continue 
               if  x2>x-(self.size/2) and x2<x+self.size:
                  attempt2+=1
                  continue
               if y2>x-(self.size/2) and y2<y+self.size:
                  attempt2+=1
                  continue   
               return (x, y, x2, y2)      
 
 def gatherFiles(self, foldername):
  for filename in os.listdir(foldername):
      if filename !=".DS_Store":
       self.files.append(filename)
  random.shuffle(self.files)
  self.foldername=foldername                  
     
 def getBatch(self):
    toreturn=[]
    for x in range(100):
        if(len(self.files)<1):
          return toreturn
        loc=random.randint(0,(len(self.files)-1))
        filename=self.files[loc]
        if filename[0]=='b':
         img=Image.open(self.foldername+"/"+filename)
         img.load()
         data=np.asarray(img, dtype=np.float32)
         n=np.asarray([1,0], dtype=np.float32)
         combo=(data, n)
         toreturn.append(combo)
        else:
         img=Image.open(self.foldername+"/"+filename)
         img.load()
         data=np.asarray(img, dtype=np.float32)
         n=np.asarray([0,1], dtype=np.float32)
         combo=(data, n)
         toreturn.append(combo)
        del self.files[loc]
    return toreturn    

 def calculatesegments(self, pieces, dest):
    for filename in os.listdir(self.folder):
     for number in range(pieces):
      #open file convert to np array
      #print filename, " ", number
      if filename!=".DS_Store":
        img=Image.open(self.folder+"/"+filename)
        img.load()
        data=np.asarray(img, dtype="int32")
        #randomly rotate the picture
        #degree=random.randint(0,359)
        #data=scipy.ndimage.interpolation.rotate(data,degree)
        #now time to get random points that isn't a pure black value
        shape=data.shape
        if shape[0]-self.size-1==0 or shape[0]-self.size-1==0:
          continue
        pair=self.calcgoodsegments(data, shape)
        x=pair[0]
        y=pair[1]
        if x==-1 and y==-1:
          continue

        picture1=data[x+(self.size/4):x+(self.size/2)+(self.size/4), y:y+(self.size/2)]
        #picture2=data[x+(self.size/2):x+self.size, y:y+self.size/2]
        n=np.asarray([0,1])
        tup=(picture1,n)
        #self.segments.append(tup)

        #print picture1 for testing purposes
        #print picture2 for testing purposes
        #scipy.misc.imsave("r"+filename, data)
        scipy.misc.imsave(dest+"/g"+str(number)+filename, picture1)
        #scipy.misc.imsave("r2"+filename, picture2)


        #now to do it for bad connections
        pair2=self.calcbadsegments(data, shape)
        x=pair2[0]
        y=pair2[1]
        x2=pair2[2]
        y2=pair2[3]
        if x==-1 and y==-1 and x2==-1 and y2==-1:
          continue
        badpic1=data[x:x+(self.size/4), y:y+(self.size/2)]
        badpic2=data[x2:x2+(self.size/4), y2:y2+(self.size/2)]
        combo=np.vstack((badpic1,badpic2))
        n=np.asarray([1,0])
        tup2=(combo,  n)
        #self.segments.append(tup2)
        #scipy.misc.imsave("b"+filename, data)
        scipy.misc.imsave(dest+"/b"+str(number)+filename, combo)
        #scipy.misc.imsave("b2"+filename, badpic2)
     
