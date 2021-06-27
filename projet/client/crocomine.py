from os import stat
from typing import List, Tuple, Dict
from pprint import pprint
from enum import Enum
from crocomine_client import CrocomineClient
import itertools
import subprocess
import random


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


def createLocalDict(grid: List[List[Dict]]) -> Dict[int, List[int]]:

    local_dict = {}
    local_dict[0] = {}
    counter = 1
    for line in grid:
        for column in line:
            if(column["field"] != -1):
                for t in range(MAX_TERRAIN):
                    for a in range(MAX_ANIMAL):
                        if((t != SEA or a != TIGER) and (t != LAND or a != SHARK)):
                            local_dict[counter] = [column["pos"][0], column["pos"][1], t, a]
                            counter += 1    


    return local_dict

def local_dict_to_kb(local_dict: Dict[int, List[int]]) -> List[List[int]]:
    li=[]
    l=[]
    for i in range(1, len(local_dict)):
        l.append(i)
        if i%CLAUSE_PER_CASE==0:
            for clause in exactly_n(l, 1):
                li.append(clause)
            l=[]
    return li


def grid_to_clause(local_dict: Dict[int, List[int]], grid: List[List[Dict]]) -> List[List[int]]:
    li = []
    for line in grid:
        for column in line:
            l = []
            for i in range(1, len(local_dict)):
                if(local_dict[i][0] == column["pos"][0] and local_dict[i][1] == column["pos"][1]):
                    if(column["field"] == local_dict[i][2]):
                        if(column["animal"] == local_dict[i][3] or column["animal"] == -1):
                            l.append(i)

            li += diff_list(li, exactly_n(l, 1))

    return li

def prox_count_to_clause(dict: Dict, grid: List[List[Dict]], m: int, n: int) -> List[List[int]]:
    li = []
    for line in grid:
        for column in line:
            prox = []

            i =  column["pos"][0]
            j =  column["pos"][1]

            if(i + 1 < m):
                prox.append((i+1, j))
            if(j + 1 < n):
                prox.append((i, j+1))
            if(i + 1 < m and j + 1 < n):
                prox.append((i+1, j+1))
            if(i - 1 >= 0):
                prox.append((i-1, j))
            if(j - 1 >= 0):
                prox.append((i, j-1))
            if(i - 1 >= 0 and j - 1 >= 0):
                prox.append((i-1, j-1))
            if(i - 1 >= 0 and j + 1 < n):
                prox.append((i-1, j+1))
            if(i + 1 < m and j - 1 >= 0):
                prox.append((i+1, j-1))

            prox_count_tiger = column["prox_count"][0]
            prox_count_shark = column["prox_count"][1]
            prox_count_crocodile = column["prox_count"][2]


            case_croco = []
            case_shark = []
            case_tiger = []

            for a in range(1, len(dict)):
                for coord in prox:
                    if(dict[a][0] == coord[0] and dict[a][1] == coord[1]):
                        if(dict[a][3] == TIGER):
                            case_tiger.append(a)
                        
                        if(dict[a][3] == SHARK):
                            case_shark.append(a)

                        if(dict[a][3] == CROCODILE):
                            case_croco.append(a)

            prox_count_tiger_clauses = []
            prox_count_shark_clauses = []
            prox_count_crocodile_clauses = []


            if(case_tiger and prox_count_tiger != 0):
                prox_count_tiger_clauses = exactly_n(case_tiger, prox_count_tiger)

            if(case_tiger and prox_count_tiger == 0):
                for c in case_tiger:
                    prox_count_tiger_clauses += [[-c]]

            if(case_shark and prox_count_shark != 0):
                prox_count_shark_clauses = exactly_n(case_shark, prox_count_shark)
            
            if(case_shark and prox_count_shark == 0):
                for c in case_shark:
                    prox_count_shark_clauses += [[-c]]
            
            if(case_croco and prox_count_crocodile != 0):
                prox_count_crocodile_clauses = exactly_n(case_croco, prox_count_crocodile)

            if(case_croco and prox_count_crocodile == 0):
                for c in case_croco:
                    prox_count_crocodile_clauses += [[-c]]

            if(prox_count_tiger_clauses):
                li += diff_list(li, prox_count_tiger_clauses)
            if(prox_count_shark_clauses):
                li += diff_list(li, prox_count_shark_clauses)
            if(prox_count_crocodile_clauses):
                li += diff_list(li, prox_count_crocodile_clauses)

    return li



def createGrid(line: int, column: int) -> List[List[Dict]]:
    li=[]
    li2=[]
    for l in range(line):
        for c in range(column):
            li2.append({"pos": [l, c], "field": -1, "prox_count": [-1,-1,-1], "animal": -1})
        li.append(li2)
        li2=[]

    return li

def grid_update_infos(grid: List[List[Dict]], infos: List[Dict]):
    for info in infos:
        
        pos = info["pos"]

        if(info["field"] == "sea"):
            grid[pos[0]][pos[1]]["field"] = SEA

        if(info["field"] == "land"):
            grid[pos[0]][pos[1]]["field"] = LAND

        if "prox_count" in info:
            grid[pos[0]][pos[1]]["prox_count"] = info["prox_count"]
            grid[pos[0]][pos[1]]["animal"] = NONE


def grid_update_animal(grid: List[List[Dict]], i: int, j: int, animal: int):
    grid[i][j]["animal"] = animal


def at_least_n(vars: List[int], n: int) -> List[List[int]]:
    result = []
    size = len(vars)
    temp = itertools.combinations(vars, size-(n-1))
    for a in temp:
        oneTab = []
        for b in a:
            oneTab.append(b)
        result.append(oneTab)
    return result

def max_n(vars: List[int], n: int) -> List[List[int]]:
    result = []
    temp = itertools.combinations(vars, n+1)
    for a in temp:
        oneTab = []
        for b in a:
            oneTab.append(-b)
        result.append(oneTab)
    return result

def exactly_n(vars: List[int], n: int) -> List[List[int]]:
    result = []
    for val in at_least_n(vars, n):
        result.append(val)
    for val in max_n(vars, n):
        result.append(val)
    return result


def dict_to_kb(vars: Dict[int, List[int]]) -> List[List[int]]:
    li=[]
    l=[]
    for i in range(1, len(vars)):
        l.append(i)
        if i%CLAUSE_PER_CASE==0:
            for clause in exactly_n(l, 1):
                li.append(clause)
            l=[]
    return li

"""
def local_dict_to_kb(dict: Dict[int, List[int]]) -> List[List[int]]:
    li = []
    l = []

    coord = [-1,-1]

    for i in range(1, len(dict)):
        if(coord != [dict[i][0], dict[i][1]] and coord != [-1,-1]):
            for clause in exactly_n(l, 1):
                li.append(clause)
            l = []
        coord = [dict[i][0], dict[i][1]]
        l.append(i)

        if(i == len(dict)-1):
            for clause in exactly_n(l, 1):
                li.append(clause)


    return li
"""



def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) -> str:
    p="p cnf "+str(nb_vars)+" "+str(len(clauses))
    
    inter2=""
    for clause in clauses:
        inter=""
        for variable in clause:
            inter += str(variable)+" "

        inter2 += "\n" + inter + "0"

    return p+inter2+"\n"



def infos_to_clauses(infos: List[Dict], dict: Dict, m: int, n: int) -> List[List[int]]:
    li = []
    for info in infos:
        l = []
        pos = info["pos"]

        i = pos[0]
        j = pos[1]

        field = info["field"]
        if(field == "sea"):
            f = SEA
        if(field == "land"):
            f = LAND

        prox_count_clauses = []
        flag = True
        if "prox_count" in info:
            flag = False
            prox_count_clauses = prox_count_to_clause(info["prox_count"], dict, i, j, m, n)

        for k in range(1, len(dict)):
            if(dict[k][0] == i and dict[k][1] == j and dict[k][2] == f and (dict[k][3] == NONE or flag)):
                l.append(k)
                

        for clause in exactly_n(l, 1):
            li.append(clause)

        li += diff_list(li, prox_count_clauses)
        

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


def counter_info_to_clauses(tiger_count: int, shark_count: int, croco_count: int, dict: Dict) -> List[List[int]]:
    case_tiger = []
    case_shark = []
    case_croco = []

    clauses_tiger = []
    clauses_shark = []
    clauses_croco = []
    
    for i in range(1, len(dict)):
        if(tiger_count != 0 and dict[i][3] == TIGER):
                case_tiger.append(i)

        if(shark_count != 0 and dict[i][3] == SHARK):
            case_shark.append(i)

        if(case_croco != 0 and dict[i][3] == CROCODILE):
            case_croco.append(i)


    print(case_shark)

    
    
    if(tiger_count != 0):
       clauses_tiger = exactly_n(case_tiger, tiger_count)

    if(shark_count != 0):
       clauses_shark = exactly_n(case_shark, shark_count)

    if(croco_count != 0):
       clauses_croco = exactly_n(case_croco, croco_count)

    return clauses_tiger+clauses_shark+clauses_croco

    


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

def exec_gophersat_count(filename: str, cmd: str = "./gophersat", encoding: str = "utf8") -> int:

    result = subprocess.run([cmd, "-count", filename], capture_output=True, check=True, encoding=encoding)

    string = str(result.stdout)
    lines = string.splitlines()

    return int(lines[1])



def main():
    server = "http://localhost:8000"
    group = "Groupe 35"
    members = "Benjamin et Enzo"
    croco = CrocomineClient(server, group, members, "enzobenjam")
    #"http://croco.lagrue.ninja:80"
    status_new_grid = "OK"

    while(status_new_grid != "Err"):

        status_new_grid, msg, grid_infos = croco.new_grid()

        #pprint(grid_infos)

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


            shark_counter = 0
            tiger_counter = 0
            croco_counter = 0

            start = grid_infos["start"]

            dict = createPossibilityDict(m, n)

            #pprint(dict)

            grid = createGrid(m, n)

            #pprint(grid)

            knowledge_base = dict_to_kb(dict)

            base_info_field = base_info_field_to_clauses(land_count == 0, sea_count == 0, dict)
            knowledge_base += diff_list(knowledge_base, base_info_field)

            base_info_animal = base_info_animal_to_clauses(shark_count == 0, tiger_count == 0, croco_count == 0, dict)
            knowledge_base += diff_list(knowledge_base, base_info_animal)


            #counter_info = counter_info_to_clauses(tiger_count, shark_count, croco_count, dict)
            
            #print("counter")
            #pprint(counter_info)

            #knowledge_base += diff_list(knowledge_base, counter_info)

         


            if(infos):
                #infos_clauses = infos_to_clauses(infos, dict, m, n)
                #knowledge_base += diff_list(knowledge_base, infos_clauses)
                grid_update_infos(grid, infos)

            #pprint(knowledge_base)


            print("discover en (0,0)")
            status, msg, infos = croco.discover(start[0], start[1])
            print(status, msg)
            print(infos)


            if(infos):
                #infos_clauses = infos_to_clauses(infos, dict, m, n)
                #knowledge_base += diff_list(knowledge_base, infos_clauses)
                grid_update_infos(grid, infos)

            #pprint(knowledge_base)


            while(status != "GG" and status != "KO" and status != "Err"):



                # On fait le suivi des cases déja découvertes, on regarde la première case pas encore découverte:
                # pour chacune de ses possibilités (encore valide par exemple: on sait que c'est une case d'eau) on ajoute
                # l'inverse de la variable représentant cette possibilité à la KB et on compte le nombre de modèles

                # On fait ça pour toute les cases pas encore découverte si pour une certaine possibilité il n'y aucun modèle en retour
                # on part sur cette possibilité (on est sur que c'est la vérité),
                # dans le cas contraire on fait le choix de la possibilité pour laquel la KB nous a retourné le moins de modèle

                #write_dimacs_file(clauses_to_dimacs(knowledge_base,m*n*CLAUSE_PER_CASE), "test.cnf")

                #exec_gophersat("test.cnf")

                i = -1
                j = -1
                animal =""
                choice = DISCOVER

                value = -1
                min = float('inf')

                #on remplit notre local Kb avec tout les modèles possible pour les cases déja découverte, ou adjacentes
                local_dict = createLocalDict(grid)

                pprint(local_dict)

                #on ajoute dans la local les infos qu'on a, on élimine  certaine possibilité avec des unique, exactly_n
                local_kb = local_dict_to_kb(local_dict)
                
                print("local_dict_to_kb")
                pprint(local_kb)

                
                grid_clauses = grid_to_clause(local_dict, grid)
                local_kb += diff_list(local_kb, grid_clauses)
                
                print("grid_to_clause")
                pprint(grid_clauses)


                prox_clauses = prox_count_to_clause(local_dict, grid, m, n)

                local_kb += diff_list(local_kb, prox_clauses)

                print("prox_count_to_clause")
                pprint(prox_clauses)


                #pprint(local_kb)



                #on parcours la grid, pour toutes les carte pas encore découverte et ou on connait le type de terrain on ajoute l'inverse
                #de chaque varable propo possible une a à une a la kb, on test avec gophersat, et on retient le la possibilité qui renvoie le moins de modèle.

                temp_kb = [x for x in local_kb if x]

                for line in grid:
                    if(min == 0):
                        break
                    for column in line:
                        if(min == 0):
                            break
                        if(column["field"] != -1 and column["animal"] == -1):
                            pprint(grid)
                            print(column["field"], column["animal"])
                            pos = column["pos"]
                            pprint(column["pos"])
                            l = []

                            for i in range(1, len(local_dict)):
                                if(local_dict[i][0] == pos[0] and local_dict[i][1] == pos[1]):
                                    l.append(i)

                            temp_kb
                            
                            print(l)
                            for possibility in l:
                                
                                write_dimacs_file(clauses_to_dimacs(temp_kb + [[-possibility]],len(local_dict)-1), "test.cnf")
                                c = exec_gophersat_count("test.cnf")

                                if(c < min):
                                    min = c
                                    value = possibility
                                
                                if(min == 0):
                                    break

                print(min, value)
                
                i = local_dict[value][0]
                j = local_dict[value][1]

                if(local_dict[value][3] == TIGER):
                    choice = GUESS
                    animal = "T"

                if(local_dict[value][3] == SHARK):
                    choice = GUESS
                    animal = "S"

                if(local_dict[value][3] == CROCODILE):
                    choice = GUESS
                    animal = "C"
    
                if choice == DISCOVER:
                    print("discover en ("+str(i)+","+str(j)+")")
                    status, msg, infos = croco.discover(i, j)

                elif choice == GUESS:
                    print("guess en ("+str(i)+","+str(j)+","+animal+")")
                    status, msg, infos = croco.guess(i, j, animal)

                    if(status == "OK"):
                        if(animal == "T"):
                            a = TIGER
                        if(animal == "S"):
                            a = SHARK
                        if(animal == "C"):
                            a = CROCODILE

                        grid_update_animal(grid, i, j, a)

                elif choice == CHORD:
                    status, msg, infos = croco.chord(i, j)

                print(status, msg)
                print(infos)


                if(infos):
                    #infos_clauses = infos_to_clauses(infos, dict, m, n)
                    #knowledge_base += diff_list(knowledge_base, infos_clauses)
                    grid_update_infos(grid, infos)



if __name__ == "__main__":
    main()




"""

                compteur = 1

                local_dict = {}

                local_dict[0] = {}

                l = [] #contient les positions des cases découverte
                for line in grid:
                    for column in line:
                        if(column["animal"] != -1):
                            l.append(column["pos"])
                            local_dict[compteur] = [column["pos"][0], column["pos"][1], column["field"], column["animal"]]
                            compteur += 1
                            

                print(l)

                voisinage = []
                
                for pos in l:

                    i = pos[0]
                    j = pos[1]

                    if(i + 1 < m and grid[i+1][j]["animal"] == -1):
                        voisinage += diff_list(voisinage, [[i+1, j]])

                    if(j + 1 < n and grid[i][j+1]["animal"] == -1):
                        voisinage += diff_list(voisinage, [[i, j+1]])

                    if(i + 1 < m and j + 1 < n and grid[i+1][j+1]["animal"] == -1):
                        voisinage += diff_list(voisinage, [[i+1, j+1]])
                    
                    if(i - 1 >= 0 and grid[i-1][j]["animal"] == -1):
                        voisinage += diff_list(voisinage, [[i-1, j]])
                    
                    if(j - 1 >= 0 and grid[i][j-1]["animal"] == -1):
                        voisinage += diff_list(voisinage, [[i, j-1]])
                    
                    if(i - 1 >= 0 and j - 1 >= 0 and grid[i-1][j-1]["animal"] == -1):
                        voisinage += diff_list(voisinage, [[i-1, j-1]])
                    
                    if(i - 1 >= 0 and j + 1 < n and grid[i-1][j+1]["animal"] == -1):
                        voisinage += diff_list(voisinage, [[i-1, j+1]])
                    
                    if(i + 1 < m and j - 1 >= 0 and grid[i+1][j-1]["animal"] == -1):
                        voisinage += diff_list(voisinage, [[i+1, j-1]])


                print(voisinage)

                for case in voisinage:
                    if(grid[case[0]][case[1]]["field"] == SEA):
                        for i in range(MAX_ANIMAL):
                            if(i != TIGER):
                                local_dict[compteur] = [case[0], case[1], SEA, i]
                                compteur += 1
                    
                    if(grid[case[0]][case[1]]["field"] == LAND):
                        for i in range(MAX_ANIMAL):
                            if(i != SHARK):
                                local_dict[compteur] = [case[0], case[1], LAND, i]
                                compteur += 1


                


                pprint(local_dict)


                local_knowledge_base = local_dict_to_kb(local_dict)


                pprint(local_knowledge_base)

                input('suivant')


                #on créer un nouveau fichier .cnf dans lequel on indique les cases connues et on test une par une l'inverse des varaibles propositionnelles représentant l'état des cases inconnus
                # on execute a chaque fois gophersat en comptant, sur toutes les cases testé on execute le coup pour lequel il y avait le moins de modèles 

                for case in voisinage:
                    for i in range(1, len(dict)):
                        if(dict[i][0] == case[0] and dict[i][1] == case[1]):
                            l.append(i)

                    for possibility in l:
                        
                        write_dimacs_file(clauses_to_dimacs(local_knowledge_base + [[-possibility]],m*n*CLAUSE_PER_CASE), "test.cnf")
                        c = exec_gophersat_count("test.cnf")

                        print(c, possibility)

                        if(c < min):
                            min = c
                            value = possibility
                        
                        if(min == 0):
                            break
"""