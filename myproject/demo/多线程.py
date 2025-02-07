import threading

# 创建一个锁对象
file_lock = threading.Lock()

def modify_file(thread_name):
    # 获取锁
    file_lock.acquire()
    try:
        # 以追加模式打开文件
        with open('test.txt', 'a') as file:
            print(f"{thread_name} 正在写入文件...")
            file.write(f"这是来自 {thread_name} 的内容。\n")
            print(f"{thread_name} 写入完成。")
    except Exception as e:
        print(f"写入文件时出错: {e}")
    finally:
        # 释放锁
        file_lock.release()

# 创建线程
threads = []
for i in range(2):
    thread = threading.Thread(target=modify_file, args=(f"线程-{i + 1}",))
    threads.append(thread)
    thread.start()

# 等待所有线程执行完毕
for thread in threads:
    thread.join()

print("所有线程执行完毕。")