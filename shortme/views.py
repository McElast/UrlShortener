import datetime

from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import View
from django.core.serializers import serialize
from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework import generics

import configs
from . import serializers
from .forms import ShortenUrlForm
from .models import ShortenUrl


class QueryMixin:
    """
    Вспомогательный класс для вывода списка объектов модели ShortenUrl с фильтром по сессии
    Если сесси нет (новый пользователь), то она предварительно создастся
    """
    def collect_data(self, *args, **kwargs):
        if not self.request.session.session_key:
            self.request.session.save()
        session_id = self.request.session.session_key
        qs = ShortenUrl.objects.filter(client_session=session_id).order_by('-added')
        results = serialize('json', qs)
        cache.set(session_id, results, timeout=configs.OBJ_LIFETIME)
        return qs


def db_or_cache_or_404(short_url):
    """
    Проверяем короткую ссылку из адреса на присутствие в сервисе:
    - есть ли она в кеше (в первую очередь)
    - есть ли она в базе данных (во вторую очередь)
    - иначе вызываем исключение на страницу 404
    """
    if short_url in cache:
        return cache.get(short_url)
    elif ShortenUrl.objects.filter(short_url_part=short_url).exists():
        url = ShortenUrl.objects.get(short_url_part=short_url).original_url
        cache.set(short_url, url, timeout=configs.OBJ_LIFETIME)
        return url
    else:
        raise Http404('Такой ссылки у нас нет. Попробуйте еще раз!')


class ShortenUrlList(View, QueryMixin):
    """
    1 - Отображение сокращенных ссылок конкретного "пользователя" (на основании сессии).
    2 - Вывод формы для добавления нового URL
    3 - Сохранение валидных данных в БД
    """
    form_class = ShortenUrlForm
    template_name = 'shortme/main.html'
    extra_context = {'title': 'Сократитель УЛЬ-ТРА'}
    success_url = '/'

    def get(self, request, *args, **kwargs):
        qs = self.collect_data()
        form = ShortenUrlForm()
        paginator = Paginator(qs, 2)
        page_number = request.GET.get('page')
        if len(request.GET) > 1:
            raise Http404('Странная ссылка... Мы пока еще ее не реализовали.')
        elif not page_number and len(request.GET):
            raise Http404('Вы попали не туда. Упс...')
        elif page_number == 'v':
            # Команда очистки устаревших записей
            # (в продакшене 'page_number' делается такой, чтобы сложно было подобрать)
            delete_time = datetime.datetime.now() - datetime.timedelta(seconds=configs.OBJ_LIFETIME)
            ShortenUrl.objects.filter(added__lt=delete_time).delete()
        elif page_number and not page_number.isdigit():
            raise Http404('Страница может быть только положительным числом!')
        elif page_number and int(page_number) > paginator.num_pages:
            raise Http404('Еще нет такой далекой страницы')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj, 'form': form,
                                                    **self.extra_context, 'paginator': paginator})

    def post(self, request, *args, **kwargs):
        if not self.request.session.session_key:
            self.request.session.save()
        form = self.form_class(request.POST)
        if form.is_valid():
            short_url_in_form = form.cleaned_data['short_url_part']
            if not ShortenUrl.objects.filter(short_url_part=short_url_in_form).exists():
                try:
                    ShortenUrl.objects.create(short_url_part=short_url_in_form,
                                              original_url=form.cleaned_data['original_url'],
                                              client_session=self.request.session.session_key)

                except IntegrityError:
                    # Редкий случай: повторная запись короткого адреса, сгенерированная случайно
                    # Возможно в случае переполнения БД всеми вариантами сокращений
                    unreal_err = 'Сервис перегружен. Повторите попытку позже или обратитесь к администратору'
                    return render(request, self.template_name, {'form': form, 'unreal_err': unreal_err})
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})


def visit_world(request, short_url):
    """
    На основании сокращенной ссылки (если она существует в БД или в кеше)
    редиректим пользователя по оригинальному URL или вызываем исключение 404
    """
    return HttpResponseRedirect(db_or_cache_or_404(short_url))


class ShortenUrlListApi(generics.ListCreateAPIView, QueryMixin):
    """
    Для вывода и создания ссылок конкретного пользователя (сессии)
    """
    serializer_class = serializers.ShortenUrlSerializer
    lookup_field = 'short_url_part'

    def get_queryset(self, *args, **kwargs):
        return self.collect_data()

    def perform_create(self, serializer):
        serializer.save(client_session=self.request.session.session_key)


class ShortenUrlListApiDetail(generics.RetrieveUpdateDestroyAPIView, QueryMixin):
    """
    Для вывода, удаления, обновления выбранной записи конкретного пользователя (сессии)
    """
    serializer_class = serializers.ShortenUrlSerializer
    lookup_field = 'short_url_part'

    def get_queryset(self, *args, **kwargs):
        return self.collect_data()
