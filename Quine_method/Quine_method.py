# ВВОД И ПРОВЕРКА ВЕКТОРА

def ReadVector():
    print("Введите вектор функции (16 символов 0 и 1).")
    print("Можно разделять пробелами каждые 4 символа.")
    print("Пример: 1010 0101 1111 0000")

    raw = input("Ваш вектор: ")

    clean = ""
    for ch in raw:
        if ch == '0' or ch == '1':
            clean += ch

    if len(clean) != 16:
        print("Ошибка: нужно ввести ровно 16 цифр.")
        return None
    return clean


# ПЕРЕВОД ЧИСЛА В ДВОИЧНЫЙ КОД (4 бита)

def ToBinary(n):
    res = ""
    for i in range(4):
        bit = n % 2
        res = str(bit) + res
        n = n // 2
    return res


# ТАБЛИЦА ИСТИННОСТИ

def PrintTable(v):
    print("\n--- Таблица истинности ---")
    print(" A B C D | F")
    print("---------|---")
    for i in range(16):
        b = ToBinary(i)
        print(" " + b[0] + " " + b[1] + " " + b[2] + " " + b[3] + " | " + v[i])


# СДНФ

def GetSDNF(v):
    vars = ['A', 'B', 'C', 'D']
    terms = []

    for i in range(16):
        if v[i] == '1':
            b = ToBinary(i)
            term = ""
            for j in range(4):
                if j > 0:
                    term += "*"
                if b[j] == '1':
                    term += vars[j]
                else:
                    term += "!" + vars[j]
            terms.append(term)

    if len(terms) == 0:
        return "0"

    res = terms[0]
    for i in range(1, len(terms)):
        res += " + " + terms[i]
    return res


# МЕТОД КВАЙНА (Полный вывод процесса)

def Combine(s1, s2):
    # Пытаемся склеить две строки. Если отличаются на 1 символ - возвращает результат, иначе - None
    diff = 0
    res = ""
    for i in range(4):
        if s1[i] != s2[i]:
            diff += 1
            res += "-"
        else:
            res += s1[i]

    if diff == 1:
        return res
    return None


def Covers(imp, m):
    # Проверяем, покрывает ли импликанта (с дефисами) конкретный минтерм
    for i in range(4):
        if imp[i] != '-' and imp[i] != m[i]:
            return False
    return True


def Quine(v):
    # 1. Собираем начальные конъюнкции (где F=1)
    minterms = []
    for i in range(16):
        if v[i] == '1':
            minterms.append(ToBinary(i))

    if len(minterms) == 0:
        print("\nФункция тождественно ложна (0).")
        return

    print("\n--- Результаты неполных склеиваний ---")
    current_level = minterms
    prime_implicants = []
    step = 1

    while True:
        used = [False] * len(current_level)
        next_level = []
        combined_any = False

        print(f"Шаг {step}:")
        for i in range(len(current_level)):
            for j in range(i + 1, len(current_level)):
                combined = Combine(current_level[i], current_level[j])
                if combined is not None:
                    print(f"  {current_level[i]} + {current_level[j]} -> {combined}")
                    used[i] = True
                    used[j] = True
                    combined_any = True
                    if combined not in next_level:
                        next_level.append(combined)

        if not combined_any:
            break

        # Те, что не склеились - это простые импликанты
        for i in range(len(current_level)):
            if not used[i]:
                if current_level[i] not in prime_implicants:
                    prime_implicants.append(current_level[i])

        current_level = next_level
        step += 1

    # Добавляем последний уровень (если он остался)
    for term in current_level:
        if term not in prime_implicants:
            prime_implicants.append(term)

    # 2. Строим Импликантную матрицу
    print("\n--- Импликантная матрица (Таблица Квайна) ---")

    # Шапка таблицы
    header = "Импликанты |"
    for m in minterms:
        header += f" {m} |"
    print(header)
    print("-" * len(header))

    matrix = []
    for p in prime_implicants:
        row_str = f"  {p:<8} |"
        row_vals = []
        for m in minterms:
            if Covers(p, m):
                row_str += "  X   |"
                row_vals.append(1)
            else:
                row_str += "  .   |"
                row_vals.append(0)
        matrix.append(row_vals)
        print(row_str)

    # 3. Поиск существенных импликант (МДНФ)
    print("\n--- Поиск минимального покрытия ---")
    essential = []
    covered = [False] * len(minterms)

    # Ищем столбцы, где только одна "X"
    for j in range(len(minterms)):
        count = 0
        last_row = -1
        for i in range(len(prime_implicants)):
            if matrix[i][j] == 1:
                count += 1
                last_row = i

        if count == 1:
            # Эта импликанта обязательна!
            imp = prime_implicants[last_row]
            if imp not in essential:
                essential.append(imp)
                print(f"  Минтерм {minterms[j]} покрывается только импликантой {imp}. Она обязательна.")
                # Вычеркиваем покрытые минтермы
                for k in range(len(minterms)):
                    if matrix[last_row][k] == 1:
                        covered[k] = True

    # Если остались непокрытые, добавляем любые подходящие
    for j in range(len(minterms)):
        if not covered[j]:
            for i in range(len(prime_implicants)):
                if matrix[i][j] == 1:
                    imp = prime_implicants[i]
                    if imp not in essential:
                        essential.append(imp)
                        print(f"  Для покрытия {minterms[j]} добавлена импликанта {imp}.")
                    for k in range(len(minterms)):
                        if matrix[i][k] == 1:
                            covered[k] = True
                    break

    # 4. Вывод МДНФ
    print("\n--- Минимальная ДНФ (МДНФ) ---")
    vars = ['A', 'B', 'C', 'D']
    final_terms = []

    for pi in essential:
        term = ""
        for i in range(4):
            if pi[i] == '1':
                if term != "": term += "*"
                term += vars[i]
            elif pi[i] == '0':
                if term != "": term += "*"
                term += "!" + vars[i]

        if term == "":
            term = "1"
        final_terms.append(term)

    res = final_terms[0]
    for i in range(1, len(final_terms)):
        res += " + " + final_terms[i]

    print(res)
    print("==============================================")


# ГЛАВНАЯ ПРОГРАММА

def Main():
    print("╔══════════════════════════════════════╗")
    print("║  МИНИМИЗАЦИЯ ФУНКЦИЙ МЕТОДОМ КВАЙНА  ║")
    print("╚══════════════════════════════════════╝")

    v = ReadVector()
    if v is None:
        return

    PrintTable(v)

    print("\n--- СДНФ ---")
    print(GetSDNF(v))

    Quine(v)


Main()
