import subprocess as sp 

def voice_sint(query, voice_id):

    if voice_id == 0:
        voice = "./piper/ru_RU-ruslan-medium.onnx"
    elif voice_id == 1:
        voice = "./piper/ru_RU-denis-medium.onnx"

    sp.Popen(f"echo {query} | piper/piper --model {voice} --output_file output.wav", shell=True)

if __name__ == "__main__":
    voice_sint('Да ладно хуй с ним, пошло всё в пизду, сколько можно блять!?', 0) 
