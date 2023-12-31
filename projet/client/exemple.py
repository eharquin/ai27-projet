from pprint import pprint
from crocomine_client import CrocomineClient

def test():
    server = "http://localhost:8000"
    group = "Groupe "
    members = "Benjamin et Enzo"
    croco = CrocomineClient(server, group, members)

    status, msg, grid_infos = croco.new_grid()
    print(status, msg)
    pprint(grid_infos)

    print("discover en (0,0)")
    status, msg, infos = croco.discover(0, 0)
    print(status, msg)
    pprint(infos)

    status, msg, grid_infos = croco.new_grid()
    print(msg, status)
    pprint(grid_infos)
    

    print("guess en (1, 2, T)")
    status, msg, infos = croco.guess(1, 2, "T")
    print(status, msg)
    pprint(infos)

    print("discover en (0, 2)")
    status, msg, infos = croco.discover(0, 2)
    print(status, msg)
    pprint(infos)

    print("chord en (0, 2)")
    status, msg, infos = croco.chord(0, 2)
    print(status, msg)
    pprint(infos)

    print("chord en (0, 0)")
    status, msg, infos = croco.discover(0, 0)
    print(status, msg)
    pprint(infos)


    status, msg, grid_infos = croco.new_grid()
    print(status, msg)
    pprint(grid_infos)

    status, msg, infos = croco.discover(0, 4)
    print(status, msg)
    pprint(infos)

    status, msg, infos = croco.guess(3, 6, "T")
    print(status, msg)
    pprint(infos)

    status, msg, grid_infos = croco.new_grid()
    print(status, msg)
    pprint(grid_infos)

    status, msg, infos = croco.guess(3, 6, "T")
    print(status, msg)
    pprint(infos)

    status, msg, grid_infos = croco.new_grid()
    print(status, msg)
    pprint(grid_infos)


if __name__ == "__main__":
    test()
