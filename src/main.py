from UCDAgent import UCDAgent

# 创建一个列表来存储处理结果
processing_results = []

for i in range(1,61):
    try:
        print(f"Processing file {i}...")
        lower = ((i - 1) // 10) * 10 + 1
        upper = lower + 9
        with open(f"../datasets/60_artificial/{lower}-{upper}/{i}.txt", "r", encoding='utf-8') as file:
            input_text = file.read().strip()
        
        # 尝试创建UCDAgent并执行各种操作
        UCD = UCDAgent(input_text)
        UCD.extract_actors()
        UCD.extract_usecases()
        UCD.extract_usecase_associations()
        UCD.extract_actor_relationships()

        # 尝试保存JSON文件
        UCD.save_to_json(f"../ablation_output/Qwen_wo_SR/{i}_result.json")

        # 尝试删除和生成操作
        UCD.delete_usecases()
        UCD.delete_actor_usecases()
        UCD.generate_diagram(f"../ablation_output/Qwen_wo_DM/{i}_result.txt")

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
