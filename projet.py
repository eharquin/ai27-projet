# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 12:27:31 2021

@author: benjam
"""

"""requin=1 tigre=2 crocodile=3 rien=4
   mer=1 terre=2"""

from typing import List, Tuple
import itertools
import subprocess

nbcol=3
nblig=3

def creationGrille(nbcol: int, nblig: int):
    grille=[]
    for i in range(nblig):
        for j in range(nbcol):
            for t in range(2):
                for z in range (4):
                    grille.append([i+1,j+1,t+1,z+1])
                    
    return grille


def uniqueAnimaux(vars: List[int]) -> List[List[int]]:
    l=[vars]
    for a,b in itertools.combinations(vars,2):
        l.append([-a,-b])
    return l


def uniqueTerrain(vars: List[int]) -> List[List[int]]:
    l=[vars]
    for a,b in itertools.combinations(vars,2):
        l.append([-a,-b])
    return l


def terrainAnimaux(vars: List[int]) -> List[List[int]]:
    l=[]
    if vars[3]==1:
        l=[vars[0],vars[1],1,-vars[3]]
    elif vars[3]==2:
        l=[vars[0],vars[1],2,-vars[3]]
    else:
        l=vars 
    return l


def compteurs(Grille: List[List[int]], nbterre:int, nbterremax:int, nbmer:int, nbmermax:int, nbrequins:int, nbrequinsmax:int, nbcrocos:int, nbcrocosmax:int, nbtigres:int, nbtigresmax:int):
    l=[]
            
            

def main():
    Grille=creationGrille(nbcol,nblig)
    print(uniqueAnimaux([1,1,3]))
    print(uniqueTerrain([1,1,2]))
    print(terrainAnimaux([1,1,2,2]))

if __name__ == "__main__":
    main()





"""def create_cell_constraints(Grille: List[List[int]]) -> List[List[int]]:
    l=[]
    for cell in Grille:
        l.append(uniqueAnimaux([cell[0],cell[1],cell[3]]))
        l.append(uniqueAnimaux([cell[0],cell[1],cell[2]]))
    return l

print(create_cell_constraints(Grille))"""
      
