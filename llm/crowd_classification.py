from langchain.output_parsers import ResponseSchema
from common_tools.tool_json_format import ai_json_format
import json

from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from llm.llm_azure_v import get_azure_llm


def crowd_classification(crowd_lists, examples, request_prefix, request_suffix, version, t):
    if crowd_lists is None:
        return ''
    if not isinstance(crowd_lists, list):
        return ''

    example_template = '人群编号:{id},人群:{crowd},交集条件为{intersect},目标群体为{target},排除条件为{except}'
    response_schemas = [
        ResponseSchema(name="id", description="人群编号", type="int"),
        ResponseSchema(name="category", description="分类结果")
    ]

    input_variables = ["人群编号", "人群"]

    fact = llm_examples_prompt(examples, example_template, response_schemas, request_prefix, request_suffix,
                               input_variables, version, t)
    result = fact.invoke(crowd_lists)
    return ai_json_format(result['text'])


def llm_examples_prompt(examples, example_template, response_schemas, request_prefix, request_suffix, request_text,
                        version, t):
    llm = get_azure_llm(version, t)

    input_variables = ['id', 'crowd', 'intersect', 'target', 'except']
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
        prefix=request_prefix + '\n分析出的人群编号和对应的分类结果必须以此{format_instructions}格式化\n',
        suffix=request_suffix,
        input_variables=request_text,
        partial_variables={"format_instructions": format_instructions}
    )
    return LLMChain(llm=llm, prompt=prompt)
