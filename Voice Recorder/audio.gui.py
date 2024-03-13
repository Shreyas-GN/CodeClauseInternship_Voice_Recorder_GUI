import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox

class VoiceRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Recorder")
        self.master.geometry("400x300")
        
        self.output_file = "recorded_audio.wav"
        self.is_recording = False
        
        self.create_widgets()

    def create_widgets(self):
        self.record_button = tk.Button(self.master, text="Record", command=self.toggle_record)
        self.record_button.pack(pady=10)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.exit_app)
        self.exit_button.pack()

    def toggle_record(self):
        if not self.is_recording:
            self.record_button.config(text="Stop Recording")
            self.record_audio()
        else:
            self.record_button.config(text="Record")
            self.is_recording = False

    def record_audio(self, duration=5, sample_rate=44100, channels=2, chunk=1024):
        self.is_recording = True

        audio_format = pyaudio.paInt16
        audio = pyaudio.PyAudio()
        
        stream = audio.open(format=audio_format, channels=channels,
                            rate=sample_rate, input=True,
                            frames_per_buffer=chunk)
        
        print("Recording...")
        frames = []
        for _ in range(0, int(sample_rate / chunk * duration)):
            if not self.is_recording:
                break
            data = stream.read(chunk)
            frames.append(data)
        
        print("Recording finished.")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        with wave.open(self.output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(audio_format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        messagebox.showinfo("Recording Finished", f"Audio saved to {self.output_file}")

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
