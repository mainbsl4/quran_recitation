import whisper
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher

model = whisper.load_model("large")

def audio_to_text(audio_file_path):
    global model
    result = model.transcribe(audio_file_path, language="ar")
    return result["text"]


user_text = audio_to_text("./1. Surah Al-Fatihah 1st verse.mp3")
print(user_text)



def highlight_differences(original, compared):
    matcher = SequenceMatcher(None, original, compared)

    output = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            output.append(original[i1:i2])
        elif tag == 'replace':
            output.append(f"[REPLACE: '{original[i1:i2]}' → '{compared[j1:j2]}']")
        elif tag == 'delete':
            output.append(f"[DELETE: '{original[i1:i2]}']")
        elif tag == 'insert':
            output.append(f"[INSERT: '{compared[j1:j2]}']")

    return ''.join(output)


def word_level_diff(original, compared):
    from difflib import Differ

    words1 = original.split()
    words2 = compared.split()

    d = Differ()
    diff = list(d.compare(words1, words2))

    return ' '.join(diff)



# input_sentence = "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"
input_sentence = user_text.strip()


sentence_list = [
  "بسم الله الرحمن الرحيم",
  "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
  "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
  "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
  "قُلْ هُوَ اللَّهُ أَحَدٌ",
  "اللَّهُ الصَّمَدُ",
  "لَمْ يَلِدْ وَلَمْ يُولَدْ",
  "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ",
  "إِنَّ اللَّهَ مَعَ الَّذِينَ اتَّقَوْا وَالَّذِينَ هُم مُّحْسِنُونَ",
  "وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا",
  "وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ فَهَلْ مِن مُّدَّكِرٍ"
]

# ==================================================from qwen
def show_tashkeel_mistakes(original, user_text):
    # Arabic diacritics (tashkeel) range
    tashkeel_chars = set('َ ً ُ ٌ ِ ٍ ّ ْ ٰ'.split())

    mistakes = []

    # We'll compare char by char, focusing on presence/absence of tashkeel
    min_len = min(len(original), len(user_text))
    for i in range(min_len):
        orig_char = original[i]
        user_char = user_text[i]

        # If the base letter is same but tashkeel differs
        if orig_char != user_char:
            if orig_char in tashkeel_chars:
                mistakes.append(f"[MISSING TASHKEEL] Position {i}: Expected '{orig_char}' (in '{original[i-1:i+2]}')")
            elif user_char in tashkeel_chars:
                mistakes.append(f"[EXTRA TASHKEEL] Position {i}: Found '{user_char}' (in '{user_text[i-1:i+2]}')")
            else:
                # Base letter mismatch
                mistakes.append(f"[LETTER MISMATCH] '{orig_char}' vs '{user_char}' at position {i}")

    # Check if user text is shorter (missing tashkeel at end)
    if len(original) > len(user_text):
        for i in range(len(user_text), len(original)):
            if original[i] in tashkeel_chars:
                mistakes.append(f"[MISSING TASHKEEL at end] '{original[i]}'")

    return mistakes


# ===========================================================================


matches = [(sentence, fuzz.ratio(input_sentence, sentence)) for sentence in sentence_list]
matches.sort(key=lambda x: x[1], reverse=True)

best_match_sentence, score = matches[0]


print("Top match found:")
print(f"Sentence: {best_match_sentence}")
print(f"Similarity Score: {score}%")
print("\nDifferences highlighted:")
print(highlight_differences(input_sentence, best_match_sentence))

print("\nDifferences word-by-word:")
print(word_level_diff(input_sentence, best_match_sentence))

# ================================================================fron qwen
print("\n=== تَشْكِيل (Tashkeel) এবং উচ্চারণের ভুল ===")
mistakes = show_tashkeel_mistakes(best_match_sentence, input_sentence)
if mistakes:
    for m in mistakes:
        print(m)
else:
    print("✅ তাশকীল এবং উচ্চারণ সঠিক আছে।")