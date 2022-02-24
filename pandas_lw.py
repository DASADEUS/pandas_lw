# -*- coding: utf-8 -*-
"""
## Лабораторная работа

1.1 В файлах `recipes_sample.csv` и `reviews_sample.csv` находится информация об рецептах блюд и отзывах на эти рецепты соответственно. Загрузите данные из файлов в виде `pd.DataFrame` с названиями `recipes` и `reviews`. Обратите внимание на корректное считывание столбца с индексами в таблице `reviews` (безымянный столбец).
"""

import numpy as np
from google.colab import files
import pandas as pd
from pandas import concat

uploaded = files.upload()

recipes = pd.read_csv('recipes_sample.csv')
reviews= pd.read_csv('reviews_sample.csv')
recipes.head(20)

"""1.2 Для каждой из таблиц выведите основные параметры:
* количество точек данных (строк);
* количество столбцов;
* тип данных каждого столбца.
"""

recipes.info()

reviews.info()

"""1.3 Исследуйте, в каких столбцах таблиц содержатся пропуски. Посчитайте долю строк, содержащих пропуски, в отношении к общему количеству строк."""

recipes.isna().sum()/recipes.size*100

reviews.isna().sum()/reviews.size*100

"""1.4 Рассчитайте среднее значение для каждого из числовых столбцов (где это имеет смысл)."""

print(recipes["minutes"].mean())
print(recipes["n_ingredients"].mean())

print(reviews["rating"].mean())

"""1.5 Создайте серию из 10 случайных названий рецептов."""

recipes["name"].sample(10)

"""1.6 Измените индекс в таблице `reviews`, пронумеровав строки, начиная с нуля."""

reviews.reset_index(drop=True)

"""1.7 Выведите информацию о рецептах, время выполнения которых не больше 20 минут и кол-во ингредиентов в которых не больше 5."""

recipes[(recipes["minutes"]<=20)&(recipes["n_ingredients"]<=5)]

"""### Работа с датами в `pandas`

2.1 Преобразуйте столбец `submitted` из таблицы `recipes` в формат времени. Модифицируйте решение задачи 1.1 так, чтобы считать столбец сразу в нужном формате.
"""

recipes['submitted']=pd.to_datetime(recipes['submitted'],format='%Y-%m-%d')
recipes

"""2.2 Выведите информацию о рецептах, добавленных в датасет не позже 2010 года."""

recipes[recipes["submitted"]<'2010-01-1']

"""### Работа со строковыми данными в `pandas`

3.1  Добавьте в таблицу `recipes` столбец `description_length`, в котором хранится длина описания рецепта из столбца `description`.
"""

recipes["description_length"]=recipes["description"].str.len()
recipes

"""3.2 Измените название каждого рецепта в таблице `recipes` таким образом, чтобы каждое слово в названии начиналось с прописной буквы."""

recipes["name"]=recipes["name"].str.title()
recipes

"""3.3 Добавьте в таблицу `recipes` столбец `name_word_count`, в котором хранится количество слов из названии рецепта (считайте, что слова в названии разделяются только пробелами). Обратите внимание, что между словами может располагаться несколько пробелов подряд."""

recipes["name_word_count"] = recipes["name"].str.split().str.len()
recipes

"""### Группировки таблиц `pd.DataFrame`

4.1 Посчитайте количество рецептов, представленных каждым из участников (`contributor_id`). Какой участник добавил максимальное кол-во рецептов?
"""

recipes.groupby("contributor_id").describe()['id']['count']

"""4.2 Посчитайте средний рейтинг к каждому из рецептов. Для скольких рецептов отсутствуют отзывы? Обратите внимание, что отзыв с нулевым рейтингом или не заполненным текстовым описанием не считается отсутствующим."""

reviews.groupby("recipe_id").describe()['rating']['mean']

reviews['review'].isnull().sum()

"""4.3 Посчитайте количество рецептов с разбивкой по годам создания."""

recipes['id'].groupby(recipes['submitted'].map(lambda x: x.year)).count()

"""### Объединение таблиц `pd.DataFrame`

5.1 При помощи объединения таблиц, создайте `DataFrame`, состоящий из четырех столбцов: `id`, `name`, `user_id`, `rating`. Рецепты, на которые не оставлен ни один отзыв, должны отсутствовать в полученной таблице. Подтвердите правильность работы вашего кода, выбрав рецепт, не имеющий отзывов, и попытавшись найти строку, соответствующую этому рецепту, в полученном `DataFrame`.
"""

dt= recipes.merge(reviews[["user_id","rating"]], left_on='contributor_id', right_on='user_id', how="right").dropna()
dr=dt[["id", "name", "user_id", "rating"]]

dt[dt['id']==223349]

"""5.3. Выясните, рецепты, добавленные в каком году, имеют наименьший средний рейтинг?"""

dt.groupby(pd.to_datetime(dt['submitted'], format='%Y-%m-%d').dt.year)[['rating']].mean().idxmax()

dt

"""### Сохранение таблиц `pd.DataFrame`

6.1 Отсортируйте таблицу в порядке убывания величины столбца `name_word_count` и сохраните результаты выполнения заданий 3.1-3.3 в csv файл.
"""

recipes["description_length"] =recipes["description"].str.len()
recipes["description"].str.title()
recipes["name_word_count"] = recipes["name"].str.split().str.len()
recipes.sort_values("name_word_count")
recipes.to_csv('ex3.csv')

"""6.2 Воспользовавшись `pd.ExcelWriter`, cохраните результаты 5.1 и 5.2 в файл: на лист с названием `Рецепты с оценками` сохраните результаты выполнения 5.1; на лист с названием `Количество отзывов по рецептам` сохраните результаты выполнения 5.2."""

pdd = pd.ExcelWriter('ex5.xlsx')
dr.to_excel(pdd,'Рецепты с оценками')
pdd.save()
