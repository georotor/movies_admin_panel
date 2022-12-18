from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models import Person, Genre, Filmwork, PersonFilmwork, GenreFilmwork


class FilmworkDateTimeFilter(DateFieldListFilter):
    """Добаляет в стандартный фильтр по дате возможность фильтрции за предыдцщий год."""
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(
            field,
            request,
            params,
            model,
            model_admin,
            field_path
        )

        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            today = now.date()

        prev_year = today.replace(year=today.year - 1, month=1, day=1)

        self.links += ((
            (_('Prev year'), {
                self.lookup_kwarg_since: str(prev_year),
                self.lookup_kwarg_until: str(today.replace(month=1, day=1)),
            }),
        ))


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)
    list_display = ('full_name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)

    list_display = ('title', 'type', 'creation_date', 'rating',)
    list_filter = ('type', ('creation_date', FilmworkDateTimeFilter),)
    search_fields = ('title', 'description', 'id',)

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}
