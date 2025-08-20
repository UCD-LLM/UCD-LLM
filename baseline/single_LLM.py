import requests
import json
import logging
import ast
import re
import time
from openai import OpenAI, RateLimitError, APIConnectionError, APIError
from config import OPENAI_API_KEY, OPENAI_MODEL, BASE_URL


def openai_chat_completion(system_prompt: str, history: list, temperature=0, max_tokens=512, max_retries=3,
                           retry_delay=1):
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

# 创建一个列表来存储处理结果
processing_results = []

for i in range(1,61):
    try:
        print(f"Processing file {i}...")
        lower = ((i - 1) // 10) * 10 + 1
        upper = lower + 9
        with open(f"../datasets/60_artificial/{lower}-{upper}/{i}.txt", "r", encoding='utf-8') as file:
            input_text = file.read().strip()
        single_LLM_prompt = open("single_LLM_template.txt", encoding='utf-8').read()
        filled_prompt = single_LLM_prompt.format_map({"input_text": input_text})
        messages = [{"role": "user", "content": filled_prompt}]
        completion = openai_chat_completion("You are an expert in the field of requirement modeling", messages)
        try:
            data_str = completion.strip().replace("json","").replace("```","").strip()
            data = json.loads(data_str)
            with open(f"GLM_single/{i}_result.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("JSON字符串验证成功并已写入文件")
        except json.JSONDecodeError as e:
            print(f"无效的JSON格式: {e}")

        # 记录成功结果
        result = f"File {i} processed successfully."
        print(result)
        processing_results.append((i, True, "Success"))

    except FileNotFoundError:
        error_msg = f"Error: File not found for iteration {i}. Check the file path."
        print(error_msg)
        processing_results.append((i, False, "File not found"))
    except PermissionError:
        error_msg = f"Error: Permission denied when accessing files for iteration {i}."
        print(error_msg)
        processing_results.append((i, False, "Permission denied"))
    except IOError as e:
        error_msg = f"Error: I/O error occurred for iteration {i}: {str(e)}"
        print(error_msg)
        processing_results.append((i, False, f"I/O error: {str(e)}"))
    except Exception as e:
        error_msg = f"Error: An unexpected error occurred for iteration {i}: {str(e)}"
        print(error_msg)
        processing_results.append((i, False, f"Unexpected error: {str(e)}"))
    finally:
        # 可以在这里添加任何需要始终执行的清理代码
        pass

# 处理完成后，输出所有结果摘要
print("\n=== Processing Summary ===")
for result in processing_results:
    file_num, success, message = result
    status = "SUCCESS" if success else "FAILED"
    print(f"File {file_num}: {status} - {message}")

# 可选：统计成功和失败的数量
success_count = sum(1 for _, success, _ in processing_results if success)
failure_count = len(processing_results) - success_count
print(f"\nTotal files processed: {len(processing_results)}")
print(f"Successful: {success_count}")
print(f"Failed: {failure_count}")
