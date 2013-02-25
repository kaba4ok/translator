# encoding: utf-8

from django.db import models


class LanguagesFromTo(models.Model):
    html_option = models.CharField(max_length=10,
                                   verbose_name=u'Направление')

    class Meta:
        verbose_name = u'Направление перевода'
        verbose_name_plural = u'Направления перевода'

    def __unicode__(self):
        return self.html_option


class Dictionary(models.Model):
    languages = models.ForeignKey(LanguagesFromTo,
                                  verbose_name=u'Направление перевода')
    word = models.CharField(max_length=40, db_index=True,
                            verbose_name=u'Слово')
    translation = models.TextField(verbose_name=u'Перевод')

    class Meta:
        verbose_name = u'Запись словаря'
        verbose_name_plural = u'Словарь'


class WordNotFound(models.Model):
    word = models.CharField(max_length=40, db_index=True, primary_key=True,
                            verbose_name=u'Слово')

    def __unicode__(self):
        return self.word

    class Meta:
        verbose_name = u'Ненайденное слово'
        verbose_name_plural = u'Ненайденные слова'


class QueryLog(models.Model):
    text = models.CharField(max_length=70,
                            verbose_name=u'Запрос')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'Запрос'
        verbose_name_plural = u'Лог запросов'
