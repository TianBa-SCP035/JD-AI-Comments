# 封装对于文件类的操作

# 数据保存到txt文件中,含中文字符encoding需传入utf-8
def txt_save(datas, file_path, file_name, encoding):
    if file_name is None or file_name == '':
        raise Exception('文件名称为空!!')
    try:
        if encoding == '':
            encoding = 'gbk'
        with open(file_path + file_name, 'a', encoding=encoding) as file:
            file.write(str(datas))
    except Exception as e:
        print(e)
