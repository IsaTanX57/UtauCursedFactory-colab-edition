from pydub import AudioSegment
import shutil
import winsound
import sys
import subprocess
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

preview = False

consonants = []
vowels = []
consonantNames = []
vowelNames = []

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system('cls' if os.name == 'nt' else 'clear')

def GetLenght(Input):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', os.getcwd() + os.path.sep + Input], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def Crossfade(Audio1, Audio2, Crossfade, OutputName, OutputFormat):
    Sound1 = AudioSegment.from_file(Audio1)
    Sound2 = AudioSegment.from_file(Audio2)
    combined = Sound1.append(Sound2, crossfade=Crossfade)
    combined.export(OutputName, format=OutputFormat)

def transform():
    for consonant in range(len(consonants)):
        for vowel in range(len(vowels)):
            consonantLength = GetLenght(consonants[consonant])
            vowelLength = GetLenght(vowels[vowel])
            crossfadeMS = (min(consonantLength, vowelLength) * 1000) / 2
            Crossfade(consonants[consonant], vowels[vowel], crossfadeMS, f"./result/{consonantNames[consonant]}{vowelNames[vowel]}.wav", "wav")
            print(f"Processed \"{consonantNames[consonant]}{vowelNames[vowel]}\"")
            if preview:
                winsound.PlaySound(f"./result/{consonantNames[consonant]}{vowelNames[vowel]}.wav", winsound.SND_ASYNC)

def audioDetect():
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                yield [root[2:], os.path.join(root, filename), filename[:len(filename) - 4]]

print("Detecting mp3 audio files...")

for file in audioDetect():
    if file[0] == "consonants":
        consonants.append(file[1])
        consonantNames.append(file[2])
    elif file[0] == "vowels":
        vowels.append(file[1])
        vowelNames.append(file[2])

if os.path.isfile("./vowels/n.mp3"):
    consonants.append("./vowels/n.mp3")
    consonantNames.append("n")

if len(vowels) < 6:
    print(color.RED + "\nThere seems to not be enough .mp3 files in the \"vowels\" folder, did you forget to add the N sound?\n" + color.END)
    if input(color.BOLD + "Without the required audio files you won't be able to make a full minimal voicebank, do you still want to continue? (Y/N) " + color.END) != "Y":
        exit()

input(color.BOLD + f"\nI was able to detect {len(consonants)} consonants and {len(vowels)} vowels, which will output a voicebank consisting of {len(consonants) * len(vowels)} audio files in total. Press Enter to continue" + color.END)
if os.name == 'nt':
    preview = True

print("\n")

if os.path.isdir("result") == False:
    os.mkdir("result")

transform()
print("\nCopying vowels...")
for vowel in vowels:
    shutil.copy(vowel, "./result")
print("\nDone! Your voicebank is in the \"result\" folder, feel free to move it to your Utau installation")