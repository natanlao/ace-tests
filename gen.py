# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
from jinja2 import Environment, FileSystemLoader, Template
import json
import re
import subprocess
import definitions


OUTPUT_DIR = "out/"

LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

LATEX_ENV_OPTS = {
    'block_start_string': '((*',
    'block_end_string': '*))',
    'variable_start_string': '(((',
    'variable_end_string': ')))',
    'comment_start_string': '((=',
    'comment_end_string': '=))',
}


def load_data():
    with open("data.json", "r") as d:
        data = json.load(d, "utf-8")
    return data

def create_directories(OUTPUT_DIR):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for book in data.keys():
        if not os.path.exists(os.path.join(OUTPUT_DIR, book)):
            os.makedirs(os.path.join(OUTPUT_DIR, book))

def generate(question_data, file_ext, OUTPUT_DIR, template, env, prefix):
    for bookname, book in question_data.items():
        for chapter, questions in book.items():
            fpath = os.path.join(OUTPUT_DIR, bookname, "%s%d.%s" % (prefix, int(chapter), file_ext))
            context = {
                'bookname': definitions.BOOKS[bookname]['bookname'],
                'chapter': int(chapter),
                'chapters': len(book.keys()),
                'questions': questions,
            }

            with open(fpath, "w") as c:
                env.get_template(template).stream(**context).dump(c, encoding="utf-8", errors="strict")


def generate_pdf(inpath):
    touched = False
    for root, dirs, files in os.walk(inpath):
        for f in [i for i in files if i.endswith(".tex")]:
            subprocess.call(["latexmk", "-quiet", "-pdf", f], cwd=root, stdout=open(os.devnull, "wb"))
            touched = True

        if touched:  # T_T
            subprocess.call(["latexmk", "-quiet", "-c"], cwd=root, stdout=open(os.devnull, "wb"))
            touched = False

if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader('templates/'))
    texenv = env.overlay(**LATEX_ENV_OPTS)
    texenv.filters['escape_tex'] = escape_tex

    data = load_data()
    create_directories(OUTPUT_DIR)
    generate(data, "html", OUTPUT_DIR, "chapter_questions.html", env, "chapter")
    generate(data, "tex", OUTPUT_DIR, "chapter_test.tex", texenv, "chapter")
    generate(data, "tex", OUTPUT_DIR, "answer_key.tex", texenv, "answers")
    generate_pdf(OUTPUT_DIR)


