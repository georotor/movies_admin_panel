import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('genre'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        ordering = ("name",)
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255, unique=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        ordering = ("full_name",)
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, default='')
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class FilmworkType(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV show')

    type = models.CharField(
        _('type'),
        max_length=255,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE
    )

    file_path = models.FileField(_('file'), blank=True, upload_to='movies/')
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('movie')
        verbose_name_plural = _('movies')
        indexes = (models.Index(
            fields=('creation_date',),
            name='film_work_creation_date_idx'
        ),)


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('кинопроизведение'))
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name=_('genre')
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('movie genre')
        verbose_name_plural = _('movie genres')
        constraints = (models.UniqueConstraint(
            fields=('film_work', 'genre'),
            name='genre_film_work_idx'
        ),)


class PersonFilmworkRole(models.TextChoices):
    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('кинопроизведение'))
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name=_('person')
    )

    role = models.CharField(
        _('role'),
        max_length=255,
        choices=PersonFilmworkRole.choices,
        default=PersonFilmworkRole.ACTOR
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('movie person')
        verbose_name_plural = _('movie persons')
        constraints = (models.UniqueConstraint(
            fields=('film_work', 'person', 'role'),
            name='person_film_work_idx'
        ),)
