import requests
import json
import logging
import ast
import re
import time
from openai import OpenAI, RateLimitError, APIConnectionError, APIError
from config import OPENAI_API_KEY, OPENAI_MODEL, BASE_URL

def openai_chat_completion(system_prompt: str, history: list, temperature=0, max_tokens=512, max_retries=3, retry_delay=1):
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=BASE_URL
    )
    if system_prompt is not None:
        messages = [{"role": "system", "content": system_prompt}] + history
    else:
        messages = history
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL, 
                messages=messages, 
                temperature=temperature, 
                max_tokens=max_tokens
            )
            print(f"LLM输出: {response.choices[0].message.content}\n")
            return response.choices[0].message.content
        except APIConnectionError as e:
            retry_count += 1
            print(f"连接错误: {e}. 正在重试 {retry_count}/{max_retries}...")
            if retry_count < max_retries:
                time.sleep(retry_delay)
        except RateLimitError as e:
            retry_count += 1
            print(f"速率限制错误: {e}. 正在重试 {retry_count}/{max_retries}...")
            if retry_count < max_retries:
                time.sleep(retry_delay * 2)  # 速率限制错误时增加延迟
        except APIError as e:
            retry_count += 1
            print(f"API错误: {e}. 正在重试 {retry_count}/{max_retries}...")
            if retry_count < max_retries:
                time.sleep(retry_delay)
        except Exception as e:
            print(f"未知错误: {e}")
            break
    
    # 如果所有重试都失败，返回错误信息
    return f"请求失败，已达到最大重试次数 {max_retries}"

# 解析原始字符串列表
def parse_raw_list_answers(raw_list_answers: str):
    parsed_list = []
    left_bracket_idx = raw_list_answers.index("[")
    right_bracket_idx = raw_list_answers.index("]")
    if left_bracket_idx == -1 or right_bracket_idx == -1 or right_bracket_idx <= left_bracket_idx:
        logging.debug(f"Invalid format in raw_list_answers: {raw_list_answers}")
        return parsed_list
    try:
        parsed_list = ast.literal_eval(raw_list_answers[left_bracket_idx : right_bracket_idx + 1])
    except Exception as e:
        pass
    logging.debug(f"List {raw_list_answers} parsed as {parsed_list}")
    return parsed_list

def get_opinion(option, usecase1, usecase2):
    # 定义映射关系
    relation_map = {
        'A': ['Inclusion relationship, ', ' must depend on ', ' '],
        'B': ['Inclusion relationship, ', ' must depend on ', ' '],
        'C': ['Extension relationship, ', ' is an optional behavior under specific conditions based on ', ' '],
        'D': ['Extension relationship, ', ' is an optional behavior under specific conditions based on ', ' '],
        'E': ['Generalization relationship, ', ' inherits the behavior of ', ' and adds new behaviors '],
        'F': ['Generalization relationship, ', ' inherits the behavior of ', ' and adds new behaviors '],
        'G': ['No relationship, ', ' and ', ' are independent of each other '],
    }
    map_list = relation_map[option]
    debater_opinion = ''
    if (ord(option) - ord('A')) % 2 == 0:
        debater_opinion = f'{map_list[0]}{usecase1}{map_list[1]}{usecase2}{map_list[2]}'
    else:
        debater_opinion = f'{map_list[0]}{usecase2}{map_list[1]}{usecase1}{map_list[2]}'
    return debater_opinion

# 解析参与者泛化关系原始输出
def parse_raw_tuple(raw_tuple: str):
    parsed_tuple = ()
    # 使用正则表达式提取括号内的内容
    match = re.search(r'\((.*?)\)', raw_tuple)
    if match:
        content = match.group(1)
        # 分割内容并去除多余的空格和引号
        items = [item.strip().strip("'\"") for item in content.split(',')]
        if len(items) == 2:
            parsed_tuple = (items[0], items[1])
            return parsed_tuple
    logging.debug(f"Invalid format in raw_tuple: {raw_tuple}")
    return None

# def parse_raw_tuple(raw_tuple: str):
#     parsed_tuple = ()
#     left_bracket_idx = raw_tuple.index("(")
#     right_bracket_idx = raw_tuple.index(")")
#     if left_bracket_idx == -1 or right_bracket_idx == -1 or right_bracket_idx <= left_bracket_idx:
#         logging.debug(f"Invalid format in raw_tuple: {raw_tuple}")
#         return None
#     try:
#         parsed_tuple = ast.literal_eval(raw_tuple[left_bracket_idx : right_bracket_idx + 1])
#     except Exception as e:
#         pass
#     logging.debug(f"Tuple {raw_tuple} parsed as {parsed_tuple}")
#     return parsed_tuple

# result = parse_raw_tuple("('Actor1', 'Actor2')")  # Example usage, can be removed in production code
# print(result)  # Should print: ('Actor1', 'Actor2') if the input is valid
