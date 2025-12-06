import wave
import math
import struct
import random

def create_jump_sound(filename):
    # 產生一個頻率上升的音效 (跳躍音)
    duration = 0.2 # 秒
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1) # 單聲道
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)
        
        data = []
        for i in range(n_samples):
            t = i / sample_rate
            # 頻率從 300Hz 上升到 600Hz
            freq = 300 + (300 * t / duration)
            # 正弦波
            value = int(32767 * 0.5 * math.sin(2 * math.pi * freq * t))
            data.append(struct.pack('<h', value))
            
        wav_file.writeframes(b''.join(data))
    print(f"Created {filename}")

def create_victory_sound(filename):
    # 產生一個簡單的勝利音效 (琶音)
    sample_rate = 44100
    notes = [523.25, 659.25, 783.99, 1046.50] # C E G C (C Major arpeggio)
    note_duration = 0.15
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        data = []
        for freq in notes:
            n_samples = int(sample_rate * note_duration)
            for i in range(n_samples):
                t = i / sample_rate
                # 簡單的方波/正弦波混合，聽起來比較像 8-bit
                value = int(32767 * 0.3 * math.sin(2 * math.pi * freq * t))
                data.append(struct.pack('<h', value))
                
        wav_file.writeframes(b''.join(data))
    print(f"Created {filename}")

if __name__ == "__main__":
    create_jump_sound("jump.wav")
    create_victory_sound("victory.wav")
