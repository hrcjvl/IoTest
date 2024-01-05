import librosa
import numpy as np

def trim_and_compare_audio(file1, file2):
    # Load the input audio files
    y1, sr1 = librosa.load(file1)
    y2, sr2 = librosa.load(file2)

    # Calculate the duration of the input audio files
    duration1 = librosa.get_duration(y=y1, sr=sr1)
    duration2 = librosa.get_duration(y=y2, sr=sr2)

    # Trim the longer audio to the duration of the shorter audio
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

    # Calculate MFCC (Mel-Frequency Cepstral Coefficients)
    mfcc1 = librosa.feature.mfcc(y=y1_trimmed, sr=sr1)
    mfcc2 = librosa.feature.mfcc(y=y2_trimmed, sr=sr2)
    print(mfcc1.shape)

    # Resize the MFCC vectors to the minimum length
    min_length = min(mfcc1.shape[1], mfcc2.shape[1])
    mfcc1 = np.resize(mfcc1, (min_length,))
    mfcc2 = np.resize(mfcc2, (min_length,))

    # Calculate cosine similarity between the two feature vectors
    similarity = np.dot(mfcc1, mfcc2) / (np.linalg.norm(mfcc1) * np.linalg.norm(mfcc2))

    return round(similarity, 2)

if __name__ == "__main__":
    music_file = "D:\\Downloads\\music.wav"
    output_file = "D:\\Downloads\\output2.wav"

    # Compare the trimmed files
    similarity = trim_and_compare_audio(music_file, output_file)

    print("音频相似性：", similarity)

