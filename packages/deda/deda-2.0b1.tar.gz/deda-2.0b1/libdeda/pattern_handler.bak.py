# -*- coding: utf-8 -*- 
'''
The patterns and their specific functions
Align all matrices for each translation and do redundance checks

Example: 
    from extract_yd import YDX
    from pattern_handler import TDM, patterns
    
    for m in YDX("input.jpg").matrices:
        transformations = patterns[2].getTransformations(m)
        for t in transformations:
            tdm = TDM(m=m, pattern=patterns[2], trans=t)
            if tdm.check(): 
                print(tdm)
                print(tdm.decode())
                exit()
            else: print("Invalid matrix, trying other...")


Copyright 2018 Timo Richter

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''

import argparse, os, sys, math, random
import numpy as np
from libdeda.extract_yd import MatrixTools, matrix2str, array2str


class _MatrixParserInterface(object):

    """
    Interface
    """
    
    def checkAnyRolling(self,m):
        """
        Optional function for performance reasons
        Do quick verification on original matrix that has been rotated and
        flipped but not rolled. If this is implemented,
        a pattern can be excluded without completely aligning it.
        Output: bool
        """
        pass
    
    @classmethod
    def applyCopies(self,m):
        """
        If @m contains a prototype and copies of it, update the copies
        """
        pass
        
    def crop(self,m): 
        """
        Format the matrix into a specific shape for check() and decode()
        Input: aligned matrix m
        Output: matrix m'
        """
        pass
        
    def check(self,m): 
        """
        Verify a matrix' validity
        Input: cropped matrix m
        Output: bool
        """
        pass
    
    def decode(self,m):
        """
        Transform a matrix to human readable information
        Input: cropped matrix m
        Output: dict
        """
        pass
        
    def createMask(self, m):
        """
        Returns anonymisation mask. United with @m it will contain
            ambiguous information.
        Input: aligned matrix m
        Output: matrix of same shape as m
        """
        

class _AbstractMatrixParser(_MatrixParserInterface):

    # Size
    n_i = -1
    n_j = -1
    d_i = -1
    d_j = -1
    
    # When reading, do a majority decision for @minCount TDMs. At least this
    # amount of valid TDMs has to be detected for a certain pattern. -1=all
    minCount = 1
    
    # For offset patterns: Define distance between markers, default: n_i, n_j
    n_i_prototype = property(lambda self:self.n_i)
    n_j_prototype = property(lambda self:self.n_j)
    
    hps = property(lambda self:self.n_i*self.d_i)
    vps = property(lambda self:self.n_j*self.d_j)
    
    def __int__(self):
        return int(''.join(list(
            filter(str.isdigit, self.__class__.__name__))))
    
    def __str__(self):
        return "Pattern %d"%int(self)
    
    def __hash__(self):
        return hash(self.__class__.__name__)
    
    def checkAnyRolling(self,m):
        return True

    def align(self, m, *args, **xargs):
        transformations = self.getTransformations(m,*args,**xargs)
        l = []
        for d in transformations:
            m = self.applyTransformation(m,d)
            l.append(m)
        return l

    @classmethod
    def applyTransformation(self, m, d):
        if d.get("flip"): m=np.fliplr(m)
        if d.get("rot"): m=np.rot90(m,d["rot"])
        m = np.roll(m,(d["x"],d["y"]),(0,1))
        return self.applyCopies(m)
    
    @staticmethod
    def undoTransformation(m, d):
        m = np.roll(m,(-d["x"],-d["y"]),(0,1))
        if d.get("rot"): m=np.rot90(m,4-d["rot"])
        if d.get("flip"): m=np.fliplr(m)
        return m
    
    @classmethod
    def applyCopies(self, m):
        return m
        
    def getTransformations(self,m_,empty=[],nempty=[],strict=True,
            allowFlip=False,allowUpsideDown=True,rot=0):
        """
        Get geometrical transformations to move a matrix to a unique point
        Note: If the dict self.alignment is present, then empty, nempty, 
            allowFlip and rot are being read from there.
        
        @m_ numpy matrix,
        @empty list of coordinate tuples where m_ should not have dots,
        @allowFlip bool: analyse the horizontally flipped matrix as well,
        @rot int: matrix must be rotated at @rot degrees,
        @returns the list of the transformations that fit best @nempty and 
                @empty. Format:
            [dict(
                x=int rolling_axis_0,
                y=int rolling_axis_1,
                rot=int rotated_x_times_90_deg,
                flip=bool
            )]
        """
        if strict == False: raise NotImplementedError("Set strict to True")
        if isinstance(getattr(self,"alignment",None),dict):
            empty = self.alignment.get("empty",empty)
            nempty = self.alignment.get("nempty",nempty)
            allowFlip = self.alignment.get("allowFlip",allowFlip)
            allowUpsideDown = self.alignment.get("allowUpsideDown",allowUpsideDown)
            rot = self.alignment.get("rot",rot)
        l = []
        rotations = [rot,rot+2] if allowUpsideDown else [rot]
        for rot_ in rotations:
          for flip in set([False, allowFlip]):
            m = m_.copy()
            if flip: m = np.fliplr(m)
            if rot_ != 0: m = np.rot90(m,rot_)
            if not self.checkAnyRolling(m): continue
            dd = [dict(x=-x,y=-y,rot=rot_,flip=flip)
                for x in range(m.shape[0])
                for y in range(m.shape[1])
                if all([m[(dotx+x)%m.shape[0],(doty+y)%m.shape[1]] for dotx,doty in nempty]) and not any([m[(dotx+x)%m.shape[0],(doty+y)%m.shape[1]] for dotx,doty in empty])
            ]
            l.extend(dd)
        return l
        

class Pattern1(_AbstractMatrixParser):
  
  n_i = 32
  n_j = 32
  d_i = .02
  d_j = .02
  n_i_prototype = 16
  n_j_prototype = 16
  minCount = -1
  alignments=[
    dict(nempty=[(0,0),(1,0)],
        empty=[(x,y) for x in range(0,16) for y in (2,4,6,8,10,12,14)]\
            +[(x,y) for x in e2 for y in range(1,16)],
        rot=rot, allowUpsideDown=False
    )
  for rot in [0,3]
  for e2 in [(3,5,7,9,11,13,15),(0,2,4,6,8,10,12,14)]
  ]
  
  @classmethod
  def applyCopies(self,aligned):
    aligned[16:32,16:32] = aligned[0:16,0:16]
    return aligned
  
  def checkAnyRolling(self,m):
    dots = np.sum(m,axis=0)
    return 2 in dots and sum([1 for s in dots if s%2==0]) >= 8
    #return 2 in dots and all([s%2==0 for s in dots])

  def getTransformations(self,m,transposed=False,strict=True):
    return [e for xargs in self.alignments 
        for e in super(Pattern1,self).getTransformations(m,**xargs)]

  def crop(self,m):
    C,R = self._findUsedCells(m)
    return np.array(m[C,:][:,R],dtype=np.uint8)

  def check(self,m):
    sums = np.sum(m,axis=0)
    return np.sum(m)>3 and all([bool(1-int(s%2)) for s in sums])
    
  def decode(self,m):
    info = list(reversed(m[1:,:].T.flatten()))
    words = list(map(''.join,zip(*[iter(map(str,info))]*4)))
    decoded = "".join([str(int(b,2)) for b in words])
    snr = decoded[-12:-1]
    trans = {'0':'W','9':'P'}
    snr2 = "%s%s%s%s"%((trans.get(snr[0]) or '?'),snr[1:4],
        (trans.get(snr[4]) or '?'),snr[5:11])
    return dict(raw=decoded, serial="%s or %s"%(snr,snr2), 
        manufacturer="Ricoh/Lanier/Savin/NRG", printer=decoded)

  def _findUsedCells(self, m):
    """ Finds the index s of first used column (2 or 3) and returns the 
    tuples R and C containing all row/column indexes """
    C3 = (3,5,7,9,11,13,15)
    C2 = (2,4,6,8,10,12,14)
    R = (1,3,5,7,9,11,13,15)
    #s=s2 if np.sum(m[s2,:]) > np.sum(m[s3,:]) else s3
    if np.sum(m[C2,:]) > np.sum(m[C3,:]): return C2, R
    else: return C3, R
      
  def createMask(self,m, allOnes=False):
    C,R = self._findUsedCells(m)
    anon = np.zeros(m.shape)
    if allOnes:
        for c in C: anon[c,R] = 1
    for r in R:
        amountNewDots = 3 if np.sum(m[C,r]) == 0 else 1
        C_empty = [c for c in C if m[c,r] == 0]
        C_fill = random.sample(C_empty,amountNewDots)
        anon[C_fill,r] = 1
    return self.applyCopies(anon)
    

class Pattern2(_AbstractMatrixParser):

  n_i = 18
  n_j = 23
  d_i = .03
  d_j = .03
  alignment = dict(empty=[(0,0),(2,1)],
        nempty=[(1,1),(1,0),(0,1)],allowFlip=True)
  manufacturers = {"3210": "Okidata", "3021": "HP", "2310": "Ricoh", 
        "0132": "Ricoh", "0213": "Lexmark", "0123": "Kyocera"}
  blocks = [[
            [(9*x+1+2*col+1-(5*y+2+row)%2,5*y+2+row) for col in range(4)]
            for row in range(5)]
        for y in range(4) for x in range(2)]

  def crop(self,m):
    return np.array([[[m[x,y] for x,y in word] for word in words] 
        for words in self.blocks])

  def check(self,m):
    return ( 
        # one hot encoding check
        all([(np.sum(words[0:4], axis=1)==1).all() for words in m])
        # parity check
        and all([(np.sum(words,axis=0)%2==1).all() for words in m]) 
    )
    
  def decode(self,m):
    trans = {'0001':0, '0010':1, '0100':2, '1000':3}
    blocks = ["".join([str(trans[array2str(w)]) for w in words[0:4]]) 
        for words in m]
    raw = "-".join(blocks)
    return dict(raw=raw, printer=raw,
        manufacturer=self.manufacturers.get(blocks[0]))
  
  def createMask(self, m):
    """ Full mask """
    anon = np.zeros(m.shape,dtype=np.uint8)
    for x,y in [z for x in self.blocks for y in x for z in y]:
        anon[x,y] = 1
    anon[m==1] = 0
    return anon
  
  def createMaskStrategic(self, m):
    oneHotCodes = [w for words in self.blocks for w in words[0:4]]
    parity = [cell for words in self.blocks for cell in words[4]]
    anon = np.zeros(m.shape,dtype=np.uint8)
    for b in oneHotCodes: # fill at random
        empty = [(x,y) for x,y in b if m[x,y] == 0]
        anon[random.choice(empty)] = 1
    empty = [(x,y) for x,y in parity if m[x,y] == 0]
    for x,y in empty: anon[x,y] = 1
    
    # blocks A and B
    anon[1:18,2:7] = 0
    trans = {str(v):k for k,v in {'0001':0, '0010':1, '0100':2, '1000':3}.items()}
    manuStr = self.decode(self.crop(m))["manufacturer"]
    otherManufacturers = [k for k,s in self.manufacturers.items() 
        if s!=manuStr]
    manu2 = random.choice(otherManufacturers)
    for r,v in enumerate(manu2):
        cy = r+2
        cx = 1
        code = trans[v] # e.g. "0001"
        col2x = lambda x: cx+2*x+1-cy%2 # column index to x coordinate
        for c,v in enumerate(code):
            if v == "0": continue # or m[col2x(c),cy] == 1
            anon[col2x(c),cy] = 1
    anon[m==1] == 0
    anon[10:18,2:7] = anon[1:9,2:7] # Block B := block A
    return anon
    

class Pattern21(Pattern2):

  n_i = 23
  n_j = 18
  alignment = dict(empty=[(0,0),(2,1)],
    nempty=[(1,1),(1,0),(0,1)],allowFlip=True,rot=1)


class Pattern3(_AbstractMatrixParser):    

  n_i = 24
  n_j = 48
  d_i = .02
  d_j = .02
  n_i_prototype = None
  n_j_prototype = None
  #alignment = dict(nempty = [(0,4+1),(0,1+1),(2,1+1)])
  alignment = dict(nempty = [(0,4),(0,1),(2,1)])
  blocks = [[((bx*4+by+x)%24,(3*by+1+y)%16) for y in range(3) for x in range(2)]
        for by in range(5) for bx in range(6) if bx+by>=2]
  
  def checkAnyRolling(self, m):
    return 30 in [np.sum(m[:,0:16]),np.sum(m[:,16:32]),np.sum(m[:,32:48])]

  @classmethod
  def applyCopies(self, m):
    m[:,16:32] = np.roll(m[:,0:16],8,0)
    m[:,32:48] = np.roll(m[:,16:32],8,0)
    return m
    
  def crop(self,m):
    #m = m[:,1:16+1]
    m = m[:,0:16]
    if np.sum(m) != 30: return None
    m = np.array([[m[x,y] for x,y in b] for b in self.blocks])
    return m

  def check(self,m):
    return all([np.sum(block)==1 for block in m])
    
  def decode(self,m):
    trans = {'000001':0, '000010':1, '000100':2, '001000':3, '010000':4,
        '100000':5}
    blocks = [str(trans[array2str(block)]) for block in m]
    raw = "--%s -%s %s %s %s"%(
        "".join(blocks[0:4]),"".join(blocks[4:9]),"".join(blocks[9:15]),
        "".join(blocks[15:21]),"".join(blocks[21:27]))
    return dict(raw=raw, printer=raw, manufacturer="Konica Minolta/Epson")
  
  def createMask(self, m):
    """ Full mask """
    anon = np.zeros(m.shape,dtype=np.uint8)
    for x,y in [y for x in self.blocks for y in x]:
        anon[x,y] = 1
    anon[m==1] = 0
    return self.applyCopies(anon)
  
  def createMaskStrategic(self,m):
    anon = np.zeros(m.shape,dtype=np.uint8)
    for b in self.blocks:
        empty = [(x,y) for x,y in b if m[x,y]==0]
        anon[random.choice(empty)] = 1
    return self.applyCopies(anon)


class Pattern31(Pattern3):

  n_i = 48
  n_j = 24
  alignment = dict(nempty = [(0,5),(0,2),(2,2)],rot=1)


class Pattern4(_AbstractMatrixParser):

  n_i = 16
  n_j = 32
  d_i = .04
  d_j = .04
  alignment=dict(empty = [(x,y) for x in range(8,16) for y in range(0,17)],
    allowFlip=True) #nempty = [(x,6) for x in range(1,4)] #1,8
  manufacturers = {0:"Xerox", 3:"Epson", 20: "Dell", 4: "Xerox"}

  def checkAnyRolling(self,m):
    # max. two rows and cols with even amount of dots
    rows = np.sum(m,axis=0)
    cols = np.sum(m,axis=1)
    return len([1 for r in rows if r%2==1]) >= 14 \
        and len([1 for c in cols if c%2==1]) >= 7
  
  @classmethod
  def applyCopies(self, m):
    m[8:16,16:32] = m[0:8,0:16]
    return m
  
  def crop(self,m):
    m = m[0:8,1:16]
    return m
    
  def check(self,m):
    r = (all([bool(int(s%2)) for s in np.sum(m[:,:14],axis=0)])
        and all([bool(int(s%2)) for s in np.sum(m[1:,:],axis=1)])
        and np.sum(m[1:4,8])==0 and np.sum(m[1:3,9:11])==0
    )
    return bool(r)
  
  def decode(self,m):
    m = np.rot90(m) # same shape as EFF
    format = dict(
        minutes=1, hour=4, day=5, month=6, year=7, serial=(12,11,10),
        unknown1=2, manufacturer=3, unknown3=8, unknown4=13, unknown5=14,
        printer=(13,12,11,10))
    decoded = {}
    for key,cols in format.items():
        if not isinstance(cols,tuple): cols = (cols,)
        decoded[key] = "".join(
            ["%02d"%int(array2str(m[col,1:]),2) for col in cols])
    decoded["raw"] = "".join(["%02d"%int(array2str(m[col+1,1:]),2) 
        for col in range(m.shape[0]-1)])
    if decoded["manufacturer"].isdigit() \
            and int(decoded["manufacturer"]) in self.manufacturers: 
        decoded["manufacturer"] = self.manufacturers.get(
            int(decoded["manufacturer"]))
    else: decoded["manufacturer"] = "Xerox/Dell/Epson"
    if decoded["manufacturer"] == "Dell": decoded["serial"] = None
    else: decoded["serial"] = "-%s-"%decoded["serial"]
    return decoded
    
  def createMask(self,m):
    anon = np.zeros(m.shape,dtype=np.uint8)
    anon[0:8,15] = 1
    anon[(7,6,5,3),12] = 1
    anon[3:8,8] = 1
    anon[4:8,9] = 1
    anon[3:8,10] = 1
    for y in range(1,6):
        empty = [x for x in range(0,8) if m[x,y] == 0]
        add = max(1, 4-int(np.sum(m[:,y])))
        anon[random.sample(empty,add),y] = 1
    anon[m==1] == 0
    return self.applyCopies(anon)


class Pattern41(Pattern4):

  n_i = 32
  n_j = 16
  alignment=dict(empty = [(x,y) for x in range(8,16) for y in range(0,17)],
    allowFlip=True,rot=1)


patterns = {int(cls()):cls() 
    for name, cls in globals().items() 
    if name.startswith("Pattern")}


class TDM(object):
    """
    An aligned Tracking Dots Matrix
    """
    
    def __init__(self, pattern, trans, atX, atY, m=None, aligned=None, 
            cropped=None):
        """
        One of @m or @aligned is required. @aligned must be @m transformed
            according to @trans.
        
        pattern _MatrixParserInterface pattern object,
        trans dict transformation dict,
        atX int position on paper in pixels,
        atY int,
        m np.array untransformed matrix,
        aligned np.array transformed matrix,
        cropped np.array cropped matrix of @aligned (optional).
        """
        assert(m is not None or aligned is not None)
        self.pattern = pattern
        self.atX = atX
        self.atY = atY
        self.trans = trans
        self.aligned = self.pattern.applyTransformation(m,self.trans) if \
            aligned is None else aligned
        self.cropped = self.pattern.crop(self.aligned) if cropped is None \
            else cropped
        
    def __getattr__(self, name):
        return getattr(self.pattern,name)(self.m)
        
    def decode(self):
        return self.pattern.decode(self.cropped)
        
    def check(self):
        return self.cropped is not None and self.pattern.check(self.cropped)
        
    def createMask(self, addTdm=True):
        mask = self.pattern.createMask(self.aligned)
        if addTdm: mask = np.array((self.aligned+mask)>0,dtype=np.uint8)
        return TDM(
            aligned=mask,atX=self.atX,atY=self.atY,
            pattern=self.pattern,trans=self.trans)
        
    def __str__(self):
        return matrix2str(self.aligned)
        
    def __repr__(self):
        return "<TDM of Pattern %d at %d x %d pixels>"%(
            self.pattern,self.atX,self.atY)
        
    def undoTransformation(self):
        return self.pattern.undoTransformation(self.aligned,self.trans)
        
    def __hash__(self):
        if self.cropped is None: return hash(None)
        return hash("".join([str(int(x)) for x in self.cropped.flat]))
        
    def __eq__(self, o):
        return hash(self) == hash(o)
        
        
