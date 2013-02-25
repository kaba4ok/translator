# encoding: utf-8

from collections import defaultdict
import re

from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import TranslateForm
from . import models

word_re = re.compile('\w+')
def translate(request):
    context_instance = RequestContext(request)
    all_langs = models.LanguagesFromTo.objects.all()

    data = {'all_langs': all_langs}
    def get_response():
        return render_to_response('index.html',
                                  data,
                                  context_instance=context_instance)
    if not request.POST:
        return get_response()

    lang = None

    try:
        lang_id = int(request.POST.get('lang', '-1'))
    except (TypeError, KeyError):
        lang_id = -1

    for l in all_langs:
        if lang_id == l.id:
            l.selected = True
            lang = l
            break

    if not lang:
        return get_response()

    words_str = request.POST.get('words', '').strip()
    if not words_str:
        return get_response()

    log_record = models.QueryLog(text=words_str[:70])
    log_record.save()

    words = words_str.split()
    translations = models.Dictionary.objects.filter(languages=lang,
                                                    word__in=words)
    trans_data = defaultdict(list)
    words_set = set(words)
    words_found = set()

    for trans in translations:
        trans_data[trans.word].append(trans.translation)
        words_found.add(trans.word)

    words_not_found = words_set - words_found

    for word in words_not_found:
        models.WordNotFound(word=word).save()

    data['words'] = words_str
    data['trans_data'] = trans_data.items()

    return get_response()
