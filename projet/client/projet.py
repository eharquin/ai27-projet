# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 12:27:31 2021

@author: benjam
"""

"""requin=1 tigre=2 crocodile=3 rien=4
   mer=1 terre=2"""

from typing import List, Tuple, Dict
from crocomine_client import CrocomineClient
import itertools
import subprocess

nbcol=3
nblig=3

nbterre=3
nbterremax=3
nbmer=0
nbmermax=9
nbtigres=0
nbtigresmax=45
nbcrocos=0
nbcrocosmax=8485
nbrequins=0
nbrequinsmax=4854

def creationGrilleVierge(nbcol: int, nblig: int):
    grille=[]
    for i in range(nblig):
        for j in range(nbcol):
            grille.append([i+1,j+1,-1,-1])
                    
    return grille

def creationGrillePossibilités(nbcol: int, nblig: int):
    grille=[]
    for i in range(nblig):
        for j in range(nbcol):
            for t in range(2):
                for z in range (4):
                    grille.append([i+1,j+1,t+1,z+1])
                    
    return grille

def PassageTableauDico(Tab: List[List[int]]):
    dico={}
    i=1
    for cell in Tab:
        dico[i]=cell
        i=i+1
    return dico



def unique(vars: List[int]) -> List[List[int]]:
    l=[vars]
    for a,b in itertools.combinations(vars,2):
        l.append([-a,-b])
    return l

def unique_generator(vars: Dict[List[int]]):
    li=[]
    l=[]
    for i in range(1, len(vars)):
        l.append(i)
        if i%8==0:
            li = unique(l)
            l=[]




def terrainAnimaux(vars: List[int]) -> List[List[int]]:
    l=[]
    if vars[3]==1:
        l=[vars[0],vars[1],1,-vars[3]]
    elif vars[3]==2:
        l=[vars[0],vars[1],2,-vars[3]]
    else:
        l=vars 
    return l


def compteurs(GrilleV: List[List[int]], nbterre:int, nbterremax:int, nbmer:int, nbmermax:int, nbrequins:int, nbrequinsmax:int, nbcrocos:int, nbcrocosmax:int, nbtigres:int, nbtigresmax:int):
        if nbterre==nbterremax:
            for cell in GrilleV:
                if cell[2]==-1:
                    cell[2]=1
        if nbmer==nbmermax:
            for cell in GrilleV:
                if cell[2]==-1:
                    cell[2]=2
        return GrilleV
                
            

def main():
    print(unique((1,2,3,4,5,6,7,8)))
    GrilleVraie=creationGrilleVierge(nbcol,nblig)
    print(GrilleVraie)
    GrillePossibilités=creationGrillePossibilités(nbcol, nblig)
    """print(GrillePossibilités)
    print(uniqueAnimaux([1,1,3]))
    print(uniqueTerrain([1,1,2]))
    print(terrainAnimaux([1,1,2,2]))"""
    GrilleVraie=compteurs(GrilleVraie, nbterre, nbterremax, nbmer, nbmermax, nbrequins, nbrequinsmax, nbcrocos, nbcrocosmax, nbtigres, nbtigresmax)
    
    print(PassageTableauDico(GrilleVraie))

if __name__ == "__main__":
    main()





"""def create_cell_constraints(Grille: List[List[int]]) -> List[List[int]]:
    l=[]
    for cell in Grille:
        l.append(uniqueAnimaux([cell[0],cell[1],cell[3]]))
        l.append(uniqueAnimaux([cell[0],cell[1],cell[2]]))
    return l

print(create_cell_constraints(Grille))"""
      
