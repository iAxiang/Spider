import xlrd
 
excel_path = "subway_store_info.xlsx"
 
#打开文件，获取excel文件的workbook（工作簿）对象
excel = xlrd.open_workbook(excel_path,encoding_override="utf-8")

sheet = excel.sheets()

for i in sheet:
    for row in range(i.nrows):
        # print(i.row_values(row))
        data = ','.join('%s' %i for i in i.row_values(row))
        print(data)
        with open('subway_store_info.comments', 'a+', encoding='utf-8') as f:
            f.write(data + '\n')
