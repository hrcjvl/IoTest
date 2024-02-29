
import librosa
import numpy as np

# 定义处理音频的函数
def trim_and_compare_audio(src, dest):
    # file1, file2 = args
    y1, sr1 = librosa.load(src)
    y2, sr2 = librosa.load(dest)

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
    
    return round(similarity, 2)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python audio.py <src> <dest>")
        sys.exit(1)

    src = sys.argv[1]
    dest = sys.argv[2]
    similarity = trim_and_compare_audio(src, dest)
    print(f"Similarity: {similarity}")
