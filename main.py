import tkinter as tk
import threading
import pyaudio
import wave
import os

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Aplicación de Chat de Voz y Texto")
ventana.geometry("400x300")

# Marco para los mensajes de texto
marco_texto = tk.Frame(ventana)
marco_texto.pack(pady=10)

# Área de texto para mostrar los mensajes
texto = tk.Text(marco_texto, height=10, width=50)
texto.pack(side=tk.LEFT, fill=tk.Y)

# Barra de desplazamiento para la zona de mensajes
scrollbar = tk.Scrollbar(marco_texto)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Vincular la barra de desplazamiento con el área de texto
texto.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=texto.yview)

# Cuadro de entrada de texto
entrada_texto = tk.Entry(ventana, font=("Helvetica", 12))
entrada_texto.pack(pady=10)

# Botón para enviar el mensaje de texto
def enviar_mensaje():
    mensaje = entrada_texto.get()
    texto.insert(tk.END, "Tú: " + mensaje + "\n")
    entrada_texto.delete(0, tk.END)

boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
boton_enviar.pack()

# Configuración de la comunicación de voz
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "grabacion.wav"

def grabar_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Guardar la grabación como archivo WAV
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def enviar_audio():
    threading.Thread(target=grabar_audio).start()

# Botón para enviar el mensaje de voz
boton_audio = tk.Button(ventana, text="Hablar", command=enviar_audio)
boton_audio.pack()

# Función para reproducir el archivo de audio
def reproducir_audio():
    os.system("aplay " + WAVE_OUTPUT_FILENAME)

# Botón para reproducir el mensaje de voz
boton_reproducir = tk.Button(ventana, text="Reproducir", command=reproducir_audio)
boton_reproducir.pack()

ventana.mainloop()
