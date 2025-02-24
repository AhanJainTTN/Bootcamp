import threading


def store_threads(thread_id, thread_set):
    thread_set.add(thread_id)


threads = []
thread_set = set()
for i in range(100):
    thread = threading.Thread(target=store_threads, args=(thread, thread_set))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Thread set size: {len(thread_set)}")
