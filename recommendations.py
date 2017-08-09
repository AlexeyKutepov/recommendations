# Мои предпочтения
me = {
    'Алексей':{
        'Ла-Ла Ленд':100,
        'Зверополис':90,
        'Легенда №17':70,
        'Стартрек: Возмездие':90,
        'Стартрек: Бесконечность':90,
        'Интерстеллар':100,
        'Джон Уик':90,
        'Джон Уик 2': 90,
        'Логан: Росомаха': 40,
        'Три икса: Мировое господство': 10,
        'Отряд самоубийц': 65,
        'Тайная жизнь домашних животных': 80,
        'Зверопой': 60,
        'Стражи Галактики. Часть 2': 90,
        'Человек-паук: Возвращение домой': 80,
        'Стив Джобс': 10,
        'Хоббит: Нежданное путешествие': 90,
        'Сталинград': 40,
        'Джанго Освобожденный': 100,
        'Оз: Великий и ужасный': 60,
        'Крёстный отец': 100,
        'Игра на понижение': 90,
        'Лего Фильм: Бэтмен':10,
        'Форсаж 8':10,
        'Форсаж 7':10,
        'Хранители снов':30,
        'Иллюзия обмана': 80,
        'Иллюзия обмана 2':80,
        'Его собачье дело':75,
        'Кредо убийцы':30,
        'Защитники':10,
        'Элизиум: Рай не на Земле':70,
    },
}

# Словарь кинокритиков и выставленных ими оценок для небольшого набора данных о фильмах
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },'Toby': {
        'Snakes on a Plane':4.5,
        'You, Me and Dupree':1.0,
        'Superman Returns':4.0
    }
}


from math import sqrt


def sim_distance(prefs, person1, person2):
    """
    Возвращает оценку подобия person1 и person2 на основе расстояния
    :param prefs: набор данных
    :param person1: человек 1
    :param person2: человек 2
    :return: коэффициент подобия
    """

    # Получить список предметов, оцененных обоими
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])

    return 1/(1 + sqrt(sum_of_squares))


def sim_pearson(prefs, person1, person2):
    """
    Коэффициент кореляции Пирсона
    :param prefs: набор данных
    :param person1: человек 1
    :param person2: человек 2
    :return: коэффициент кореляции Пирсона
    """
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    # Вычислить сумму всех предпочтений
    sum1 = sum([prefs[person1][item] for item in si])
    sum2 = sum([prefs[person2][item] for item in si])

    # Вычислить сумму квадратов
    sum1_sq = sum([pow(prefs[person1][item], 2) for item in si])
    sum2_sq = sum([pow(prefs[person2][item], 2) for item in si])

    # Вычислить сумму произведений
    p_sum = sum([prefs[person1][item]*prefs[person2][item] for item in si])

    # Вычислить коэффициент Пирсона
    num = p_sum - (sum1 * sum2 / len(si))
    den = sqrt((sum1_sq - pow(sum1, 2) / len(si)) * (sum2_sq - pow(sum2, 2) / len(si)))

    if den == 0: return 0

    return num/den


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    """
    Возвращает список наилучших соответствий для человека из словаря prefs.
    :param prefs: набор данных
    :param person: человек
    :param n: количество наиболее похожих людей
    :param similarity: функция для вычисления коэффициента подобия
    :return: писок наилучших соответствий для человека
    """

    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    # Отсортировать список по убыванию оценок
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommendations(prefs, person, similarity=sim_pearson):
    """
    Получить рекомендации для заданного человека, пользуясь взвешенным средним оценок, данных всеми остальными пользователями
    :param prefs: набор данных
    :param person: человек
    :param similarity: функция для вычисления коэффициента подобия
    :return: рекомендации
    """
    totals = {}
    sim_sums = {}
    for other in prefs:
        # сравнивать человека с самим собой же не нужно
        if other == person: continue
        sim = similarity(prefs,person,other)
        # игнорировать нулевые и отрицательные оценки
        if sim <= 0: continue
        for item in prefs[other]:
            # оценивать только фильмы, которые я еще не смотрел
            if item not in prefs[person] or prefs[person][item] == 0:
                # Коэффициент подобия * Оценка
                totals.setdefault(item,0)
                totals[item] += prefs[other][item] * sim
                # Сумма коэффициентов подобия
                sim_sums.setdefault(item,0)
                sim_sums[item] += sim

    # Создать нормализованный список
    rankings = [(total/sim_sums[item], item) for item, total in totals.items()]

    # Вернуть отсортированный список
    rankings.sort()
    rankings.reverse()
    return rankings


if __name__ == "__main__":
    # print(sim_distance(critics, 'Lisa Rose', 'Toby'))
    # print(sim_pearson(critics, 'Lisa Rose', 'Toby'))
    # print(top_matches(critics, 'Lisa Rose'))
    # print(get_recommendations(critics, 'Toby'))

    from rus_critics import rus_critics

    rus_critics.update(me)

    print(top_matches(rus_critics, 'Алексей'))
    print(get_recommendations(rus_critics, 'Алексей', similarity=sim_pearson))