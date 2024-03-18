import spacy
import api.my_config as config
from api.tencentAPI import TextTranslateBatch



def extract_keywords_zh(text):
    """
    使用spaCy提取中文文本中的关键词。

    参数:
    text (str): 输入的文本。

    返回:
    list: 关键词列表。
    """
    # 加载中文模型
    nlp = spacy.load("zh_core_web_sm")
    doc = nlp(text)
    keywords = []
    # # 提取人物
    # people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    # # 提取地点
    # locations = [ent.text for ent in doc.ents if ent.label_ == "LOCATION"]
    # keywords.append(people);
    # keywords.append(locations);
    # print("提取的人物:", people)
    # print("提取的地点:", locations)
    # # 遍历文档中的每个词token
    for token in doc:
        # 过滤掉停用词和非名词/专有名词
        if not token.is_stop and (token.pos_ == "NOUN" or token.pos_ == "PROPN"):
            keywords.append(token.text)

    return keywords

def getTranslator(textArr=[]):
    # 你的腾讯翻译API密钥
    secret_id = config.secretId
    secret_key = config.secretKey
    # textArr = ["你是谁", "欢迎各位观众来到《名人们的童年》纪录片节目组 ！我们的节目采用直播方式为大家播出 我们的目 标是通过高科技脑电波记忆提取"]
    return TextTranslateBatch(textArr, secret_id, secret_key);

def getEnKeyWords(example_text):
    # 提取关键词
    keywords = extract_keywords_zh(example_text)
    # print("提取的关键词:", keywords)
    dealWithKeywords = getTranslator(keywords);
    return ",".join(dealWithKeywords);


# if __name__ == '__main__':
#     # 示例文本
#     example_text = "欢迎各位观众来到《名人们的童年》纪录片节目组 ！我们的节目采用直播方式为大家播出我们的目标是通过高科技脑电波记忆提取"
#     print(getEnKeyWords(example_text));
