# -*- coding: utf-8 -*-

BOOKS = {
    "USHIST": {
        "bookname": "The American Pageant, 12e",
        "workflow": "http://college.cengage.com/history/us/kennedy/am_pageant/12e/assets/students/ace/data/workflow_{chapter:02d}.xml",
        "question": "http://college.cengage.com/history/us/kennedy/am_pageant/12e/assets/students/ace/data/his_us_kennedy_{chapter:02d}_q{question:02d}.xml",
        "chapters": xrange(1, 42 + 1),
    },
    "EUHIST": {
        "bookname": "A History of Western Society, 9e",
        "workflow": "http://college.cengage.com/history/west/mckay/western_society/9e/assets/students/ace/data/workflow_{chapter:02d}.xml",
        "question": "http://college.cengage.com/history/west/mckay/western_society/9e/assets/students/ace/data/mckay_ace_ch{chapter:02d}_q{question:02d}.xml",
        "chapters": xrange(1, 31 + 1),
    },
}