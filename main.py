from typing import Dict, List

import jieba
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel

from llm.comments_analyze import comments_analyze
from nlp.tool_nlp_compression import __snownlp_summary_simple__
from llm.crowd_classification import crowd_classification  # 引入你的人群分类模块
import logging
import logging.handlers

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('fastapi')  # 获取FastAPI的日志记录器
log_file_path = 'app.log'  # 日志文件路径
handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 100,
                                               backupCount=5)  # 设置文件处理器，最大大小100MB，最多保留5个备份
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 设置日志格式
handler.setFormatter(formatter)
logger.addHandler(handler)

# 设置FastAPI使用自定义的日志记录器
logging.getLogger('uvicorn.error').setLevel(logging.INFO)
logging.getLogger('uvicorn.access').setLevel(logging.INFO)

app = FastAPI()


# 定义请求体模型
class CommentAnalysisRequest(BaseModel):
    comment_lists: list = Body(...)
    examples: str = Body(...)
    request_prefix: str = Body(...)
    request_suffix: str = Body(...)
    version: int = Body(...)
    t: int = Body(...)


class CrowdClassificationRequest(BaseModel):
    crowd_lists: list = Body(...)
    examples: str = Body(...)
    request_prefix: str = Body(...)
    request_suffix: str = Body(...)
    version: int = Body(...)
    t: int = Body(...)


# 定义FastAPI路由
@app.post("/analyze_comments")
async def analyze_comments(request_data: CommentAnalysisRequest):
    comment_lists = request_data.comment_lists
    examples = request_data.examples
    request_prefix = request_data.request_prefix
    request_suffix = request_data.request_suffix
    version = request_data.version
    t = request_data.t

    logger.info(f"Received analyze_comments request with {len(request_data.comment_lists)} comments.")

    # 调用你的comments_analyze函数
    result = comments_analyze(comment_lists, examples, request_prefix, request_suffix, version, t)

    # 返回结果，这里我们假设ai_json_format返回的是一个字典
    return result


@app.post("/classify_crowds")
async def classify_crowds(request_data: CrowdClassificationRequest):
    crowd_lists = request_data.crowd_lists
    examples = request_data.examples
    request_prefix = request_data.request_prefix
    request_suffix = request_data.request_suffix
    version = request_data.version
    t = request_data.t

    logger.info(f"Received classify_crowds request with {len(request_data.crowd_lists)} crowds.")

    # 调用你的人群分类函数
    result = crowd_classification(crowd_lists, examples, request_prefix, request_suffix, version, t)

    # 返回结果，这里我们假设ai_json_format返回的是一个字典
    return result


class Question(BaseModel):
    comment: str
    id: int  # 明确指定id为整数类型


@app.post("/summary")
async def summary(
        questions: List[Question] = Body(..., description="输入需要提取摘要的问题列表，每个问题包含comment和id字段"),
        limit: int = Body(..., description="返回的摘要句子数量", gt=0),
        punctuation: str = Body('.', description="句子之间的分隔符")):
    summaries = []
    logger.info(f"Received summary request with {len(questions)} comments.")

    for question in questions:
        comment = question.comment
        compress_comment = __snownlp_summary_simple__(comment, limit, punctuation)
        summaries.append({'comment': compress_comment, 'id': question.id})  # 使用question.id来获取整数id
    if not summaries:
        raise HTTPException(status_code=400, detail="无法生成摘要")
    return {"summaries": summaries}

@app.post("/cut")
async def summary(question: str = Body('.', description="句子之间的分隔符")):
    question = question.replace(" ","")
    seg_list = jieba.cut(question, cut_all=False)
    return seg_list


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # 运行FastAPI应用，监听所有接口在8000端口
