# encoding: utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext


from .forms import TranslateForm
from . import models

def translate(request):
    context_instance = RequestContext(request)
    all_langs = models.LanguagesFromTo.objects.all()

    data = {'all_langs': all_langs}
    if not request.POST:
        return render_to_response('index.html',
                                  data,
                                  context_instance=context_instance)

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

    words = request.POST.get('words', '').strip().split()

    trans_data = [('word1', ('translation11',
                             'translation12',
                             'translation13',)),
                  ('word2', ('translation21',
                             'translation22',
                             'translation23',)),
                  ('word3', ('translation31',
                             'translation32',
                             'translation33',))]

    data['words'] = 'word1 word2 word3'
    data['trans_data'] = trans_data

    return render_to_response('index.html',
                              data,
                              context_instance=context_instance)
