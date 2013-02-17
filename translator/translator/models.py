# encoding: utf-8

from django.db import model

class LangaugesFromTo(models.Model):
    html_option = models.CharField(max_length=10)


class Dictionary(models.Model):
    languages = models.ForeignKey(LangaugesFromTo)
    word = models.CharField(max_length=40, db_index=True)
    translation = models.TextField()

