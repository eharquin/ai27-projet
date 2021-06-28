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


"""
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
    li = []
    l = []
    for i in range(1, len(local_dict)):
        l.append(i)
        if i % CLAUSE_PER_CASE == 0:
            for clause in exactly_n(l, 1):
                li.append(clause)
            l = []
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



def counter_to_clause(dict: Dict, grid: List[List[Dict]], shark_count: int, croco_count: int, tiger_count: int, shark_counter: int, croco_counter: int, tiger_counter: int) -> List[List[int]]:
    li = []

    for a in range(1, len(dict)):
        if((dict[a][3] == TIGER and tiger_count == tiger_counter) and grid[dict[a][0]][dict[a][1]]["animal"] == -1):
            li += [[-a]]

        if((dict[a][3] == SHARK and shark_count == shark_counter) and grid[dict[a][0]][dict[a][1]]["animal"] == -1):
            li += [[-a]]

        if((dict[a][3] == CROCODILE and croco_count == croco_counter) and grid[dict[a][0]][dict[a][1]]["animal"] == -1):
            li += [[-a]]

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



def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) -> str:
    p="p cnf "+str(nb_vars)+" "+str(len(clauses))
    
    inter2=""
    for clause in clauses:
        inter=""
        for variable in clause:
            inter += str(variable)+" "

        inter2 += "\n" + inter + "0"

    return p+inter2+"\n"


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

            grid = createGrid(m, n)


            if(infos):
                grid_update_infos(grid, infos)


            status, msg, infos = croco.discover(start[0], start[1])

            if(infos):
                grid_update_infos(grid, infos)


            while(status != "GG" and status != "KO" and status != "Err"):

                local_dict = createLocalDict(grid)


                local_kb = local_dict_to_kb(local_dict)
                
                
                grid_clauses = grid_to_clause(local_dict, grid)
                local_kb += diff_list(local_kb, grid_clauses)
                

                counter_clauses = counter_to_clause(local_dict, grid, shark_count, croco_count, tiger_count, shark_counter, croco_counter, tiger_counter)
                local_kb += diff_list(local_kb, counter_clauses)


                prox_clauses = prox_count_to_clause(local_dict, grid, m, n)
                local_kb += diff_list(local_kb, prox_clauses)


                # On retire les eventuelles listes vide
                temp_kb = [x for x in local_kb if x]

                value = -1
                min = float('inf')

                # On cherche un UNSAT
                UNSAT = False
                for line in grid:
                    if(UNSAT == True):
                        break
                    for column in line:
                        if(UNSAT == True):
                            break
                        if(column["field"] != -1 and column["animal"] == -1):
                            pos = column["pos"]
                            l = []

                            for i in range(1, len(local_dict)):
                                if(local_dict[i][0] == pos[0] and local_dict[i][1] == pos[1]):
                                    l.append(i)
                            
                            for possibility in l:
                                
                                write_dimacs_file(clauses_to_dimacs(temp_kb + [[-possibility]],len(local_dict)-1), "test.cnf")
                                ret, model = exec_gophersat("test.cnf")

                                if(ret == False):
                                    UNSAT = True
                                    value = possibility
                                    break

                # SI on ne trouve pas de UNSAT on cherche le plus petit nombre de modèle
                if(UNSAT == False):
                    for line in grid:
                        if(min == 1):
                            break
                        for column in line:
                            if(min == 1):
                                break
                            if(column["field"] != -1 and column["animal"] == -1):
                                pos = column["pos"]
                                l = []

                                for i in range(1, len(local_dict)):
                                    if(local_dict[i][0] == pos[0] and local_dict[i][1] == pos[1]):
                                        l.append(i)
                                
                                for possibility in l:
                                    
                                    write_dimacs_file(clauses_to_dimacs(temp_kb + [[-possibility]],len(local_dict)-1), "test.cnf")
                                    c = exec_gophersat_count("test.cnf")

                                    if(c < min):
                                        min = c
                                        value = possibility
                                    
                                    if(min == 1):
                                        break

                
                i = local_dict[value][0]
                j = local_dict[value][1]
                animal = ""
                choice = DISCOVER

                if(local_dict[value][3] == TIGER):
                    choice = GUESS
                    animal = "T"
                    tiger_counter += 1

                if(local_dict[value][3] == SHARK):
                    choice = GUESS
                    animal = "S"
                    shark_counter += 1

                if(local_dict[value][3] == CROCODILE):
                    choice = GUESS
                    animal = "C"
                    croco_counter += 1
    
                if choice == DISCOVER:
                    status, msg, infos = croco.discover(i, j)

                elif choice == GUESS:
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



                if(infos):
                    grid_update_infos(grid, infos)



if __name__ == "__main__":
    main()
    