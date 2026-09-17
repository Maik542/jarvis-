# =====================================================================
# STEP 1: IMPORT THE REQUIRED LIBRARIES
# =====================================================================
# 'pyaudio' connects Python to your computer's microphone hardware.
import pyaudio

# 'numpy' handles large lists of numbers (audio waves are just numbers).
import numpy as np

# 'WhisperModel' is the artificial intelligence that turns voice numbers into text letters.
from faster_whisper import WhisperModel

# =====================================================================
# STEP 2: LOADING THE AI MODEL
# =====================================================================
print("Loading model locally... Please wait...")

# We load the "tiny" model because it is small and fast enough for a normal computer.
# 'device="cpu"' means your main processor handles the work (no fancy graphics card needed).
# 'compute_type="int8"' compresses the model size so it doesn't max out your RAM.
model = WhisperModel("base", device="cpu", compute_type="int8")

# =====================================================================
# STEP 3: CONFIGURE THE MICROPHONE AUDIO SETTINGS
# =====================================================================
# 'paInt16' means the audio will record using 16-bit integers (standard digital audio format).
FORMAT = pyaudio.paInt16

# '1' means Mono audio (1 microphone channel). We do not need Stereo (2 channels) for talking.
CHANNELS = 1

# '16000' means the mic samples audio 16,000 times per second. Whisper demands exactly this speed.
RATE = 16000

# '1024' is the buffer chunk size. Python will grab audio in small bite-sized pieces of 1,024 numbers.
CHUNK = 1024

# Initialize PyAudio so Python knows how to interact with Windows sound devices.
p = pyaudio.PyAudio()

# Open the microphone stream channel with the settings we defined above.
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,             # 'True' means we are RECORDING input, not playing sound output.
    frames_per_buffer=CHUNK
)

print("\n=== Jarvis Listening (Local & Offline) ===")
print("Speak into your mic. Press Ctrl+C in the terminal window to stop.\n")

# This empty list [] will hold the raw audio data chunks as they stream in from the mic.
audio_frames = []

# =====================================================================
# STEP 4: THE CONTINUOUS LISTENING LOOP
# =====================================================================
try:
    while True:
        # Grab 1,024 samples of raw audio bytes from the active mic stream.
        data = stream.read(CHUNK)
        
        # Throw those raw bytes into our audio accumulation list.
        audio_frames.append(data)
        
        # Math check: (RATE / CHUNK) is how many chunks happen in 1 second.
        # We multiply by 3 to wait until we have roughly 3 full seconds of speech saved up.
        if len(audio_frames) >= int(RATE / CHUNK * 3):
            
            # Glue all the small, separate bytes chunks together into one single giant byte string.
            raw_audio = b"".join(audio_frames)
            
            # Convert the raw bytes into a numpy array of numbers. 
            # Then divide by 32768.0 to turn those numbers into tiny decimals between -1.0 and 1.0.
            # Whisper requires this exact decimal format to read audio correctly.
            audio_np = np.frombuffer(raw_audio, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Feed the decimal audio array to the AI.
            # 'beam_size=1' makes it pick the fastest translation guess instantly.
            # 'vad_filter=True' stands for Voice Activity Detection. It filters out dead room silence.
            segments, info = model.transcribe(audio_np, beam_size=1, vad_filter=True)
            
            # Loop through whatever sentences the AI managed to pull out of the audio.
            for segment in segments:
                # '.strip()' removes any useless blank spaces from the front or back of the text.
                # If there are actual words left inside the text, print it.
                if segment.text.strip():
                    print(f">> {segment.text}", flush=True)
            
            # Wipe the list completely clean so it's empty for your next sentence.
            # If we don't clear it, the AI will keep rereading your old words over and over.
            audio_frames = []

# =====================================================================
# STEP 5: CLEAN UP AFTER STOPPING
# =====================================================================
except KeyboardInterrupt:
    # If the user presses Ctrl+C, jump down here instead of crashing with an ugly error screen.
    print("\nStopping stream...")

finally:
    # Safely tell the microphone to stop recording.
    stream.stop_stream()
    
    # Close down the audio channel so it doesn't get stuck open in Windows background processes.
    stream.close()
    
    # Fully shut down PyAudio to free up system memory.
    p.terminate()
    
    print("Jarvis is offline.")
