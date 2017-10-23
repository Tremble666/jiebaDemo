import jieba
import jieba.analyse
import re
from string import punctuation
import jieba.posseg as pseg
# 引入TF-IDF关键词抽取接口
tfidf = jieba.analyse.extract_tags
textrank = jieba.analyse.textrank
class myJB:
    def __init__(self,src):
        #self.src为所读取的文本文档路径，self.target为分词后的保存文档路径
        self.src = src
    #仅保留中文，进行分词，并保存最重文本
    #标注句子分词后每个词的词性，采用和 ictclas 兼容的标记法
    def cut_all(self,target):
        with open(self.src,'r') as fread:
            str1 = fread.read()
            #将读取文本进行筛选，仅保留中文文本
            pureText=''.join(re.findall(u'[\u4e00-\u9fff]+', str1))
            #结巴精确模式进行分词，返回结果为一个生成器
            seg_list = pseg.cut(pureText)
            with open(target,'a') as fwrite:
                for ele,flag in seg_list:
                    fwrite.write(ele + ' ' + flag + '\n')
            fwrite.close()
        fread.close()
    #添加用户自定义词库
    def add_dict(self,path):
        jieba.load_userdict(path)
    #添加用户自定义词
    def add(self,word): 
        jieba.add_word (word)
    # 基于TF-IDF算法进行关键词抽取
    #topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
    #withWeight 为是否一并返回关键词权重值，默认值为 False
    #allowPOS 仅包括指定词性的词，默认值为空，即不筛选
    def extract_key_tfidf(self,target):
        with open(self.src,'r') as fread:
            text = fread.read()
            keywords = tfidf(text, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
            with open(target,'a') as fwrite:
                fwrite.write('keywords by TF-IDF:\n')
                for keyword,flag in keywords:
                    fwrite.write(str(keyword) + '\n')
            fwrite.close()
        fread.close()
    # 基于TextRank算法进行关键词抽取
    def extract_key_textrank(self,target):
        with open(self.src,'r') as fread:
            text = fread.read()
            keywords = textrank(text, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
            with open(target,'a') as fwrite:
                fwrite.write('keywords by TextRank:\n')
                for keyword in keywords:
                    fwrite.write(str(keyword) + '\n')
            fwrite.close()
        fread.close()   
if __name__ == '__main__':
    j1 = myJB('C:\\Users\\chenjin\\Desktop\\python\\专业实训\\src.txt')
    #j1.add_dict("C:\\Users\\chenjin\\Desktop\\python\\专业实训\\userdict.txt")
    #j1.add('很好看')
    j1.cut_all('C:\\Users\\chenjin\\Desktop\\python\\专业实训\\target.txt')
    j1.extract_key_tfidf('C:\\Users\\chenjin\\Desktop\\python\\专业实训\\key1.txt')
    j1.extract_key_textrank('C:\\Users\\chenjin\\Desktop\\python\\专业实训\\key2.txt')
