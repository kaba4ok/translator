# encoding: utf-8

from django.db import models

class LanguagesFromTo(models.Model):
    html_option = models.CharField(max_length=10)


class Dictionary(models.Model):
    languages = models.ForeignKey(LanguagesFromTo)
    word = models.CharField(max_length=40, db_index=True)
    translation = models.TextField()


class WordNotFound(models.Model):
    word = models.CharField(max_length=40, db_index=True)


class QueryLog(models.Model):
    text = models.CharField(max_length=70)
    time = models.DateTimeField(auto_now_add=True)
