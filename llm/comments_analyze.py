from langchain.output_parsers import ResponseSchema
from common_tools.tool_json_format import ai_json_format
import json

from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from llm.llm_azure_v import get_azure_llm


def comments_analyze(comment_lists, examples, request_prefix, request_suffix, version, t):
    if comment_lists is None:
        return ''
    if not isinstance(comment_lists, list):
        return ''

    example_template = '评论编号:{id},商品评论:{comment},一级分类为{level1},二级分类为{level2},三级分类为{level3}'
    response_schemas = [
        ResponseSchema(name="id", description="评论编号", type="int"),
        ResponseSchema(name="level1", description="一级分类"),
        ResponseSchema(name="level2", description="二级分类"),
        ResponseSchema(name="level3", description="三级分类")
    ]

    input_variables = ["评论编号", "评论"]

    fact = llm_examples_prompt(examples, example_template, response_schemas, request_prefix, request_suffix,
                               input_variables, version, t)
    result = fact.invoke(comment_lists)
    return ai_json_format(result['text'])


def llm_examples_prompt(examples, example_template, response_schemas, request_prefix, request_suffix, request_text,
                        version, t):

    llm = get_azure_llm(version, t)

    input_variables = ['id', 'comment', 'level1', 'level2', 'level3']
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    example_prompt = PromptTemplate(
        input_variables=input_variables,
        template=example_template
    )
    examples_list = json.loads(examples)

    prompt = FewShotPromptTemplate(
        examples=examples_list,
        example_prompt=example_prompt,
        prefix=request_prefix + '\n分析出的评论编号、对应的一级分类、二级分类、三级分类必须以此{format_instructions}格式化\n',
        suffix=request_suffix,
        input_variables=request_text,
        partial_variables={"format_instructions": format_instructions}
    )
    return LLMChain(llm=llm, prompt=prompt)
