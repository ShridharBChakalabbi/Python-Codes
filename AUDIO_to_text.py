import os
os.chdir("E:/chuncks")

import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
myaudio = AudioSegment.from_file("C:/Users/Sridhar/Downloads/201802061702400132110000049268-1 (online-audio-converter.com).wav" , "wav") 
inp=input("enter chunk size in Sec:")
chunk_length_ms = int(inp)*1000
chunks = make_chunks(myaudio, chunk_length_ms)
print("The audio file content is writing to task.csv:")

filename = "task.csv"
f = open(filename, "w")
headers = "chunks, content, start_time, end_time \n"
f.write(headers)
for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    chunk.export(chunk_name, format="wav")
    start_time = i+ (i*int(inp))
    end_time = start_time + int(inp)
    print ("exporting", chunk_name)
    r=sr.Recognizer()

    with sr.AudioFile(chunk_name) as source:
        audio=r.record(source)
    
    try:
        print("chunks: " + chunk_name)
        print("content: " + r.recognize_google(audio))
        print(start_time)
        print(end_time)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not results from google speech recognition service; {0}").format(e)
    f.write(str(chunk_name)+ "," + str(r.recognize_google(audio))+ "," + str(start_time)+ "," + str(end_time) + "\n")
f.close()
        