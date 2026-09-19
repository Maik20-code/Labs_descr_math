from random import randint

A = set()
B = set()
C = set()
U = set(range(-30,31))
MAX_SIZE=10

def Format_list(l):
    if len(l) == 0:
        return {0}
    return l

def Action():
    m = input("Выберите действие: ").lower()
    match m:
        case "print": Print()
        case "rand": Rand()
        case "end":
            print("Завершение программы")
            return
        case "add": Add()
        case "rand_all": Rand_all()
        case "print_full": Print_full()
        case "rand_full": Rand_full()
        case "del": Del()
        case "clear": Clear()
        case "clear_all": Clear_all()
        case "opers":  Operations()
        case _:
            print("Нет такого действия!")
            Action()
    print("====================================")

def Add():
    m = input("В какое множество хотите добавить число? ").lower()
    match m:
        case "a": lst = A
        case "b": lst = B
        case "c": lst = C
        case _:
            print("Нет такого множества!")
            return Action()

    if len(lst) >= MAX_SIZE:
        print("Множество", m.upper(), "уже заполнено!")
        return Action()

    c = int(input("Введите желаемое кол-во чисел: "))
    space_left = MAX_SIZE - len(lst)
    if c > space_left:
        print("Возможно добавить только", space_left, "чисел")
        c = space_left

    for i in range(c):
        n = int(input(f"Введите {i+1} число: "))
        if not (-30 <= n <= 30):
            print("Число не принадлежит U")
            continue
        lst.add(n)
        print("Число", n, "добавлено в множество", m)

    Action()

def Rand():
    n = randint(-30, 30)
    m = input("Выберите множество: ").lower()
    match m:
        case "a":
            if len(A) < MAX_SIZE:
                A.add(n)
                print("число", n, "было добавлено в множество", m)
            else:
                print("Множество A заполнено!")
        case "b":
            if len(B) < MAX_SIZE:
                B.add(n)
                print("число", n, "было добавлено в множество", m)
            else:
                print("Множество B заполнено!")
        case "c":
            if len(C) < MAX_SIZE:
                C.add(n)
                print("число", n, "было добавлено в множество", m)
            else:
                print("Множество C заполнено!")
        case _:
            print("Нет такого множества")
    Action()

def Rand_full():
    space_leftA = MAX_SIZE - len(A)
    space_leftB = MAX_SIZE - len(B)
    space_leftC = MAX_SIZE - len(C)
    if space_leftA > 0:
        for i in range(space_leftA):
            A.add(randint(-30, 30))
    if space_leftB > 0:
        for i in range(space_leftB):
            B.add(randint(-30, 30))
    if space_leftC > 0:
        for i in range(space_leftC):
            C.add(randint(-30, 30))
    print("Множество А:", A)
    print("Множество B:", B)
    print("Множество C:", C)
    Action()

def Rand_all():
    m = input("Какое множество хотите заполнить? ").lower()
    match m:
        case "a":
            space_left = MAX_SIZE - len(A)
            if space_left > 0:
                for i in range(space_left):
                    A.add(randint(-30, 30))
                print("Множество А:", A)
            else:
                print("Множество A уже заполнено!")
        case "b":
            space_left = MAX_SIZE - len(B)
            if space_left > 0:
                for i in range(space_left):
                    B.add(randint(-30, 30))
                print("Множество B:", B)
            else:
                print("Множество B уже заполнено!")
        case "c":
            space_left = MAX_SIZE - len(C)
            if space_left > 0:
                for i in range(space_left):
                    C.add(randint(-30, 30))
                print("Множество C:", C)
            else:
                print("Множество C уже заполнено!")
        case _:
            print("Нет такого множества!")
    Action()

def Print():
    m = input("Какое множество вывести на экран? ").lower()
    match m:
        case "a": print("множество A:", sorted(Format_list(A)))
        case "b": print("множество B:", sorted(Format_list(B)))
        case "c": print("множество C:", sorted(Format_list(C)))
        case _: print("Нет такого множества")
    Action()

def Print_full():
    print("Множество А:", Format_list(A))
    print("Множество B:", Format_list(B))
    print("Множество C:", Format_list(C))
    Action()

def Clear():
    m = input("Какое множество хотите очистить? ").lower()
    match m:
        case "a":
            A.clear()
            print("Множество A очищенно")
        case "b":
            B.clear()
            print("Множество B очищенно")
        case "c":
            C.clear()
            print("Множество C очищенно")
        case _:
            print("Нет такого множества")
    Action()

def Clear_all():
    A.clear()
    B.clear()
    C.clear()
    print("Все множества очищенны")
    Print_full()

def Del():
    m = input("Из какого множества хотите удалить число? ").lower()
    n = int(input("Введите число: "))
    match m:
        case "a":
            if n in A:
                A.remove(n)
                print("число", n, "удалено из множества", m)
            else:
                print("числа", n, "нет в множестве", m)
        case "b":
            if n in B:
                B.remove(n)
                print("число", n, "удалено из множества", m)
            else:
                print("числа", n, "нет в множестве", m)
        case "c":
            if n in C:
                C.remove(n)
                print("число", n, "удалено из множества", m)
            else:
                print("числа", n, "нет в множестве", m)
        case _:
            print("Такого множества нет!")
    Action()

def Operations():
    while True:
        print("Выберите операцию:")
        print("1 - Пересечение (A ∩ B)")
        print("2 - Объединение (A ∪ B)")
        print("3 - Разность (A \\ B)")
        print("4 - Симметрическая разность (A △ B)")
        print("5 - Дополнение (U \\ A)")
        print("0 - Назад в главное меню")

        op = input("Введите номер операции: ")

        if op == "0":
            Legenda()
            return Action()
        if op == "5":
            m = input("Выберите множество (a, b, c): ").lower()
            match m:
                case "a": source = A
                case "b": source = B
                case "c": source = C
                case _:
                    print("Нет такого множества!")
                    continue
            result = set()
            for x in U:
                if x not in source:
                    result.add(x)
            print(f"Дополнение {m.upper()} = U \\ {m.upper()}:")
            print(sorted(result))
            print(f"Мощность: {len(result)}")
            print("==========================")
            continue

        if op not in ("1", "2", "3", "4"):
            print("Нет такой операции")
            continue
        m1 = input("Выберите первое множество: ").lower()
        m2 = input("Выберите второе множество: ").lower()
        match m1:
            case "a": set1 = A
            case "b": set1 = B
            case "c": set1 = C
            case _:
                print("Нет такого множества!")
                continue
        match m2:
            case "a": set2 = A
            case "b": set2 = B
            case "c": set2 = C
            case _:
                print("Нет такого множества!")
                continue

        result = set()
        if op == "1":
            for x in set1:
                if x in set2:
                    result.add(x)
            print(f"{m1.upper()} ∩ {m2.upper()} =", sorted(result))
        elif op == "2":
            for x in set1:
                result.add(x)
            for x in set2:
                if x not in result:
                    result.add(x)
            print(f"{m1.upper()} ∪ {m2.upper()} =", sorted(result))
        elif op == "3":
            for x in set1:
                if x not in set2:
                    result.add(x)
            print(f"{m1.upper()} \\ {m2.upper()} =", sorted(result))
        elif op == "4":
            for x in set1:
                if x not in set2:
                    result.add(x)
            for x in set2:
                if x not in set1:
                    result.add(x)
            print(f"{m1.upper()} △ {m2.upper()} =", sorted(result))
        print("==========================")


def Legenda():
    print("================================================= \n"
          "print - вывести числа из множества на экран \n"
          "print_full - вывести все множества на экран \n"
          "add - добавить n числ в множество вручную (U=(-30,30)) \n"
          "rand - добавить случайное число в множество (U=(-30,30)) \n"
          "rand_all - заполнить множество случайными числами  \n"
          "rand_full - заполнить все множества случайными числами \n"
          "del - удалить выбранное число из множества \n"
          "clear - очистить выбранное множество \n"
          "clear_all - очистить все множества \n"
          "end - завершить работу программы \n"
          "opers - операции над множествами \n" 
          "=================================================")
    Action()

Legenda()