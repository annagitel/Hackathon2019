import pyaudio
import wave

chunk = 1024
f = wave.open(r"output.wav","rb")
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)
data = f.readframes(chunk)
while data:  
    stream.write(data)  
    data = f.readframes(chunk)
stream.stop_stream()  
stream.close()  

p.terminate()  