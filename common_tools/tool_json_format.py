# 封装处理json数据的功能
from common_tools.tool_file_operation import txt_save
import json


# 将输入的json中全部的key转成list格式返回
def get_json_keys(json_s):
    try:
        if json_s is None:
            return None
        _json_s = json.loads(json.dumps(json_s))
        ks = _json_s[0].keys()
        for k in ks:
            if k is None or k == '':
                raise Exception('输入描述缺失请重新传入!!!')
                return None
                break
            else:
                return list(ks)
    except Exception as e:
        print(e)
        return None


# 讲AI返回的类json数据进行格式化
def ai_json_format(json_str):
    json_str = json_str.replace('```json', '').replace('```', '').replace('\n', '')
    if '},' not in json_str:
        s1 = json_str.replace('}', '},')
        s2 = s1[0:len(s1) - 1]
        json_comment = s2
    else:
        json_comment = json_str

    if '[' not in json_comment:
        json_comment = '[' + json_comment + ']'

    try:
        return json.loads(json_comment)
    except Exception as e:
        print(e)
        txt_save(json_comment + '\n', '', 'comments_exception_data.txt', 'utf-8')
        return ''


def merge_results(results):
    # 假设results是一个列表，其中每个元素也是一个列表，包含一个字典
    # 我们想要合并所有的字典到一个单一的列表中
    merged_list = []
    for result in results:
        # 假设每个result是一个列表，只包含一个字典
        if isinstance(result, list) and len(result) == 1 and isinstance(result[0], dict):
            merged_list.append(result[0])
        else:
            raise ValueError("Each result should be a list containing a single dictionary.")
    return merged_list
