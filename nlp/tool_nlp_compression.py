import re
import jieba
from snownlp import SnowNLP
from sumy.nlp.stemmers import Stemmer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from common_const.normalized_const import punctuation_list
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer


# snownlp处理简单的文本语句,将语句进行压缩。limit传入整型数值,返回主要语义中排名前limit的句子.
# 可以设置punctuation,用于将返回的句子进行标点符号的串联
def __snownlp_summary_simple__(sentence, limit, punctuation):
    if sentence == '':
        return ''
    if type(sentence) != str:
        sentence = str(sentence)
    if type(limit) != int:
        raise Exception('参数代表返回摘要的句子数量,请输入整型数据!')
        return ''
    if punctuation not in punctuation_list():
        punctuation = ','
    s_compress = ''
    try:
        # 先使用jieba进行分词处理,理论上jieba对中文分析效果更好,使用分词后的结果再进行内容摘要的提取
        seg_list = jieba.cut(sentence, cut_all=False)
        seg_text = ''.join(seg_list)
        snow_nlp_sentence = SnowNLP(seg_text)
        summary_sentence = snow_nlp_sentence.summary(limit)
        if summary_sentence.__len__() == 0:
            return ''
        else:
            for i in range(len(summary_sentence)):
                if i < len(summary_sentence) - 1:
                    s_compress += summary_sentence[i] + punctuation
                else:
                    s_compress += summary_sentence[i]
            return s_compress
    except Exception as e:
        print(e)
        return ''


# snownlp处理中文文章.
# separator,用于将长文本进行切割,可以按照separator进行拆分(例如，。或者\n)
def __snownlp_summary_list__(article_text, separator):
    if article_text == '':
        return ''
    elif type(article_text) != str:
        return ''
    article_text_list = re.split(separator, article_text)
    if article_text_list.__len__() == 0:
        return ''
    fragment_list = []
    for i in range(len(article_text_list)):
        fragment_list.append(__snownlp_summary_simple__(article_text_list[i], 5, '.'))
    return ','.join(fragment_list)


# snownlp处理简单的文本语句,将语句进行压缩。limit传入整型数值,返回主要语义中排名前limit的句子.
# 可以设置punctuation,用于将返回的句子进行标点符号的串联
# sumy目前测试下来不太准,可能更适合其它场景,暂时搁置
def __sumy_summary_simple__(sentence, limit, punctuation):
    if sentence == '':
        return ''
    if type(sentence) != str:
        sentence = str(sentence)
    if type(limit) != int:
        raise Exception('参数代表返回摘要的句子数量,请输入整型数据!')
        return ''
    try:
        seg_list = jieba.cut(sentence, cut_all=False)
        seg_text = ''.join(seg_list)
        parser = PlaintextParser.from_string(seg_text, Tokenizer("chinese"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, limit)
        fragment_list = []
        for s_seg in summary:
            fragment_list.append(str(s_seg) + (punctuation if punctuation in punctuation_list() else ','))
    except Exception as e:
        print(e)
        return ''
    return ''.join(fragment_list)


# 分析句子的情感价值(正负情绪价值。越接近1表示正面情绪,越接近0表示负面情绪)
# 测试下来稍微难一点的语句准确度不高,正式使用时建议测试,可以训练自己的数据集会更准确
def __sentence_sentiments__(sentence):
    return SnowNLP(sentence).sentiments if sentence != '' else -1


# 基于模型的中文摘要输出,data传入长文本,language=chinese即分析中文,count参数
# 代表返回摘要返回的句子总数
def __long_text_summary__(data, language, count):
    parser = PlaintextParser.from_string(data, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    for sentence in summarizer(parser.document, count):
        print(sentence)


# 测试
# 该处发现一个问题,如果一个句子中没有标点符号,中间用空格连接,会对词语分析造成误解,导致失败。
# 目前发现的方法是,将所有短语用，隔开即可,是否造成误差及误差大小需要大量测试得出结果
# 可以对比下面的差异
if __name__ == '__main__':
    s1 = """
        灰色的打折 挺好的 没想到其中的隔层那么多 可以放多张卡片 大小可以放下IP14pm 够大 上面的小包可以放得下耳机盒 也可以放钥匙 肩带可调节 也够长
    """
    l = re.split(' ', s1)
    ll = []
    for i in range(len(l)):
        ll.append(l[i] + '，')
    s2 = ''.join(ll)
    ss = __snownlp_summary_simple__(s1, 3, ',')
    print(ss)
    ss = __snownlp_summary_simple__(s2, 3, ',')
    print(ss)
