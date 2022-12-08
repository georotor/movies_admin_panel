from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import PersonFilmworkRole, Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        films = self.model.objects.values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg(
                'persons__full_name', distinct=True, filter=Q(personfilmwork__role=PersonFilmworkRole.ACTOR)),
            directors=ArrayAgg(
                'persons__full_name', distinct=True, filter=Q(personfilmwork__role=PersonFilmworkRole.DIRECTOR)),
            writers=ArrayAgg(
                'persons__full_name', distinct=True, filter=Q(personfilmwork__role=PersonFilmworkRole.WRITER)),
        )
        return films

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return self.get_queryset().filter(id=self.kwargs['pk']).first()
