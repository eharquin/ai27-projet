from os import stat
from typing import List, Tuple, Dict
from pprint import pprint
from enum import Enum
from crocomine_client import CrocomineClient
import itertools
import subprocess


SEA = 0
LAND = 1
MAX_TERRAIN = 2


NONE = 0
SHARK = 1
TIGER = 2
CROCODILE = 3
MAX_ANIMAL = 4

CLAUSE_PER_CASE = 6


DISCOVER = 0
GUESS = 1
CHORD = 2




def createPossibilityDict(line: int, column: int) -> Dict[int, List[int]]:
    dict={}
    dict[0] = {}
    counter = 1
    for l in range(line):
        for c in range(column):
            for t in range(MAX_TERRAIN):
                for a in range(MAX_ANIMAL):
                    if((t != SEA or a != TIGER) and (t != LAND or a != SHARK)):
                        dict[counter] = [l, c, t, a]
                        counter += 1    
    return dict


def createGrid(line: int, column: int) -> List[List[Dict]]:
    li=[]
    li2=[]
    for l in range(line):
        for c in range(column):
            li2.append({"pos": [l, c], "field": "", "prox_count": (-1,-1,-1), "animal": -1})
        li.append(li2)
        li2=[]

    return li

def grid_update_infos(grid: List[List[Dict]], infos: List[Dict]):
    for info in infos:
        
        pos = info["pos"]
        grid[pos[0]][pos[1]]["field"] = info["field"]

        if "prox_count" in info:
            grid[pos[0]][pos[1]]["prox_count"] = info["prox_count"]


def grid_update_animal(grid: List[List[Dict]], i: int, j: int, animal: str):
    grid[i][j]["animal"] = animal


def unique(vars: List[int]) -> List[List[int]]:
    l=[vars]
    for a,b in itertools.combinations(vars,2):
        l.append([-a,-b])
    return l


def unique_generator(vars: Dict[int, List[int]]) -> List[List[int]]:
    li=[]
    l=[]
    for i in range(1, len(vars)+1):
        l.append(i)
        if i%CLAUSE_PER_CASE==0:
            for clause in unique(l):
                li.append(clause)
                l=[]
    return li


def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) -> str:
    p="p cnf "+str(nb_vars)+" "+str(len(clauses))
    
    inter2=""
    for clause in clauses:
        inter=""
        for variable in clause:
            inter += str(variable)+" "

        inter2 += "\n" + inter + "0"

    return p+inter2+"\n"



def infos_to_clauses(infos: List[Dict], dict: Dict) -> List[List[int]]:
    li = []
    for info in infos:
        l = []
        for i in range(1, len(dict)):
            pos = info["pos"]

            field = info["field"]
            if(field == "sea"):
                f = SEA
            if(field == "land"):
                f = LAND

            flag = True
            if "prox_count" in info:
                flag = False
            
            if(dict[i][0] == pos[0] and dict[i][1] == pos[1] and dict[i][2] == f and (dict[i][3] == NONE or flag)):
                l.append(i)

        for clause in unique(l):
            li.append(clause)
            l=[]

    return li

def base_info_field_to_clauses(noLand: bool, noSea: bool, dict: Dict) -> List[List[int]]:
    l = []

    if(noLand):
        for i in range(1, len(dict)):
            if(dict[i][2] == LAND):
                l.append([-i])

    if(noSea):
        for i in range(1, len(dict)):
            if(dict[i][2] == SEA):
                l.append([-i])

    return l


def base_info_animal_to_clauses(noShark: bool, noTiger: bool, noCrocodile: bool, dict: Dict) -> List[List[int]]:

    l = []
    for i in range(1, len(dict)):
        if(noShark):
            if(dict[i][3] == SHARK):
                l.append([-i])

        if(noTiger):
            if(dict[i][3] == TIGER):
                l.append([-i])
        
        if(noCrocodile):
            if(dict[i][3] == CROCODILE):
                l.append([-i])

    return l

def diff_list(kb: List[List[int]], add: List[List[int]]) -> List[List[int]]:
    tuple1 = [tuple(l) for l in kb]
    tuple2 = [tuple(l) for l in add]

    not_in_tuples = set(tuple2) - set(tuple1)

    return list(map(list, not_in_tuples))


def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)



def exec_gophersat(filename: str, option: str = "", cmd: str = "./gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    if option == "":
        result = subprocess.run([cmd, filename], capture_output=True, check=True, encoding=encoding)

    else:
        result = subprocess.run([cmd, option, filename], capture_output=True, check=True, encoding=encoding)

        
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

    status_new_grid = "OK"

    #while(status_new_grid != "Err")

    status_new_grid, msg, grid_infos = croco.new_grid()

    pprint(grid_infos)

    if(status_new_grid == "OK"):

        m = grid_infos['m']
        n = grid_infos['n']

        i3BV = grid_infos["3BV"]

        infos = grid_infos["infos"]

        sea_count = grid_infos["sea_count"]
        land_count = grid_infos["land_count"]
        
        shark_count = grid_infos["shark_count"]
        tiger_count = grid_infos["tiger_count"]
        croco_count = grid_infos["croco_count"]

        start = grid_infos["start"]

        dict = createPossibilityDict(m, n)

        pprint(dict)

        grid = createGrid(m, n)

        #pprint(grid)

        knowledge_base = unique_generator(dict)

        base_info_field = base_info_field_to_clauses(land_count == 0, sea_count == 0, dict)
        knowledge_base += diff_list(knowledge_base, base_info_field)

        base_info_animal = base_info_animal_to_clauses(shark_count == 0, tiger_count == 0, croco_count == 0, dict)
        knowledge_base += diff_list(knowledge_base, base_info_animal)



        if(infos):
            infos_clauses = infos_to_clauses(infos, dict)
            knowledge_base += diff_list(knowledge_base, infos_clauses)
            grid_update_infos(grid, infos)

        #pprint(knowledge_base)


        print("discover en (0,0)")
        status, msg, infos = croco.discover(start[0], start[1])
        #print(status, msg)
        #print(infos)


        if(infos):
            infos_clauses = infos_to_clauses(infos, dict)
            knowledge_base += diff_list(knowledge_base, infos_clauses)
            grid_update_infos(grid, infos)

        pprint(knowledge_base)


        while(status != "GG" and status != "KO"):

            # On fait le suivi des cases déja découvertes, on regarde la première case pas encore découverte:
            # pour chacune de ses possibilités (encore valide par exemple: on sait que c'est une case d'eau) on ajoute
            # l'inverse de la variable représentant cette possibilité à la KB et on compte le nombre de modèles

            # On fait ça pour toute les cases pas encore découverte si pour une certaine possibilité il n'y aucun modèle en retour
            # on part sur cette possibilité (on est sur que c'est la vérité),
            # dans le cas contraire on fait le choix de la possibilité pour laquel la KB nous a retourné le moins de modèle

            #write_dimacs_file(clauses_to_dimacs(knowledge_base,m*n*CLAUSE_PER_CASE), "test.cnf")

            #exec_gophersat("test.cnf")

            i = 0
            j = 0

            animal = "T"

            choice = DISCOVER
 
            if choice == DISCOVER:
                status, msg, infos = croco.discover(i, j)

            elif choice == GUESS:
                status, msg, infos = croco.guess(i, j, animal)

            elif choice == CHORD:
                status, msg, infos = croco.chord(i, j)


            if(infos):
                infos_clauses = infos_to_clauses(infos, dict)
                knowledge_base += diff_list(knowledge_base, infos_clauses)
                grid_update_infos(grid, infos)



if __name__ == "__main__":
    main()
