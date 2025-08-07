

def get_form_text(username: str | None, kwargs: dict):
    name = kwargs.get('name')
    age = kwargs.get('age')
    city = kwargs.get('city')
    origin = kwargs.get('origin')
    height = kwargs.get('height')
    weight = kwargs.get('weight')
    children = kwargs.get("children")
    about = kwargs.get('about')
    phone = kwargs.get('phone')
    channels = kwargs.get('channel')

    text = (f'Юзернейм: {username if username else "Отсутствует"}\nЗовут: {name}\nВозраст: {age}\nГород: {city}\nНациональность: {origin}\nРост: {height}\n'
            f'Вес: {weight}\nНаличие детей: {children if children else "Отсутствуют"}'
            f'\nО себе: {about}\n')
    male = kwargs.get('male')
    if male:
        text = '<b>Мужская анкета</b>\n\n' + text
        work = kwargs.get("work")
        married = kwargs.get('married')
        prayer = kwargs.get('prayer')
        women_wishes = kwargs.get('women_wishes')
        print(kwargs.get('rate'))
        rate = 'VIP анкета' if kwargs.get('rate') == 'vip' else 'Обычная анкета'
        text += (f'Работает: {work}\nСовершает намаз: {prayer}\nСостоял/состоит в браке: {married}'
                 f'\nПожелания по сестре: {women_wishes}\nКонтактные данные: {phone}\n'
                 f'Тариф анкеты: {rate}\nКаналы для выставления: {channels}')
    else:
        text = '<b>Женская анкета</b>\n\n' + text
        languages = kwargs.get('languages')
        relation = kwargs.get('relation')
        religion = kwargs.get('religion')
        married = kwargs.get('married')
        prayer = kwargs.get('prayer')
        second_wife = kwargs.get('second_wife')
        removal = kwargs.get('removal')
        text += (f'Языки: {languages}\nОтношения с мужчиной: {relation}\n'
                 f'Религия: {religion}\nСовершает намаз: {prayer}\nСостояла в браке: {married}\nПойдет второй женой если '
                 f'брат обеспеченный: {second_wife}\nГотова на переезд: {removal}\nКонтактные данные: {phone}'
                 f'\nКаналы для выставления: {channels}')
    return text

