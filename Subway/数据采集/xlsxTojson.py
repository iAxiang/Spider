from collections import OrderedDict
import json
import xlrd
import codecs


def xlsxTojson(path):
    wb = xlrd.open_workbook(path)

    convert_list = []
    sh = wb.sheet_by_index(0)
    title = sh.row_values(0)
    for rownum in range(1, sh.nrows):
        rowvalue = sh.row_values(rownum)
        single = OrderedDict()
        for colnum in range(0, len(rowvalue)):
            print(title[colnum], rowvalue[colnum])
            single[title[colnum]] = rowvalue[colnum]
        convert_list.append(single)

    j = json.dumps(convert_list)

    with codecs.open('other.json', "w", "utf-8") as f:
        f.write(j)


if __name__ == '__main__':
    path = 'other.xlsx'
    xlsxTojson(path)