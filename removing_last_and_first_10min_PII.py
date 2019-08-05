# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:09:01 2018

@author: admin
"""

import os
import urllib.request
import pandas as pd
import re
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import pandas as pd
from wit import Wit
import os
import shutil

os.chdir('D:/Audio_text')

aspen_inbound=pd.read_csv('0618_Aspen Inbound Export (1).csv')


from pydub import AudioSegment

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=100000):
    trim_ms = 0 # ms
    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size
    return trim_ms

start_trim = 10000
end_trim = 10000

for i in range(0,len(aspen_inbound)):
    m = bool(re.search('http',str(aspen_inbound.recording_url[i])))
    if(m==True):
        urllib.request.urlretrieve(aspen_inbound.recording_url[i],"D:/Audio_text/nithin/original/"+str('audio_file')+str(i)+".wav")
        print('wav_converted')
        sound = AudioSegment.from_wav("D:/Audio_text/nithin/original/"+str('audio_file')+str(i)+".wav")

        duration = len(sound)    
        trimmed_sound = sound[start_trim:duration-end_trim]
        trimmed_sound.export("D:/Audio_text/nithin/PII_remove/"+str('audio_file')+str(i)+".wav", format="wav")
        print('pii removed')
    if(m==False):
        print('url_error')

