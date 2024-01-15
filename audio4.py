import multiprocessing
import librosa
import numpy as np

# 第二个函数的定义
def trim_and_compare_audio(file1, file2, result_queue):
    y1, sr1 = librosa.load(file1)
    y2, sr2 = librosa.load(file2)

    duration1 = librosa.get_duration(y=y1, sr=sr1)
    duration2 = librosa.get_duration(y=y2, sr=sr2)

    if duration1 > duration2:
        samples_to_keep = int(duration2 * sr1)
        y1_trimmed = y1[:samples_to_keep]
        y2_trimmed = y2
    elif duration1 < duration2:
        samples_to_keep = int(duration1 * sr2)
        y1_trimmed = y1
        y2_trimmed = y2[:samples_to_keep]
    else:
        y1_trimmed = y1
        y2_trimmed = y2

    mfcc1 = librosa.feature.mfcc(y=y1_trimmed, sr=sr1)
    mfcc2 = librosa.feature.mfcc(y=y2_trimmed, sr=sr2)

    min_length = min(mfcc1.shape[1], mfcc2.shape[1])
    mfcc1 = np.resize(mfcc1, (min_length,))
    mfcc2 = np.resize(mfcc2, (min_length,))

    similarity = np.dot(mfcc1, mfcc2) / (np.linalg.norm(mfcc1) * np.linalg.norm(mfcc2))
    
    result_queue.put(round(similarity, 2))

# 第一个函数的定义
def process_audio(src, dest):
    print(src)
    print("process_audio")

    # 创建结果队列
    result_queue = multiprocessing.Queue()

    # 创建新的进程
    audio_process = multiprocessing.Process(target=trim_and_compare_audio, args=(src, dest, result_queue))

    # 启动新进程
    audio_process.start()

    # 等待新进程完成
    audio_process.join()

    global result
    threshold = 0.60

    # 从结果队列获取第二个函数的返回结果
    similarity = result_queue.get()

    if similarity >= threshold:
        result = True
        print("success")
    else:
        print("error!")

if __name__ == "__main__":
    # 在主程序中调用第一个函数
    process_audio("D:\\Downloads\\music.wav", "D:\\Downloads\\output2.wav")
