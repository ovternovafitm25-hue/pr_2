
print("Завдання 1")
class CyclicRange:

    def __init__(self, start: int, stop: int, step: int = 1,
                 repeats: int = 1):
        if step <= 0:
            raise ValueError("Крок повинен бути додатним")
        if repeats < 0:
            raise ValueError("Кількість циклів не може бути від'ємною")

        self._start = start
        self._stop = stop
        self._step = step
        self._repeats = repeats
        self._current = start
        self._cycle = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self._cycle >= self._repeats:
            raise StopIteration

        if self._current >= self._stop:
            self._current = self._start
            self._cycle += 1

            if self._cycle >= self._repeats:
                raise StopIteration

        result = self._current
        self._current += self._step
        return result


def main():
    print("CyclicRange(1, 4, repeats=3):")
    for num in CyclicRange(1, 4, repeats=3):
        print(num, end=" ")
    print()

    print("CyclicRange(0, 10, step=3, repeats=2):")
    for num in CyclicRange(0, 10, step=3, repeats=2):
        print(num, end=" ")
    print()

    result = list(CyclicRange(5, 8, repeats=2))
    print(f"Як список: {result}")

    total = sum(CyclicRange(1, 5, repeats=2))
    print(f"Сума CyclicRange(1, 5, repeats=2): {total}")


if __name__ == "__main__":
    main()

print("\n")

from collections import namedtuple

Student = namedtuple("Student", ["name", "grade"])


class StudentGroupIterator:

    def __init__(self, students: list[Student]):
        self._students = students
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Student:
        if self._index >= len(self._students):
            raise StopIteration

        student = self._students[self._index]
        self._index += 1
        return student


class StudentGroup:

    def __init__(self, group_name: str):
        self._group_name = group_name
        self._students: list[Student] = []

    def add_student(self, name: str, grade: int) -> None:
        self._students.append(Student(name, grade))

    def __iter__(self):
        return StudentGroupIterator(self._students)

    def __len__(self) -> int:
        return len(self._students)

    def top_students(self, n: int = 3):
        sorted_students = sorted(
            self._students,
            key=lambda student: student.grade,
            reverse=True
        )
        return iter(sorted_students[:n])


def main():
    group = StudentGroup("КІ-21")
    group.add_student("Олена", 95)
    group.add_student("Іван", 78)
    group.add_student("Марія", 92)
    group.add_student("Петро", 85)
    group.add_student("Анна", 88)

    print("Перший обхід:")
    for student in group:
        print(f"  {student.name}: {student.grade}")

    print("Другий обхід:")
    for student in group:
        print(f"  {student.name}: {student.grade}")

    print("Всі пари студентів:")
    for s1 in group:
        for s2 in group:
            if s1.name < s2.name:
                print(f"  {s1.name} та {s2.name}")

    print("Топ-3 студенти:")
    for student in group.top_students(3):
        print(f"  {student.name}: {student.grade}")


if __name__ == "__main__":
    main()

print("\nЗавдання 2")

import itertools
from typing import Optional


def arithmetic_progression(start: float, step: float):
    current = start
    while True:
        yield current
        current += step


def geometric_progression(start: float, ratio: float,
                          limit: float = float("inf")):
    current = start
    while current <= limit:
        yield current
        current *= ratio


def fibonacci(n: Optional[int] = None):
    a, b = 0, 1
    count = 0

    while n is None or count < n:
        yield a
        a, b = b, a + b
        count += 1


def collatz_sequence(n: int):
    if n <= 0:
        raise ValueError("Початкове число повинно бути додатним")

    while True:
        yield n
        if n == 1:
            break
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1


def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def main():
    ap = arithmetic_progression(2, 3)
    first_10 = list(itertools.islice(ap, 10))
    print(f"Арифметична прогресія (2, 3): {first_10}")

    gp = list(geometric_progression(1, 2, limit=1000))
    print(f"Геометрична прогресія (1, 2): {gp}")

    fib_15 = list(fibonacci(15))
    print(f"Фібоначчі (15): {fib_15}")

    coll = list(collatz_sequence(27))
    print(f"Коллатц (27): довжина={len(coll)}, макс={max(coll)}")

    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    flat = list(flatten(nested))
    print(f"Розгортання: {flat}")

    for fib_num in fibonacci(None):
        if fib_num > 10000:
            print(f"Перше число Фібоначчі > 10000: {fib_num}")
            break


if __name__ == "__main__":
    main()

print("\n")

from collections import defaultdict


SAMPLE_DATA = [
    "Олена,Математика,95",
    "Іван,Математика,78",
    "",
    "Марія,Фізика,92",
    "Петро,Математика,INVALID",
    "Анна,Фізика,88",
    "Олена,Фізика,90",
    "Іван,Програмування,85",
    "Марія,Програмування,91",
    "Петро,Фізика,76",
    "Анна,Математика,93",
    "Олена,Програмування,97",
    "",
    "Марія,Математика,89",
    "Іван,Фізика,72",
    "Петро,Програмування,80",
    "Анна,Програмування,86",
]


def data_source(records: list[str]):
    for record in records:
        yield record


def filter_empty(records):
    for record in records:
        if record.strip():
            yield record


def parse_records(records):
    for record in records:
        parts = record.split(",")

        if len(parts) != 3:
            continue

        try:
            grade = int(parts[2])
        except ValueError:
            continue

        yield {
            "student": parts[0],
            "subject": parts[1],
            "grade": grade
        }


def filter_passed(records, min_grade: int = 60):
    for record in records:
        if record["grade"] >= min_grade:
            yield record


def format_output(records):
    for record in records:
        yield (
            f"[{record['subject']}] "
            f"{record['student']}: {record['grade']} балів"
        )


def main():
    pipeline = format_output(
        filter_passed(
            parse_records(
                filter_empty(data_source(SAMPLE_DATA))
            ),
            min_grade=75,
        )
    )

    print("=== Результати (>= 75 балів) ===")
    for line in pipeline:
        print(line)

    print("=== Середній бал по предметах ===")

    subject_grades = defaultdict(list)

    for record in parse_records(
        filter_empty(data_source(SAMPLE_DATA))
    ):
        subject_grades[record["subject"]].append(record["grade"])

    for subject, grades in sorted(subject_grades.items()):
        avg = sum(grades) / len(grades)
        print(f"  {subject}: {avg:.1f} (з {len(grades)} оцінок)")


if __name__ == "__main__":
    main()

print("\nЗавдання 3")


"""Порівняння list comprehension та generator expression."""

import sys
import timeit


def memory_comparison():
    """Порівняння використання пам'яті."""

    sizes = [1_000, 10_000, 100_000, 1_000_000]

    print("=" * 60)
    print(f"{'N':>12} | {'list (байт)':>14} | {'gen (байт)':>12} | {'Ratio':>8}")
    print("-" * 60)

    for n in sizes:
        data_list = [x ** 2 for x in range(n)]
        data_gen = (x ** 2 for x in range(n))

        list_size = sys.getsizeof(data_list)
        gen_size = sys.getsizeof(data_gen)

        print(
            f"{n:>12,} | {list_size:>14,} | "
            f"{gen_size:>12,} | {list_size / gen_size:>7.0f}×"
        )

    print("=" * 60)


def performance_comparison():
    """Порівняння часу виконання."""

    n = 500_000

    time_list = timeit.timeit(
        lambda: sum([x ** 2 for x in range(n)]),
        number=5,
    )

    time_gen = timeit.timeit(
        lambda: sum(x ** 2 for x in range(n)),
        number=5,
    )

    print(f"sum() для {n:,} елементів (середнє з 5 запусків):")
    print(f"  list comprehension: {time_list:.4f} с")
    print(f"  generator expression: {time_gen:.4f} с")

    faster = "list" if time_list < time_gen else "generator"
    print(f"  Швидше: {faster}")


def practical_usage():
    """Практичне використання generator expression."""

    words = [
        "Python", "ітератор", "генератор", "yield", "comprehension",
        "дані", "пам'ять", "ефективність", "конвеєр", "ліниві",
        "обчислення", "протокол", "об'єкт", "клас", "функція",
    ]

    longest = max(words, key=lambda w: len(w))
    print(f"Найдовше слово: '{longest}' ({len(longest)} символів)")

    all_nonempty = all(word != "" for word in words)
    print(f"Всі слова непорожні: {all_nonempty}")

    has_long = any(len(word) > 15 for word in words)
    print(f"Є слово > 15 символів: {has_long}")

    csv_line = ",".join(word for word in words)
    print(f"CSV: {csv_line}")

    total_length = sum(len(word) for word in words)
    print(f"Сума довжин: {total_length}")

    word_lengths = {word: len(word) for word in words}
    print(f"Довжини: {word_lengths}")

    numbers = range(1, 101)

    even_squares_sum = sum(
        x ** 2 for x in numbers if x % 2 == 0
    )
    print(f"Сума квадратів парних від 1 до 100: {even_squares_sum}")


def main():
    print(">>> Порівняння використання пам'яті <<<")
    memory_comparison()

    print(">>> Порівняння продуктивності <<<")
    performance_comparison()

    print(">>> Практичне використання generator expression <<<")
    practical_usage()


if __name__ == "__main__":
    main()
