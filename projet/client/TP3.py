# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:34:01 2021

@author: benja
"""

from typing import List, Tuple
import itertools
import subprocess


def cell_to_variable(i: int, j: int, val: int) -> int:
    var=i*81+j*9+val
    return var

print(cell_to_variable(0, 1, 9))
print(cell_to_variable(1, 0, 8))

def variable_to_cell(lit: int) -> Tuple[int, int, int]:
    if(lit<=9):
        t=(0,0,lit)
    elif(lit<=81):
        col=lit//9
        val=lit-9*col
        if val==0:
            col=col-1
            val=val+9
        t=(0,col,val)
    else:
        lin=lit//81
        col=(lit-81*lin)//9
        val=lit-81*lin-9*col
        if val==0:
            lin=lin-1
            if col==0:
               col=col+8 
            val=val+9
        t=[lin,col,val]
    return t

print(variable_to_cell(90))

def at_least_one(vars: List[int]) -> List[int]:
    liste=vars
    return liste

print(at_least_one([1,3,4]))

def unique(vars: List[int]) -> List[List[int]]:
    l=[vars]
    for a,b in itertools.combinations(vars,2):
        l.append([-a,-b])
    return l

print(unique([1,3,5]))

def create_cell_constraints() -> List[List[int]]:
    l=[]
    for i in range(730):
        if i!=0:
            l.append(unique(variable_to_cell(i)))
    return l

print("gfjsdgnfkjdsnhùkgjdnhfkg")
print(create_cell_constraints())
print("gfjsdgnfkjdsnhùkgjdnhfkg")

def create_line_constraints() -> List[List[int]]:
    l=[]
    i=0
    j=0
    for i in range(9):
        l1=[]
        for j in range(82):
            
            l1.append(at_least_one(variable_to_cell(81*i+j)))
        l.append(l1)
    return l    

"""print(create_line_constraints())"""

def create_column_constraints() -> List[List[int]]:
    l=[]
    for h in range(9):
        l1=[]
        for i in range(9):
            for j in range(10):
                if j!=0:
                    l1.append(at_least_one(variable_to_cell(9*h+81*i+j)))                
        l.append(l1)
    return l    

"""print(create_column_constraints())"""

def create_box_constraints() -> List[List[int]]:
    l=[]
    decalageligne=0
    decalagecolonne=0
    while decalagecolonne!=3 or decalageligne!=3:
        if decalagecolonne<3:
            decalagecolonne+=1
        else:
            decalagecolonne=1
            decalageligne+=1
        for h in range(3*decalageligne):
            if h>=3*(decalageligne-1):
                l1=[]
                for i in range(3*decalagecolonne):
                    if i>=3*(decalagecolonne-1):
                        for j in range(10):
                            if j!=0:
                                l1.append(at_least_one(variable_to_cell(9*h+81*i+j)))  
                l.append(l1)
    return l   

"""print(create_box_constraints())"""

Grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

def create_value_constraints(grid: List[List[int]]) -> List[List[int]]:
    l=[]
    i=0
    j=0
    for ligne in grid:
        for cell in ligne:
            l.append([j,i,cell])
            i=i+1
            if i>8:
                i=0
        j=j+1
    return l

"""print(create_value_constraints(Grid))"""

def generate_problem(grid: List[List[int]]) -> List[List[int]]:
    l=[]
    l.append(create_value_constraints(grid))
    l.append(create_box_constraints())
    l.append(create_column_constraints())
    l.append(create_line_constraints())
    l.append(create_cell_constraints())
    return l

print(generate_problem(Grid))

def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) -> str:
    p="p cnf "+str(nb_vars)
    inter=""
    inter2=""
    i=0
    for clause in clauses:
       i=i+1
       inter=""
       for variable in clause:
           inter=inter+" "+str(variable)
       inter2=inter2 + "\n" + inter + " 0"   
    p=p+" "+str(i)+inter2+" \n"
    return p

"""print(clauses_to_dimacs([[-1, -2], [1, 2], [1, 3], [2, 4], [-3, 4], [-4, 5]],5))"""

def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)

def exec_gophersat(filename: str, cmd: str = "gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    result = subprocess.run([cmd, filename], capture_output=True, check=True, encoding=encoding)
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:].split(" ")

    return True, [int(x) for x in model]
    
def main():
    """write_dimacs_file(clauses_to_dimacs([[-1, -2], [1, 2], [1, 3], [2, 4], [-3, 4], [-4, 5]],5), "sudoku")"""
    exec_gophersat(r"C:\Users\benja\Desktop\Cours" "UTC\AI27\sudoku.cnf")
    
"""if __name__ == "__main__":
    main()"""