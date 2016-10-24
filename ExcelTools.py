# -*- coding: utf-8 -*-

"""
Created on  2016/10/24
Author:     Haiyu Zhu
E-mail:     zhuhaiyu1991@163.com
"""

import xlrd
from openpyxl.workbook import Workbook
from openpyxl.workbook import Workbook


# read xls file as xlsx file
def open_xls_as_xlsx(file_path):
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    book1 = Workbook()
    sheet1 = book1.active
    if nrows != 0 and ncols != 0:
        for r in range(0, nrows):
            for c in range(0, ncols):
                sheet1.cell(row=r+1, column=c+1).value = sheet.cell_value(r, c)
    return book1


# some value in the ceil may contain space, use it carefully
def erase_space(str):
    res = ""
    for c in str:
        if c != " ":
            res += c
    return res


