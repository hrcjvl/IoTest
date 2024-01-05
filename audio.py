import librosa
import numpy as np
import soundfile as sf

def trim_audio(input_file, output_file, target_duration):
    # Load the input audio file
    y, sr = librosa.load(input_file)

    # Calculate the duration of the input audio file
    duration = librosa.get_duration(y=y, sr=sr)

    # Trim the audio to the target duration
    if duration > target_duration:
        samples_to_keep = int(target_duration * sr)
        y_trimmed = y[:samples_to_keep]

        # Save the trimmed audio to the output file
        sf.write(output_file, y_trimmed, sr)

        print(f"Trimmed {input_file} to {target_duration} seconds and saved to {output_file}")
    else:
        print(f"{input_file} is already shorter than {target_duration} seconds")

def calculate_mfcc(audio_file, target_length=77520):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Trim the audio to the target duration (if needed)
    if len(y) > target_length:
        y = y[:target_length]

    # Calculate MFCC (Mel-Frequency Cepstral Coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)

    # Resize the MFCC vector to the target length
    resized_mfcc = np.resize(mfcc, (target_length,))

    return resized_mfcc

def calculate_similarity(mfcc1, mfcc2):
    # Calculate cosine similarity between the two feature vectors
    similarity = np.dot(mfcc1, mfcc2) / (np.linalg.norm(mfcc1) * np.linalg.norm(mfcc2))
    return similarity

def compare_audio_files(file1, file2):
    target_length = 77520  # Set the desired length for MFCC vectors
    mfcc1 = calculate_mfcc(file1, target_length)
    mfcc2 = calculate_mfcc(file2, target_length)

    similarity = calculate_similarity(mfcc1, mfcc2)

    return round(similarity, 2)

if __name__ == "__main__":
    music_file = "D:\\Downloads\\music.wav"
    output_file = "D:\\Downloads\\output4.wav"

    # Specify the target duration based on the music file
    target_duration = librosa.get_duration(path=music_file)

    # Trim the output file to match the target duration
    trim_audio(output_file, "D:\\Downloads\\trimmed_output2.wav", target_duration)

    # Compare the trimmed files
    trimmed_file1 = "path/to/trimmed_music.wav"
    trimmed_file2 = "D:\\Downloads\\trimmed_output2.wav"
    # trimmed_file2 = "D:\\Downloads\\music.wav"

    similarity = compare_audio_files(music_file, trimmed_file2)

    print("音频相似性：", similarity)
