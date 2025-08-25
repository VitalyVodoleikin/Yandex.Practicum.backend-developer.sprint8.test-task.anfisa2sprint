from django.shortcuts import render
from ice_cream.models import IceCream, Category
from django.db.models import Q


def index(request):
    template = 'homepage/index.html'

    # # Изначальный запрос 1. Возьмём нужное. А ненужное не возьмём:
    # ice_cream_list = IceCream.objects.values(
    #         'id', 'title', 'description'
    #     ).filter(
    #         Q(is_published=True) &
    #         (Q(is_on_main=True) | Q(title__contains='пломбир'))
    #         )[1:4]
    # 
    # # Запрос 2 для отработки сортировок
    # categories = Category.objects.values(
    #     'id', 'output_order', 'title'
    # ).order_by(
    #     # Сортируем записи по значению поля output_order,
    #     # а если значения output_order у каких-то записей равны -
    #     # сортируем эти записи по названию в алфавитном порядке.
    #     'output_order', 'title'
    # )
    # 
    # # Запрос 3 (JOIN c помощью метода .values())
    # ice_cream_list = IceCream.objects.values('id', 'title', 'category__title')
    # # values(..., '<поле fk>__<поле в модели, связанной по fk>')

    # Запрос 4 (JOIN c помощью .select_related())
    ice_cream_list = IceCream.objects.select_related('category')


    # # Полученный из БД QuerySet по изначальному запросу 1 
    # # передаём в словарь контекста:
    # context = {'ice_cream_list': ice_cream_list, }
    # 
    # # Словарь context для отработки запроса 2 для сортировки
    # context = {
    #     'categories': categories
    # }

    # Формирование словаря для запроса 3, 4
    context = {
        'ice_cream_list': ice_cream_list,
    }

    # Словарь контекста передаём в шаблон, рендерим HTML-страницу:
    return render(request, template, context)






# ----------
# Для возврата только тех объектов, у которых в поле is_on_main указано True,
# используется метод .filter(is_on_main__exact=True)
# ---
# Для исключения тех объектов, у которых is_published=False,
# используется метод .exclude(is_published=False)
# ---
# Для объединения условий при выборке данных можно записать так:
# IceCream.objects.values('id', 'title', 'description').filter(is_published=True, is_on_main=True)
# или так:
# IceCream.objects.filter(is_published=True).filter(is_on_main=True)


# ----------
# Пример использования Q-запросов
# # --->
# 
# # homepage/views.py
# # Для применения Q-объектов их нужно импортировать:
# from django.db.models import Q
# from django.shortcuts import render
# from ice_cream.models import IceCream
# 
# def index(request):
#     template_name = 'homepage/index.html'
#     ice_cream_list = IceCream.objects.values(
#         'id', 'title', 'description'
#     ).filter(
#         # Делаем запрос, объединяя два условия
#         # через Q-объекты и оператор AND:
#         Q(is_published=True) & Q(is_on_main=True)
#     )
#     context = {
#         'ice_cream_list': ice_cream_list,
#     }
#     return render(request, template_name, context)
# # <---


# ----------
# Пример использования логического оператора AND в запросах
# # --->
# 
# SQL: получаем записи, у которых значения полей is_on_main и is_published равны TRUE:
# SELECT "ice_cream_icecream"."id"
# FROM "ice_cream_icecream"
# WHERE ("ice_cream_icecream"."is_on_main" AND "ice_cream_icecream"."is_published");
#  
# Для такого запроса в ORM есть несколько вариантов:
# 
# # Вариант 1, через запятую в аргументах метода .filter():
# IceCream.objects
# .values('id')
# .filter(is_published=True, is_on_main=True)
# 
# # Вариант 2, через Q-объекты:
# IceCream.objects
# .values('id')
# .filter(Q(is_published=True) & Q(is_on_main=True))
# 
# # Вариант 3, дважды вызываем метод .filter();
# # так обычно не пишут, но этот вариант тоже встречается:
# IceCream.objects
# .values('id')
# .filter(is_published=True).filter(is_on_main=True)
# # <---


# ----------
# Пример использования логического оператора OR в запорсах
# # --->
# 
# SQL: получаем записи, у которых поле is_on_main ИЛИ поле is_published равно True:
# SELECT "ice_cream_icecream"."id"       
# FROM "ice_cream_icecream"
# WHERE ("ice_cream_icecream"."is_on_main" OR "ice_cream_icecream"."is_published");
# 
# Django ORM:
# 
# # Можно так, через Q-объекты:
# IceCream.objects
# .values('id')
# .filter(Q(is_published=True) | Q(is_on_main=True))
# 
# # А можно и так - более многословно, но зато без Q-объектов:
# IceCream.objects.values('id').filter(is_published=True) 
# | IceCream.objects.values('id').filter(is_on_main=True)
# # <---


# ----------
# Пример использования логического оператора NOT в запросах
# # --->
# 
# SQL: получаем записи, у которых поле is_published равно True
# и одновременно поле is_on_main не равно False (НЕ НЕ равно True):
#  SELECT "ice_cream_icecream"."id",
#  FROM "ice_cream_icecream"
#  WHERE ("ice_cream_icecream"."is_published" 
#         AND NOT (NOT "ice_cream_icecream"."is_on_main")
# 
# Django ORM:
# 
# # Лучше так:
# IceCream.objects
# .values('id')
# .filter(Q(is_published=True) & ~Q(is_on_main=False))
# 
# # Но сработает и так:
# IceCream.objects
# .values('id')
# .filter(is_published=True)
# .exclude(is_on_main=False)
# # <---
