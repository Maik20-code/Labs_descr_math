from random import *

# ДАННЫЕ

A = set()
B = set()
C = set()
U = set(range(-30, 31))          # универсальное множество
SETS = {"a": A, "b": B, "c": C}  # доступ к множествам по имени (типо словаря)


# ОПЕРАЦИИ НАД МНОЖЕСТВАМИ

def Peresech(s1, s2):
    res = set()
    for x in s1:
        if x in s2:
            res.add(x)
    return res


def Objedinenie(s1, s2):
    res = set()
    for x in s1:
        res.add(x)
    for x in s2:
        if x not in res:
            res.add(x)
    return res


def Raznost(s1, s2):
    res = set()
    for x in s1:
        if x not in s2:
            res.add(x)
    return res


def SimmRaznost(s1, s2):
    res = set()
    for x in s1:
        if x not in s2:
            res.add(x)
    for x in s2:
        if x not in s1:
            res.add(x)
    return res


def Dopolnenie(s):
    return Raznost(U, s)


# ФОРМАТИРОВАНИЕ

def Format(s):
    if len(s) == 0:
        return "∅"
    return "{" + ", ".join(str(x) for x in sorted(s)) + "}"


# ТОКЕНИЗАЦИЯ

SYMBOLS = {
    "∪": "+",
    "|": "+",
    "∩": "&",
    "*": "&",
    "△": "^",
    "¬": "~",
    "!": "~",
    "/": "\\",
}


def Tokenize(expr):
    tokens = []
    for ch in expr:
        if ch.isspace():
            continue
        if ch in "ABCabc":
            tokens.append(ch.upper())
        elif ch in "+\\&^~()":
            tokens.append(ch)
        elif ch in SYMBOLS:
            tokens.append(SYMBOLS[ch])
        else:
            raise SyntaxError(f"Недопустимый символ: '{ch}'")
    return tokens


# ПАРСЕР (рекурсивный спуск)
#  Грамматика по приоритетам (от низкого к высокому):
#    expr -> term (("+" | "\" | "^") term)*
#    term -> factor ("&" factor)*
#    factor -> "~" factor | atom
#    atom -> "A" | "B" | "C" | "(" expr ")"

def Peek(state):
    pos = state["pos"]
    tok = state["tokens"]
    return tok[pos] if pos < len(tok) else None

def Consume(state):
    t = state["tokens"][state["pos"]]
    state["pos"] += 1
    return t

def Record(state, op, left, right, res):
    if not state["trace"]:
        return
    state["step"] += 1
    l = Format(left) if isinstance(left, set) else left
    r = Format(right) if isinstance(right, set) else right
    state["log"].append(
        f"  шаг {state['step']}: {l} {op} {r} -> {Format(res)}"
    )

def ParseAtom(state):
    tok = Peek(state)
    if tok is None:
        raise SyntaxError("Неожиданный конец выражения")
    if tok in ("A", "B", "C"):
        Consume(state)
        return SETS[tok.lower()]
    if tok == "(":
        Consume(state)
        inner = ParseExpr(state)
        if Peek(state) != ")":
            raise SyntaxError("Не закрыта скобка")
        Consume(state)
        return inner
    raise SyntaxError(f"Неожиданный токен: '{tok}'")

def ParseFactor(state):
    if Peek(state) == "~":
        Consume(state)
        operand = ParseFactor(state)
        res = Dopolnenie(operand)
        Record(state, "~", operand, "U", res)
        return res
    return ParseAtom(state)

def ParseTerm(state):
    left = ParseFactor(state)
    while Peek(state) == "&":
        Consume(state)
        right = ParseFactor(state)
        res = Peresech(left, right)
        Record(state, "&", left, right, res)
        left = res
    return left

def ParseExpr(state):
    left = ParseTerm(state)
    while Peek(state) in ("+", "\\", "^"):
        op = Consume(state)
        right = ParseTerm(state)
        if op == "+":
            res = Objedinenie(left, right)
            Record(state, "+", left, right, res)
        elif op == "\\":
            res = Raznost(left, right)
            Record(state, "\\", left, right, res)
        else:
            res = SimmRaznost(left, right)
            Record(state, "^", left, right, res)
        left = res
    return left

def Evaluate(expr, trace=False):
    tokens = Tokenize(expr)
    if not tokens:
        raise SyntaxError("Пустое выражение")

    state = {
        "tokens": tokens,
        "pos": 0,
        "trace": trace,
        "step": 0,
        "log": [],
    }

    res = ParseExpr(state)

    if state["pos"] != len(tokens):
        raise SyntaxError(
            f"Лишние символы после выражения: '{tokens[state['pos']]}'"
        )
    return res, state["log"]


# УСЛОВИЯ ДЛЯ ЧИСЕЛ

def Conditions():
    print("Выберите условия (можно несколько подряд):")
    print("  1 - Отрицательные (x < 0)")
    print("  2 - Положительные (x > 0)")
    print("  3 - Кратные n")
    print("  4 - Чётные")
    print("  5 - Нечётные")
    print("  6 - В диапазоне [lo, hi]")
    print("  7 - Любые (по умолчанию)")

    raw = input("Ваш выбор: ").strip()
    if not raw:
        raw = "7"

    checks = []
    descr = []

    for ch in raw:
        if ch == "1":
            checks.append(lambda x: x < 0)
            descr.append("отрицательные")
        elif ch == "2":
            checks.append(lambda x: x > 0)
            descr.append("положительные")
        elif ch == "3":
            try:
                n = int(input("  n = "))
            except ValueError:
                print("  Некорректно, пропускаем.")
                continue
            if n == 0:
                print("  n не может быть 0, пропускаем.")
                continue
            checks.append(lambda x, n=n: x % n == 0)
            descr.append(f"кратные {n}")
        elif ch == "4":
            checks.append(lambda x: x % 2 == 0)
            descr.append("чётные")
        elif ch == "5":
            checks.append(lambda x: x % 2 != 0)
            descr.append("нечётные")
        elif ch == "6":
            try:
                lo = int(input("  нижняя граница: "))
                hi = int(input("  верхняя граница: "))
            except ValueError:
                print("  Некорректно, пропускаем.")
                continue
            if lo > hi:
                lo, hi = hi, lo
            checks.append(lambda x, lo=lo, hi=hi: lo <= x <= hi)
            descr.append(f"в [{lo}, {hi}]")
        elif ch == "7":
            continue
        else:
            print(f"  Пропускаем неизвестный пункт '{ch}'.")

    if not checks:
        checks = [lambda x: True]
        descr = ["любые"]

    print(f"Условия: {', '.join(descr)}.")
    return checks

def Check(x, checks):
    for check in checks:
        if not check(x):
            return False
    return True


# ВЫБОР МНОЖЕСТВА

def ChooseSet():
    m = input("Выберите множество (a/b/c): ").strip().lower()
    if m not in SETS:
        print("Нет такого множества!")
        return None
    return m


# МЕНЮ 1: ДЕЙСТВИЯ НАД МНОЖЕСТВАМИ

def AddRand():
    m = ChooseSet()
    if m is None:
        return
    target = SETS[m]

    checks = Conditions()
    valid = [n for n in U if Check(n, checks)]
    if not valid:
        print("Под условия не подходит ни одно число из U.")
        return

    free = [n for n in valid if n not in target]
    if not free:
        print("Все подходящие числа уже есть в множестве.")
        return

    try:
        count = int(input(f"Сколько добавить? (доступно {len(free)}): "))
    except ValueError:
        print("Некорректно.")
        return

    if count <= 0:
        print("Количество должно быть положительным.")
        return

    count = min(count, len(free))
    for n in sample(free, count):
        target.add(n)
        print(f"  + {n} -> {m.upper()}")

    print(f"Добавлено {count}. {m.upper()} = {Format(target)}")


def AddManual():
    m = ChooseSet()
    if m is None:
        return
    target = SETS[m]

    print("Введите 'stop' для завершения ввода.")

    added = 0

    while True:
        raw = input(f"Число {added + 1} (или 'stop'): ").strip().lower()
        if raw == "stop":
            break
        try:
            n = int(raw)
        except ValueError:
            print("  Некорректный ввод.")
            continue

        if n not in U:
            print(f"  {n} не входит в U (-30..30).")
            continue
        if n in target:
            print(f"  {n} уже есть в {m.upper()}.")
            continue

        target.add(n)
        added += 1
        print(f"  + {n} -> {m.upper()}")
    print(f"Добавлено {added}. {m.upper()} = {Format(target)}")

def Del():
    m = ChooseSet()
    if m is None:
        return
    try:
        n = int(input("Введите число: "))
    except ValueError:
        print("Некорректно.")
        return
    if n in SETS[m]:
        SETS[m].remove(n)
        print(f"Число {n} удалено из {m.upper()}.")
    else:
        print(f"Числа {n} нет в {m.upper()}.")

def Clear():
    m = ChooseSet()
    if m is None:
        return
    SETS[m].clear()
    print(f"Множество {m.upper()} очищено.")

def ClearAll():
    for s in SETS.values():
        s.clear()
    print("Все множества очищены.")

def MenuActions():
    while True:
        print("--- Действия над множествами ---")
        print("  1 - Добавить случайно")
        print("  2 - Добавить вручную")
        print("  3 - Удалить число")
        print("  4 - Очистить множество")
        print("  5 - Очистить все множества")
        print("  0 - Назад")

        m = input("Ваш выбор: ").strip()

        if m == "1": AddRand()
        elif m == "2": AddManual()
        elif m == "3": Del()
        elif m == "4": Clear()
        elif m == "5": ClearAll()
        elif m == "0": return
        else: print("Нет такого пункта.")


# МЕНЮ 2: ВЫЧИСЛЕНИЕ

def MenuCalc():
    print("╔══════════════════════════════════════════════════════╗")
    print("║                    ВЫЧИСЛЕНИЕ                        ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║  Введите любое выражение из множеств A, B, C.        ║")
    print("║                                                      ║")
    print("║  Операторы:                                          ║")
    print("║    +     — объединение            (A + B = A ∪ B)    ║")
    print("║    \\     — разность               (A \\ B)            ║")
    print("║    &     — пересечение            (A & B = A ∩ B)    ║")
    print("║    ^     — симметрическая разность (A ^ B = A △ B)   ║")
    print("║    ~     — дополнение             (~A = U \\ A)       ║")
    print("║                                                      ║")
    print("║  Примеры:                                            ║")
    print("║    A + (B & C)                                       ║")
    print("║    (A \\ B) ^ C                                       ║")
    print("║    ~A + (B & C)                                      ║")
    print("║    (A + B) \\ (B & C)                                 ║")
    print("║                                                      ║")
    print("║  Приоритеты:  ~  >  &  >  (+, \\, ^)                  ║")
    print("║  Введите 'back' или пустую строку — возврат.         ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    while True:
        expr = input("Выражение: ").strip()
        if expr.lower() in ("back", "0", ""):
            return
        try:
            res, log = Evaluate(expr, trace=True)
            if log:
                print("Пошаговое вычисление:")
                for line in log:
                    print(line)
            print(f"Результат: {Format(res)}")
        except SyntaxError as e:
            print(f"Ошибка разбора: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")
        print("-" * 45)


# МЕНЮ 3: ПРОСМОТР

def MenuView():
    while True:
        print("--- Просмотр множеств ---")
        print("  1 - Одно множество")
        print("  2 - Все множества")
        print("  3 - Универсальное множество U")
        print("  0 - Назад")

        m = input("Ваш выбор: ").strip()

        if m == "1":
            name = input("Множество (a/b/c): ").strip().lower()
            if name not in SETS:
                print("Нет такого множества!")
                continue
            print(f"{name.upper()} = {Format(SETS[name])}")
        elif m == "2":
            for name in ("a", "b", "c"):
                print(f"  {name.upper()} = {Format(SETS[name])}")
        elif m == "3":
            print(f"  U = {Format(U)}")
        elif m == "0":
            return
        else:
            print("Нет такого пункта.")


# ГЛАВНОЕ МЕНЮ

def MainMenu():
    while True:
        print()
        print("╔════════════════════════════════╗")
        print("║      КАЛЬКУЛЯТОР МНОЖЕСТВ      ║")
        print("╠════════════════════════════════╣")
        print("║  1 - Действия над множествами  ║")
        print("║  2 - Вычисление                ║")
        print("║  3 - Просмотр множеств         ║")
        print("║  0 - Выход                     ║")
        print("╚════════════════════════════════╝")

        m = input("Ваш выбор: ").strip()

        if m == "1":   MenuActions()
        elif m == "2": MenuCalc()
        elif m == "3": MenuView()
        elif m == "0":
            print("Завершение программы.")
            return
        else:
            print("Нет такого пункта.")


# ЗАПУСК

MainMenu()
