file_path = r"C:\Users\DmitroP\Downloads\netflix_list.csv\netflix_list.csv"

# -------------------- Модуль 1: Зчитування даних --------------------

# Функція для розділення рядків, враховуючи лапки
def parse_line(line):
    """
    Розбиває рядок на колонки з урахуванням ком у лапках.
    """
    result = []
    current = ''
    inside_quotes = False

    for char in line:
        if char == '"' and not inside_quotes:
            inside_quotes = True
        elif char == '"' and inside_quotes:
            inside_quotes = False
        elif char == ',' and not inside_quotes:
            result.append(current.strip())
            current = ''
        else:
            current += char

    result.append(current.strip())
    return result

# Зчитування даних із файлу
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [parse_line(line.strip()) for line in file]

    print("Перші 5 рядків даних:")
    for row in data[:5]:
        print(", ".join(row))
    print("\n")
except FileNotFoundError:
    print(f"Файл {file_path} не знайдено.")
    data = []

# -------------------- Фільтрування та обробка даних --------------------

# a) Список, що містить тільки шоу або фільми, де рейтинг більше 7.5
filtered_data = [
    row for row in data
    if len(row) > 13 and row[13].replace('.', '', 1).isdigit() and float(row[13]) > 7.5
]

# b) Збереження тільки перших 5 колонок кожного рядка
limited_data = [row[:5] for row in filtered_data]

print("Відфільтровані дані (перші 5 рядків):")
for row in limited_data[:5]:
    print(", ".join(row))
print("\n")

# -------------------- Генераторна функція --------------------

def filter_shows(data):
    """
    Генераторна функція для фільтрування шоу або фільмів за умовами:
    - Мова шоу або фільму — англійська (поле language);
    - Це або серіал, або фільм (поле type), що закінчився після 2015 року (поле endYear).
    """
    for row in data:
        if len(row) > 11:  # Перевірка довжини рядка
            language = row[10]  # Поле 'language'
            type_ = row[8]      # Поле 'type'
            end_year = row[5]   # Поле 'endYear'

            if language == "English" and type_ in ["movie", "tvSeries"] and end_year.isdigit() and int(end_year) > 2015:
                yield row

# Використання генераторної функції
filtered_shows = filter_shows(data)

print("Результати генераторної функції (перші 5 рядків):")
for idx, show in enumerate(filtered_shows):
    print(f"Рядок {idx + 1}: {', '.join(show)}")
    if idx == 4:  # Виводимо тільки перші 5 рядків
        break
print("\n")

# -------------------- Ітератор для основного акторського складу --------------------

class CastIterator:
    """
    Ітератор для проходження через датасет і повернення основного акторського складу (поле cast),
    якщо його довжина перевищує 50 символів.
    """
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.data):
            row = self.data[self.index]
            self.index += 1

            if len(row) > 17:
                cast_field = row[17]
                if cast_field.startswith("[") and cast_field.endswith("]"):
                    cast = cast_field[1:-1]
                    cast_list = [actor.strip(" '") for actor in cast.split(',')]
                    if len(cast) > 50:  # Довжина оригінального рядка
                        return cast_list
        raise StopIteration

# Використання ітератора
cast_iterator = CastIterator(data)

print("Основний акторський склад (перші 10 записів):")
for idx, cast in enumerate(cast_iterator):
    print(f"Запис {idx + 1}: {cast}")
    if idx == 9:  # Виводимо тільки перші 10 записів
        break
print("\n")

# -------------------- Функція для аналізу дорослого контенту --------------------

def analyze_data_with_generators(data):
    """
    Аналізує:
    a) Кількість дорослого контенту (isAdult == 1);
    b) Середній рейтинг для записів із більше ніж 1000 голосами.
    """
    # Підрахунок дорослого контенту
    adult_count = sum(
        1 for row in data
        if len(row) > 7 and row[7].isdigit() and int(row[7]) == 1
    )

    # Генератори для обчислення рейтингу та кількості голосів
    ratings = (
        float(row[13]) for row in data
        if len(row) > 13 and row[13].replace('.', '', 1).isdigit()
        and len(row) > 14 and row[14].replace('.', '', 1).isdigit() and float(row[14]) > 1000
    )

    vote_counts = (
        1 for row in data
        if len(row) > 14 and row[14].replace('.', '', 1).isdigit() and float(row[14]) > 1000
    )

    # Обчислення сум
    total_ratings = sum(ratings)
    total_votes = sum(vote_counts)

    # Обчислюємо середній рейтинг
    average_rating = total_ratings / total_votes if total_votes > 0 else 0

    return adult_count, average_rating

# Виклик функції
adult_content_count, avg_rating = analyze_data_with_generators(data)

# Вивід результатів
print(f"Кількість дорослого контенту: {adult_content_count}")
print(f"Середній рейтинг: {avg_rating:.2f}\n")



# -------------------- Пошук шоу з більше ніж 10 епізодами --------------------

def find_top_shows(data, avg_rating):
    """
    Повертає список заголовків шоу:
    a) Більше ніж 10 епізодів;
    b) Рейтинг вище середнього.
    """
    return [
        row[1]
        for row in data
        if len(row) > 13 and row[6].isdigit() and int(row[6]) > 10 and
        row[13].replace('.', '', 1).isdigit() and float(row[13]) > avg_rating
    ]

top_shows = find_top_shows(data, avg_rating)

print("Шоу з більше ніж 10 епізодами та рейтингом вище середнього:")
for show in top_shows[:10]:  # Виводимо тільки перші 10 записів
    print(f"- {show}")
