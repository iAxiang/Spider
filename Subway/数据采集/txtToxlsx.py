import os
import openpyxl as xl

def txtToxlsx(fileName, xlsName):
    result_path = os.path.join(xlsName)
    print(result_path)
    print('***** 开始写入excel文件 ' + result_path + ' ***** \n')
    if os.path.exists(result_path):
        print('***** excel已存在，在表后添加数据 ' + result_path + ' ***** \n')
        workbook = xl.load_workbook(result_path)
    else:
        print('***** excel不存在，创建excel ' + result_path + ' ***** \n')
        workbook = xl.Workbook()
        workbook.save(result_path)
    sheet = workbook.active
    # headers = ["URL", "predict", "score"]
    # sheet.append(headers)
    # result = [['1', 1, 1], ['2', 2, 2], ['3', 3, 3]]
    with open(fileName, 'r', encoding='utf-8') as f:
        line = f.readlines()
        for i in line:
            item = i.split(',')
            print(item)
            sheet.append(item)
    workbook.save(result_path)
    print('***** 生成Excel文件 ' + result_path + ' ***** \n')
txtToxlsx('subwayStoreInfo.comments', 'subwayStoreInfo.xlsx')