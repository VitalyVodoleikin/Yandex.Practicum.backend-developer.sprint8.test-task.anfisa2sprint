from django.shortcuts import render
from ice_cream.models import IceCream


def index(request):
    template = 'homepage/index.html'
    # Запрос. Возьмём нужное. А ненужное не возьмём:
    
    # Заключаем вызов методов в скобки
    # (это стандартный способ переноса длинных строк в Python);
    # каждый вызов пишем с новой строки, так проще читать код:
    ice_cream_list = IceCream.objects.values(
            'id', 'title', 'description'
        # Исключи те объекты, у которых is_published=False:
        ).exclude(is_published=False)
    
    # Полученный из БД QuerySet передаём в словарь контекста:
    context = {'ice_cream_list': ice_cream_list, }
    # Словарь контекста передаём в шаблон, рендерим HTML-страницу:
    return render(request, template, context)


# ---
# Для возврата только тех объектов, у которых в поле is_on_main указано True,
# используется метод .filter(is_on_main__exact=True)
# ---
# Для исключения тех объектов, у которых is_published=False,
# используется метод .exclude(is_published=False)
