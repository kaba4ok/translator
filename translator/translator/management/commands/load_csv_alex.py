# encoding: utf-8

import sys

from django.core.management.base import BaseCommand, CommandError
from translator.translator import models


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        f = file(sys.argv[2], 'rb')
        models.Dictionary.objects.all().delete()
        dict_models = []
        lang = None
        for l in f:
            l = l.strip().decode('utf-8')
            if l.startswith('lang:'):
                lang = models.LanguagesFromTo.objects.get(html_option=l[5:])
                print lang
                continue
            if not lang:
                continue
            l_splitted = l.split(';')[:2]
            if len(l_splitted) != 2:
                continue
            word = ' '.join(l_splitted[0].strip().split())
            if len(word) > 40:
                continue
            translation = ' '.join(l_splitted[1].strip().split())
            dict_models.append(models.Dictionary(languages=lang,
                                                 word=word,
                                                 translation=translation))
        f.close()
        models.Dictionary.objects.bulk_create(dict_models)
        print 'created %d records' % len(dict_models)
