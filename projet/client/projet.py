# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 12:27:31 2021

@author: benjam
"""

"""requin=1 tigre=2 crocodile=3 rien=4
   mer=1 terre=2"""

from typing import List, Tuple, Dict
from pprint import pprint
from crocomine_client import CrocomineClient
import itertools
import subprocess

nbcol=15
nblig=15

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
                    if not ((t==0 and z==1) or (t==1 and z==0)):
                        grille.append([i+1,j+1,t+1,z+1])
                    
    return grille

def PassageTableauDico(Tab: List[List[int]]):
    dico={}
    i=0
    for cell in Tab:
        i=i+1
        dico[i]=cell        
    return dico



def unique(vars: List[int]) -> List[List[int]]:
    l=[vars]
    for a,b in itertools.combinations(vars,2):
        l.append([-a,-b])
    return l

def unique_generator(vars: Dict[int, List[int]]):
    li=[]
    l=[]
    for i in range(1, len(vars)+1):
        l.append(i)
        if i%6==0:
            li.append(unique(l))
            l=[]
    return li


"""def terrainAnimaux(vars: List[int]) -> List[List[int]]:
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
                  """

def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) -> str:
    p="p cnf "+str(nb_vars)
    inter=""
    inter2=""
    i=0
    for serie in clauses:
        for clause in serie:
           i=i+1
           inter=""
           for variable in clause:
               inter=inter+" "+str(variable)
           inter2=inter2 + "\n" + inter + " 0"   
    p=p+" "+str(i)+inter2+"\n"
    return p



def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)
        
def exec_gophersat(
    filename: str, cmd: str = "./gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    print(result)

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:].split(" ")

    return True, [int(x) for x in model]
            

def main():
    server = "http://localhost:8000"
    group = "Groupe "
    members = "Benjamin et Enzo"
    croco = CrocomineClient(server, group, members)

    status, msg, grid_infos = croco.new_grid()
    print(status, msg)
    pprint(grid_infos)

    




    GrilleVraie=creationGrilleVierge(grid_infos.n,grid_infos.m)
    #print(GrilleVraie)
    GrillePossibilités=creationGrillePossibilités(grid_infos.n,grid_infos.m)
    #print(GrillePossibilités)
    
    """GrilleVraie=compteurs(GrilleVraie, nbterre, nbterremax, nbmer, nbmermax, nbrequins, nbrequinsmax, nbcrocos, nbcrocosmax, nbtigres, nbtigresmax)
    """
    Dico=PassageTableauDico(GrillePossibilités)
    
    unique=unique_generator(Dico)
    #print(unique)
    
    
    
    write_dimacs_file(clauses_to_dimacs(unique,nbcol*nblig*6), "demineur.cnf")
    exec_gophersat("demineur.cnf")

if __name__ == "__main__":
    main()
