# ЧТЕНИЕ МАТРИЦЫ

def ReadMatrix(filename):
    matrix = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Разбиваем строку по пробелам и переводим в целые числа
                row = [int(x) for x in line.split()]
                if row:
                    matrix.append(row)
        return matrix
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден в папке с программой.")
        return None
    except ValueError:
        print(f"Ошибка: В файле {filename} есть некорректные символы (ожидаются только 0 и 1).")
        return None


# ВЫВОД МАТРИЦЫ

def PrintMatrix(m):
    print("\nМатрица отношения:")
    for row in m:
        print("  " + " ".join(str(x) for x in row))


# ПРОВЕРКА СВОЙСТВ (возвращают True/False + строка с объяснением)

def IsReflexive(m):
    for i in range(len(m)):
        if m[i][i] != 1:
            return False, f"m[{i}][{i}] = 0 (на главной диагонали есть нули)"
    return True, "все элементы на главной диагонали равны 1"


def IsIrreflexive(m):
    for i in range(len(m)):
        if m[i][i] != 0:
            return False, f"m[{i}][{i}] = 1 (на главной диагонали есть единицы)"
    return True, "все элементы на главной диагонали равны 0"


def IsSymmetric(m):
    n = len(m)
    for i in range(n):
        for j in range(n):
            if m[i][j] != m[j][i]:
                return False, f"m[{i}][{j}] = {m[i][j]}, но m[{j}][{i}] = {m[j][i]} (матрица не симметрична)"
    return True, "матрица симметрична относительно главной диагонали"


def IsAntisymmetric(m):
    n = len(m)
    for i in range(n):
        for j in range(n):
            if i != j and m[i][j] == 1 and m[j][i] == 1:
                return False, f"m[{i}][{j}]=1 и m[{j}][{i}]=1, но {i} != {j} (есть взаимная связь)"
    return True, "нет взаимных связей между разными элементами"


def IsTransitive(m):
    n = len(m)
    for i in range(n):
        for j in range(n):
            if m[i][j] == 1:
                for k in range(n):
                    if m[j][k] == 1 and m[i][k] != 1:
                        return False, f"m[{i}][{j}]=1, m[{j}][{k}]=1, но m[{i}][{k}]=0 (нет замыкания)"
    return True, "для всех путей длиной 2 есть замыкающее ребро"


def IsConnected(m):
    n = len(m)
    for i in range(n):
        for j in range(n):
            if i != j and m[i][j] == 0 and m[j][i] == 0:
                return False, f"m[{i}][{j}]=0 и m[{j}][{i}]=0 (элементы {i} и {j} не связаны)"
    return True, "любые два элемента сравнимы (есть хотя бы одна связь)"


# КЛАССИФИКАЦИЯ ОТНОШЕНИЯ

def AnalyzeRelation(m):
    if not m:
        return

    # 1. Проверка свойств (функции возвращают 2 значения: True/False + текст)
    ref, ref_msg = IsReflexive(m)
    irref, irref_msg = IsIrreflexive(m)
    sym, sym_msg = IsSymmetric(m)
    antisym, antisym_msg = IsAntisymmetric(m)
    trans, trans_msg = IsTransitive(m)
    conn, conn_msg = IsConnected(m)

    # Вывод свойств с пояснениями
    print("\nСвойства отношения:")

    print(f"  Рефлексивность:        {'Да' if ref else 'Нет'}")
    print(f"     -> Причина: {ref_msg}")

    print(f"  Антирефлексивность:    {'Да' if irref else 'Нет'}")
    print(f"     -> Причина: {irref_msg}")

    print(f"  Симметричность:        {'Да' if sym else 'Нет'}")
    print(f"     -> Причина: {sym_msg}")

    print(f"  Антисимметричность:    {'Да' if antisym else 'Нет'}")
    print(f"     -> Причина: {antisym_msg}")

    print(f"  Транзитивность:        {'Да' if trans else 'Нет'}")
    print(f"     -> Причина: {trans_msg}")

    print(f"  Связность (линейность):{'Да' if conn else 'Нет'}")
    print(f"     -> Причина: {conn_msg}")

    # 2. Классификация
    print("\nВердикт:")
    is_equivalence = ref and sym and trans
    is_strict_order = irref and trans and antisym
    is_nonstrict_order = ref and trans and antisym

    if is_equivalence:
        print("  -> Отношение является ЭКВИВАЛЕНТНОСТЬЮ")
        print("     (Рефлексивность + Симметричность + Транзитивность)")
    elif is_strict_order:
        if conn:
            print("  -> Отношение является ПОЛНЫМ (СТРОГИМ) ЛИНЕЙНЫМ ПОРЯДКОМ")
        else:
            print("  -> Отношение является СТРОГИМ ЧАСТИЧНЫМ ПОРЯДКОМ")
    elif is_nonstrict_order:
        if conn:
            print("  -> Отношение является ПОЛНЫМ (НЕСТРОГИМ) ЛИНЕЙНЫМ ПОРЯДКОМ")
        else:
            print("  -> Отношение является НЕСТРОГИМ ЧАСТИЧНЫМ ПОРЯДКОМ")
    else:
        print("  -> Отношение НЕ является ни эквивалентностью, ни отношением порядка")


# ГЛАВНОЕ МЕНЮ

def MainMenu():
    files = [f"m{i}.txt" for i in range(1, 9)]

    while True:
        print("\n╔══════════════════════════════════════════════╗")
        print("║       АНАЛИЗАТОР СВОЙСТВ ОТНОШЕНИЙ           ║")
        print("╠══════════════════════════════════════════════╣")
        print("║  Доступные матрицы:                          ║")
        for i, filename in enumerate(files, 1):
            print(f"║    {i} - {filename:<35}   ║")
        print("║    0 - Выход                                 ║")
        print("╚══════════════════════════════════════════════╝")

        choice = input("Выберите номер матрицы (или 0 для выхода): ").strip()

        if choice == "0":
            print("Завершение работы.")
            break

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(files):
                filename = files[idx - 1]
                print(f"\n>>> Выбрана матрица: {filename}")

                matrix = ReadMatrix(filename)
                if matrix:
                    PrintMatrix(matrix)
                    print("-" * 45)
                    AnalyzeRelation(matrix)
                    print("-" * 45)
            else:
                print("Ошибка: Нет файла с таким номером. Введите от 1 до 8.")
        else:
            print("Ошибка: Введите число.")


# ЗАПУСК

MainMenu()
