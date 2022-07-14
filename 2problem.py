import requests
from bs4 import BeautifulSoup as BS4


def parser_step_1() -> list:
    '''функция первичного парсинга и получения списка животных с первой страницы'''
    req = requests.get('https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:'
                       '%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_'
                       '%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83')
    html = req.text
    parser = BS4(html, "html.parser")
    elements = parser.select("ul")
    list_animals = elements[2].text.split('\n')
    while True:
        list_animals += parser_step_2(list_animals)
        if 'Ящурки' == list_animals[-1]:
            break
    return list_animals


def parser_step_2(list_animals) -> list:
    '''Функция вторичного парсинга и получения оставшихся страничек с животными'''
    element = list_animals[-1].split()
    result = '+'.join(element)
    req = requests.get(f"https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom={result}")

    html = req.text
    parser = BS4(html, "html.parser")
    elements = parser.select("ul")
    tmp_list_animals = elements[2].text.split('\n')
    if 'ЖивотныеОрганизмы по алфавиту' != elements[3].text:
        return tmp_list_animals + elements[3].text.split('\n')
    return tmp_list_animals


def counting_animals(list_animals) -> dict:
    '''Функция подсчета количества '''
    result = {}
    rus_alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О',
                    'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
    count = 0
    for letter in rus_alphabet:
        for res in list_animals:
            if res.startswith(letter):
                count += 1
        result[letter] = count
        count = 0
    return result


list_animals = parser_step_1()
result = counting_animals(list_animals)
print(result)



