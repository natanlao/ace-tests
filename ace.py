#!/usr/bin/env python
from bs4 import BeautifulSoup
from definitions import BOOKS as books
import json
import requests

# data = {
#     book: {
#         chapter_id: {
#             question_id: {
#                 question_text: question_text_here,
#                 answer_choice_letter: {
#                     answer_is_correct: boolean,
#                     answer_text: text_here,
#                     answer_explanation: explanation_here, }
#             }
#         }
#     }
# }


_data = {}


for bookname, book in books.iteritems():
    WORKFLOW_BASE_URL = book["workflow"]
    QUESTION_BASE_URL = book["question"]
    chapters = book["chapters"]
    _data[bookname] = {}
    DATA = _data[bookname]

    for chapter in chapters:
        DATA[chapter] = {}

        _r = requests.get(WORKFLOW_BASE_URL.format(chapter=chapter)).content
        wflow = BeautifulSoup(_r)

        questions = wflow.find("workflow-elements").findChildren()
        lastq = int(questions[-2].get("id").split("_")[-1].lstrip("q"))

        for question_id in xrange(1, lastq + 1):
            _r = requests.get(QUESTION_BASE_URL.format(chapter=chapter, question=question_id)).content
            question = BeautifulSoup(_r)
            question_text = question.find("matflash", label="qstem").flashmixed.flashtext.text.strip()

            DATA[chapter][question_id] = {
                "question": question_text,
            }

            for answer in question.find_all("response_label"):
                letter = answer.get("ident")
                text = answer.material.mat_extension.flash.matflash.flashmixed.flashtext.text.strip()
                correct = True if answer.get("labelrefid") == "select" else False
                expl_tree = question.find("itemfeedback", ident="feedback_{0}".format(letter))
                explanation = expl_tree.material.mat_extension.flash.matflash.flashtext.text.strip()

                DATA[chapter][question_id][letter] = {
                    'text': text,
                    'correct': correct,
                    'explanation': explanation
                }


with open("data.json", "w") as dfile:
    json.dump(_data, dfile)
