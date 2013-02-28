# encoding: utf-8

from collections import defaultdict
import re

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import TranslateForm
from . import models
from . import admin

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

    words_splitted = words_str.split()
    words = [' '.join(words_splitted)] + words_splitted

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
        models.WordNotFound(word=word[:40]).save()

    data['words'] = words_str
    data['trans_data'] = trans_data.items()

    return get_response()

def load_dictionary(request):
    response = redirect(reverse('admin:translator_dictionary_changelist'))
    if not request.POST or not request.FILES:
        return response
    lang_id = request.POST.get('lang')

    try:
        lang_id = int(lang_id)
    except (TypeError, ValueError):
        return response

    try:
        lang = models.LanguagesFromTo.objects.get(id=lang_id)
    except models.LanguagesFromTo.DoesNotExist:
        return response

    dictionary = set(tuple(d)
                     for d in models
                              .Dictionary
                              .objects
                              .filter(languages=lang)
                              .values_list('word', 'translation'))

    data_to_dictionary = []
    for file in request.FILES.itervalues():
        data = file.read()
        try:
            data = data.decode('utf-8')
        except UnicodeDecodeError:
            continue
        for l in data.split('\n'):
            l_splitted = l.strip().split(';')[:2]
            if len(l_splitted) != 2:
                continue
            word = ' '.join(l_splitted[0].strip().split())
            translation = ' '.join(l_splitted[1].strip().split())
            if not (word, translation) in dictionary:
                data_to_dictionary.append(models.Dictionary(languages=lang,
                                                            word=word,
                                                            translation=translation))
                
    if data_to_dictionary:
        models.Dictionary.objects.bulk_create(data_to_dictionary)

    messages.add_message(request,
                         messages.INFO,
                         "Добавлено записей: %d" % len(data_to_dictionary))
    return response
