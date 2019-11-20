from ibm_watson import SpeechToTextV1
from os.path import join, dirname
import json
from ibm_watson import TextToSpeechV1
import csv
import re
from ibm_watson.natural_language_understanding_v1 \
    import *
import pyaudio
import wave
import sounddevice as sd
from scipy.io.wavfile import write
from  tkinter import *
import tkinter.scrolledtext

#start answer recording
def on_hold(seconds=5):
    fs = 44100
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    return write('output.wav', fs, myrecording)



#stop answer recording
def on_relaese(sd):
    sd.stop()

# calling the TtoS tool from the IBM cloud
text_to_speech = TextToSpeechV1(
    iam_apikey='FuabejLeSlCUpIyh-woGfIy5Dx4JNVhgl1piYMiYEAR9',
    url='https://gateway-lon.watsonplatform.net/text-to-speech/api'
)


# Take a String and return a WAV file
def text_to_audio(text):
    x = re.sub('["?]', "", text)
    name = str(x + '.wav')
    print(type(name))
    print(name)
    with open(name, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text,
                voice='en-US_AllisonVoice',
                accept='audio/wav'
            ).get_result().content)

    return name

def playAudio(audioFile):
    chunk = 1024
    f = wave.open(audioFile, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    data = f.readframes(chunk)
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    stream.stop_stream()
    stream.close()

    p.terminate()


# Go over a CSV file and send to "text_to_audio"
with open('Question_Answer.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for i in range (1):
        row1 = next(csv_reader)





# geting the "transcrint" value from the Json item got from the StoT func
def id_generator(json_input, lookup_key="transcript"):
    if isinstance(json_input, dict):
        for k, v in json_input.iteritems():
            if k == lookup_key:
                yield v
            else:
                for child_val in id_generator(v, lookup_key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in id_generator(item, lookup_key):
                yield item_val

#function gets the Json answer from the StoT function, returns the key word

def speech_to_text():
    # calling to the StoT tool from the IBM cloud
    speech_to_text = SpeechToTextV1(
        iam_apikey='OZeac4xlSe-tv1wP1rsyV0BsIYzEmTyp83H_pwdzQPFl',
        url='https://gateway-lon.watsonplatform.net/speech-to-text/api')
    with open(join(dirname(__file__), './.', 'output.wav'),
               'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav',
            word_alternatives_threshold=0.9,
            keywords=['colorado', 'tornado', 'tornadoes'],
            keywords_threshold=0.5).get_result()
        return(json.dumps(speech_recognition_results, indent=2))

# calling the NLU tool from the ibm cloud
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='WUNkJebT8d9wFP-tUq3jcq0cXZTnjLk5hAmygy8KJ-tJ',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api')

def nlu(text):
    nlu = ''
    response = natural_language_understanding.analyze(
        features=Features(
            relations=RelationArgument(),
            concepts=ConceptsOptions(),
            categories=CategoriesOptions(),
            semantic_roles=SemanticRolesKeyword(),
            entities=EntitiesOptions(sentiment=True, limit=10),
            keywords=KeywordsOptions(sentiment=True, limit=10))).get_result()
    print(json.dumps(response, indent=2))
    for i in id_generator(text):
        nlu = i
    return nlu


###############################################################################
def master(q,a):
 playAudio(text_to_audio(q))
 on_hold()
 userAnswer = speech_to_text()
 find_transcript = "There are opals underground."
 print("2")
 if (a.find(userAnswer) != -1):
   playAudio(text_to_audio("good job"))

 else:
    playAudio(text_to_audio("good job"))
def total():
 master('Why do many people come to Coober Pedy?','To become rich.')

if __name__ == '__main__':
    # -- coding: utf-8 --
    root = tkinter.Tk()
    root.title("tkinter scrolledtext Example")
    root.geometry('400x600+300+200')
    scrolledtext = tkinter.scrolledtext.ScrolledText(root)
    scrolledtext.pack(fill="both", expand=True)
    text = "There is a treasure in the town of Coober Pedy, Australia. It is a treasure you cannot see because it is under the ground.\n This treasure is special stones called opals. Opals are very valuable. Many people come to Coober Pedy to look for opals because they hope to get rich.\n You can sell a perfect opal for a million dollars.You will also see other unusual things in Coober Pedy. There are signs that tell you to be careful\n because there are holes in the ground. You will also see many doors in the hills. This is because opals aren’t the only things under the ground in Coober\n Pedy. Today, 1,500 people live and work under the ground. So there are shops restaurants and even a bookstore under the ground. Why do they\n live under the ground? The answer is simple: to stay cool. It is very hot outside! The temperature can reach 50 degrees in the summer.\n But the temperature underground will always be a comfortable 24 degrees. underground has other advantages. It’s quiet.\n This makes it easy to get a good night’s sleep. Also, there isn't any sunlight to wake you up. And the best thing is you can dig for opals\n under your own home and maybe get rich."
    scrolledtext.insert(tkinter.INSERT, text)
    b1 = Button(root, text="play", activeforeground="black", activebackground="black", pady=10, command=lambda: total())
    b1.pack(side=BOTTOM)
    root.mainloop()





