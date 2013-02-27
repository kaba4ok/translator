from optparse import make_option
import re
import sys

from django.core.management.base import BaseCommand, CommandError
from translator.translator import models

class Command(BaseCommand):
    trans_re = re.compile('^trans:([^;]*);([^;]*);([^;]*).*$')
    lang_re = re.compile('^langs:(.*)$')

    def handle(self, *args, **kwargs):
        f = file(sys.argv[2], 'rb')
        data = {'trans': [],
                'langs': {}}

        models.Dictionary.objects.all().delete()
        models.LanguagesFromTo.objects.all().delete()

        for l in f:
            trans_matched = self.trans_re.match(l.strip())
            if trans_matched:
                lang = data['langs'].get(trans_matched.group(1))
                if not lang:
                    continue
                dict_obj = (
                    models
                    .Dictionary(languages=lang,
                                word=trans_matched
                                     .group(2)
                                     .decode('utf-8'),
                                translation=trans_matched
                                            .group(3)
                                            .decode('utf-8')))
                data['trans'].append(dict_obj)
                continue
            lang_matched = self.lang_re.match(l.strip())
            if lang_matched:
                lang_obj = models.LanguagesFromTo(
                               html_option=lang_matched
                               .group(1)
                               .decode('utf-8'))
                data['langs'][
                    lang_matched.group(1)] = lang_obj
                lang_obj.save()

        for lang in data['langs'].itervalues():
            lang.save()

        models.Dictionary.objects.bulk_create(data['trans'])
