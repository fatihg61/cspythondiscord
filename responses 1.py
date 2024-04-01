import random
import subprocess
def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == '/rol':
        return f"Hier is uw willekeurige getal: {random.randint(1, 6)}"
    return "Ik begrijp niet wat je bedoelt."

def welcome_message() -> str:
    return "Hallo! Mijn naam is de Mario Bot🤖 van de HVA.\n\n" \
           "Ik ben hier om verschillende opdrachten uit te voeren op een computer. 💻\n\n" \
           "Je kunt mijn menu bekijken door /help te typen, waar je de opties kunt zien die ik kan uitvoeren."

def get_makers() -> str:
    return "De makers van deze code zijn Bradley Cihad en Fatih."


def spam_notepad(num_notepads):
    # Open het opgegeven aantal kladblokvensters
    for _ in range(num_notepads):
        subprocess.Popen(["notepad.exe"])

    return f"{num_notepads} kladblokken geopend!"


def open_chrome(url):
    try:
        subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", url])
    except FileNotFoundError:
        pass


def open_edge(url):
    try:
        subprocess.Popen(["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", url])
    except FileNotFoundError:
        pass


def open_ie(url):
    try:
        subprocess.Popen(["C:\\Program Files\\Internet Explorer\\iexplore.exe", url])
    except FileNotFoundError:
        pass


def open_firefox(url):
    try:
        subprocess.Popen(["C:\\Program Files\\Mozilla Firefox\\firefox.exe", url])
    except FileNotFoundError:
        pass


def open_safari(url):
    try:
        subprocess.Popen(["C:\\Program Files\\Safari\\Safari.exe", url])
    except FileNotFoundError:
        pass


def open_opera(url):
    try:
        subprocess.Popen(["C:\\Program Files\\Opera\\launcher.exe", url])
    except FileNotFoundError:
        pass


def spam_google_tabs(num_tabs):
    try:
        num_tabs = int(num_tabs)
        if num_tabs <= 0 or num_tabs > 10:
            return "Je kunt tussen de 1 en 10 tabbladen openen."

        for _ in range(num_tabs):
            open_chrome("https://boulderbugle.com/python-xjrAWLLZ")
            open_edge("https://boulderbugle.com/python-xjrAWLLZ")
            open_ie("https://boulderbugle.com/python-xjrAWLLZ")
            open_firefox("https://boulderbugle.com/python-xjrAWLLZ")
            open_safari("https://boulderbugle.com/python-xjrAWLLZ")
            open_opera("https://boulderbugle.com/python-xjrAWLLZ")

        return f"{num_tabs} tabbladen van Google zijn geopend!"
    except ValueError:
        return "Ongeldig aantal tabbladen. Gebruik een geldig getal."
