file_path = r"C:\Users\DmitroP\Downloads\netflix_list.csv\netflix_list.csv"  # Замініть на ваш шлях до файлу

# -------------------- Модуль 1: Зчитування даних --------------------

# Ініціалізація списку для збереження даних
data = []

# Відкриваємо файл у режимі читання
with open(file_path, 'r', encoding='utf-8') as file:
    # Проходимо по кожному рядку файлу
    for line in file:
        row = line.strip().split(',')
        data.append(row)


print("Перші 5 рядків даних:", data[:5])



# a) Створіть новий список, що містить тільки шоу або фільми, де рейтинг більше 7.5
filtered_data = [row for row in data if len(row) > 13 and row[13].replace('.', '', 1).isdigit() and float(row[13]) > 7.5]

# b) Зберігайте тільки перші 5 колонок кожного рядка
limited_data = [row[:5] for row in filtered_data]

print("Відфільтровані дані (перші 5 рядків):", limited_data[:5])



def filter_shows(data):
    for row in data:
        # Перевіряємо, чи рядок має достатню кількість колонок
        if len(row) > 11:
            language = row[10]  # Поле 'language' знаходиться у 11-й колонці (індекс 10)
            type_ = row[8]      # Поле 'type' знаходиться у 9-й колонці (індекс 8)
            end_year = row[5]   # Поле 'endYear' знаходиться у 6-й колонці (індекс 5)

            #  мова - англійська, тип - серіал або фільм, кінець року > 2015
            if language == "English" and type_ in [ "movie" , "tvSeries" ] and end_year.isdigit() and int(end_year) > 2015:
                yield row

# Використання генераторної функції
filtered_shows = filter_shows(data)

print("Результати генераторної функції (перші 5 рядків):")
for show in list(filtered_shows)[:5]:
    print(show)
    print()
