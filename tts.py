from gtts import gTTS
from io import BytesIO
import pygame

mp3_fp = BytesIO()
tts = gTTS('Hello, im a text to speech bot', 'en')
tts.save('test.mp3')

pygame.mixer.init()
pygame.mixer.music.load("test.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
