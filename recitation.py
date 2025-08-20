# import whisper
# from fuzzywuzzy import fuzz
# from difflib import SequenceMatcher

# # Load Whisper model
# model = whisper.load_model("large")

# # Convert audio to text (Arabic)
# def audio_to_text(audio_file_path):
#     global model
#     result = model.transcribe(audio_file_path, language="ar")
#     return result["text"].strip()

# # Function to highlight character-level differences
# def highlight_differences(original, compared):
#     matcher = SequenceMatcher(None, original, compared)

#     output = []
#     for tag, i1, i2, j1, j2 in matcher.get_opcodes():
#         if tag == 'equal':
#             output.append(original[i1:i2])
#         elif tag == 'replace':
#             output.append(f"\n❌ Pronunciation mismatch: '{original[i1:i2]}' → '{compared[j1:j2]}'")
#         elif tag == 'delete':
#             output.append(f"\n❌ Missing in input: '{original[i1:i2]}'")
#         elif tag == 'insert':
#             output.append(f"\n❌ Extra in input: '{compared[j1:j2]}'")

#     return ''.join(output) if output else "✅ Perfect pronunciation (with tashdid & harakat)"

# # Function to highlight word-level differences
# def word_level_diff(original, compared):
#     words1 = original.split()
#     words2 = compared.split()

#     d = SequenceMatcher(None, words1, words2)
#     differences = []
#     for tag, i1, i2, j1, j2 in d.get_opcodes():
#         if tag == 'replace':
#             differences.append(f"❌ Word mismatch: '{' '.join(words1[i1:i2])}' → '{' '.join(words2[j1:j2])}'")
#         elif tag == 'delete':
#             differences.append(f"❌ Missing word: '{' '.join(words1[i1:i2])}'")
#         elif tag == 'insert':
#             differences.append(f"❌ Extra word: '{' '.join(words2[j1:j2])}'")

#     return "\n".join(differences) if differences else "✅ All words correct"

# # ---- MAIN EXECUTION ----

# # Step 1: Get transcription from audio
# input_sentence = audio_to_text("./1. Surah Al-Fatihah 1st verse.mp3")
# print("🎤 Transcribed Text from Audio:")
# print(input_sentence)

# # Step 2: Reference sentences (Quran Ayat list)
# sentence_list = [
#   "بسم الله الرحمن الرحيم",
#   "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
#   "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
#   "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
#   "قُلْ هُوَ اللَّهُ أَحَدٌ",
#   "اللَّهُ الصَّمَدُ",
#   "لَمْ يَلِدْ وَلَمْ يُولَدْ",
#   "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ",
#   "إِنَّ اللَّهَ مَعَ الَّذِينَ اتَّقَوْا وَالَّذِينَ هُم مُّحْسِنُونَ",
#   "وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا",
#   "وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ فَهَلْ مِن مُّدَّكِرٍ"
# ]

# # Step 3: Find the best match
# matches = [(sentence, fuzz.ratio(input_sentence, sentence)) for sentence in sentence_list]
# matches.sort(key=lambda x: x[1], reverse=True)
# best_match_sentence, score = matches[0]

# print("\n✅ Top match found:")
# print(f"Reference Sentence: {best_match_sentence}")
# print(f"Similarity Score: {score}%")

# # Step 4: Show differences
# print("\n🔎 Character-level check:")
# print(highlight_differences(input_sentence, best_match_sentence))

# print("\n🔎 Word-level check:")
# print(word_level_diff(input_sentence, best_match_sentence))
# #
















# import whisper
# from fuzzywuzzy import fuzz
# from difflib import SequenceMatcher
# import re

# # Load Whisper model
# model = whisper.load_model("large")

# # Convert audio to text (Arabic)
# def audio_to_text(audio_file_path):
#     global model
#     result = model.transcribe(audio_file_path, language="ar")
#     return result["text"].strip()

# # Character-level differences
# def highlight_differences(original, compared):
#     matcher = SequenceMatcher(None, original, compared)
#     output = []
#     for tag, i1, i2, j1, j2 in matcher.get_opcodes():
#         if tag == 'equal':
#             output.append(original[i1:i2])
#         elif tag == 'replace':
#             output.append(f"\n❌ Pronunciation mismatch: '{original[i1:i2]}' → '{compared[j1:j2]}'")
#         elif tag == 'delete':
#             output.append(f"\n❌ Missing in input: '{original[i1:i2]}'")
#         elif tag == 'insert':
#             output.append(f"\n❌ Extra in input: '{compared[j1:j2]}'")
#     return ''.join(output) if output else "✅ Perfect pronunciation (with tashdid & harakat)"

# # Word-level differences
# def word_level_diff(original, compared):
#     words1 = original.split()
#     words2 = compared.split()
#     d = SequenceMatcher(None, words1, words2)
#     differences = []
#     for tag, i1, i2, j1, j2 in d.get_opcodes():
#         if tag == 'replace':
#             differences.append(f"❌ Word mismatch: '{' '.join(words1[i1:i2])}' → '{' '.join(words2[j1:j2])}'")
#         elif tag == 'delete':
#             differences.append(f"❌ Missing word: '{' '.join(words1[i1:i2])}'")
#         elif tag == 'insert':
#             differences.append(f"❌ Extra word: '{' '.join(words2[j1:j2])}'")
#     return "\n".join(differences) if differences else "✅ All words correct"

# # Harakat / Tashdid checker
# def check_harakat(original, compared):
#     # Arabic diacritics set
#     diacritics = {
#         "َ": "Fatha",
#         "ً": "Tanwin Fath",
#         "ِ": "Kasra",
#         "ٍ": "Tanwin Kasr",
#         "ُ": "Damma",
#         "ٌ": "Tanwin Damm",
#         "ْ": "Sukun",
#         "ّ": "Shadda"
#     }

#     issues = []
#     for i, (o_char, c_char) in enumerate(zip(original, compared)):
#         if o_char != c_char:
#             if o_char in diacritics or c_char in diacritics:
#                 issues.append(f"❌ Harakat mismatch at pos {i}: '{o_char}' → '{c_char}'")

#     if not issues:
#         return "✅ All Harakat & Tashdid correct"
#     return "\n".join(issues)

# # ---- MAIN EXECUTION ----

# # Step 1: Get transcription from audio
# input_sentence = audio_to_text("./1. Surah Al-Fatihah 1st verse.mp3")
# print("🎤 Transcribed Text from Audio:")
# print(input_sentence)

# # Step 2: Reference sentences (Quran Ayat list)
# sentence_list = [
#   "بسم الله الرحمن الرحيم",
#   "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
#   "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
#   "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
#   "قُلْ هُوَ اللَّهُ أَحَدٌ",
#   "اللَّهُ الصَّمَدُ",
#   "لَمْ يَلِدْ وَلَمْ يُولَدْ",
#   "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ",
#   "إِنَّ اللَّهَ مَعَ الَّذِينَ اتَّقَوْا وَالَّذِينَ هُم مُّحْسِنُونَ",
#   "وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا",
#   "وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ فَهَلْ مِن مُّدَّكِرٍ"
# ]

# # Step 3: Find the best match
# matches = [(sentence, fuzz.ratio(input_sentence, sentence)) for sentence in sentence_list]
# matches.sort(key=lambda x: x[1], reverse=True)
# best_match_sentence, score = matches[0]

# print("\n✅ Top match found:")
# print(f"Reference Sentence: {best_match_sentence}")
# print(f"Similarity Score: {score}%")

# # Step 4: Show differences
# print("\n🔎 Character-level check:")
# print(highlight_differences(input_sentence, best_match_sentence))

# print("\n🔎 Word-level check:")
# print(word_level_diff(input_sentence, best_match_sentence))

# print("\n🔎 Harakat & Tashdid check:")
# print(check_harakat(input_sentence, best_match_sentence))




































# import whisper
# from fuzzywuzzy import fuzz
# from difflib import SequenceMatcher
# import re

# # --- Load Whisper model ---
# model = whisper.load_model("large")

# # --- Arabic diacritics / tashkeel set ---
# ARABIC_DIACRITICS = set([
#     '\u0610','\u0611','\u0612','\u0613','\u0614','\u0615','\u0616','\u0617','\u0618','\u0619','\u061A',
#     '\u064B','\u064C','\u064D','\u064E','\u064F','\u0650','\u0651','\u0652','\u0653','\u0654','\u0655'
# ])
# # make a small friendly map name (optional)
# DIACRITIC_NAMES = {
#     "َ": "Fatha", "ً": "Tanwin-Fath", "ِ": "Kasra", "ٍ": "Tanwin-Kasr",
#     "ُ": "Damma", "ٌ": "Tanwin-Damm", "ْ": "Sukun", "ّ": "Shadda"
# }

# # --- Utility: transcribe audio to text (Arabic) ---
# def audio_to_text(audio_file_path):
#     global model
#     result = model.transcribe(audio_file_path, language="ar")
#     return result["text"].strip()

# # --- Utility: split text into base characters with attached diacritics ---
# def split_bases_and_diacritics(text):
#     """
#     Return list of tuples: [(base_char, diacritics_str), ...]
#     Spaces and punctuation are returned as base chars with empty diacritics.
#     """
#     parts = []
#     for ch in text:
#         if not parts:
#             parts.append([ch, ""])
#             continue
#         if ch in ARABIC_DIACRITICS:
#             # append diacritic to last base (if any)
#             parts[-1][1] += ch
#         else:
#             # new base character
#             parts.append([ch, ""])
#     # convert to tuples
#     return [(b, d) for b, d in parts]

# # --- Character-level diff with clear messages ---
# def highlight_differences(original, compared):
#     matcher = SequenceMatcher(None, original, compared)
#     output = []
#     for tag, i1, i2, j1, j2 in matcher.get_opcodes():
#         if tag == 'equal':
#             output.append(original[i1:i2])
#         elif tag == 'replace':
#             output.append(f"\n❌ Replace: '{original[i1:i2]}'  →  '{compared[j1:j2]}'")
#         elif tag == 'delete':
#             output.append(f"\n❌ Missing in input: '{original[i1:i2]}'")
#         elif tag == 'insert':
#             output.append(f"\n❌ Extra in input: '{compared[j1:j2]}'")
#     return ''.join(output) if output else "✅ No character-level differences."

# # --- Word-level diff (word alignment) ---
# def word_level_diff(original, compared):
#     words1 = original.split()
#     words2 = compared.split()
#     d = SequenceMatcher(None, words1, words2)
#     differences = []
#     for tag, i1, i2, j1, j2 in d.get_opcodes():
#         if tag == 'replace':
#             differences.append(f"❌ Word mismatch: '{' '.join(words1[i1:i2])}' → '{' '.join(words2[j1:j2])}'")
#         elif tag == 'delete':
#             differences.append(f"❌ Missing word: '{' '.join(words1[i1:i2])}'")
#         elif tag == 'insert':
#             differences.append(f"❌ Extra word: '{' '.join(words2[j1:j2])}'")
#     return "\n".join(differences) if differences else "✅ All words correct."

# # --- Harakat & Tashdid (Shadda) checker ---
# def check_harakat_and_tashdid(original, compared):
#     """
#     Compares diacritics and specifically checks presence/absence of Shadda (ّ).
#     Returns a dict with lists of issues and a brief summary.
#     """
#     o_list = split_bases_and_diacritics(original)
#     c_list = split_bases_and_diacritics(compared)

#     # Build sequences of base chars only for alignment
#     o_bases = [b for b, d in o_list]
#     c_bases = [b for b, d in c_list]

#     sm = SequenceMatcher(None, o_bases, c_bases)
#     issues = []
#     pos_index = 0  # base-character index approximate (counts matched bases)
#     for tag, i1, i2, j1, j2 in sm.get_opcodes():
#         if tag == 'equal':
#             # iterate through matched ranges and compare diacritics
#             for oi, ci in zip(range(i1, i2), range(j1, j2)):
#                 o_base, o_diac = o_list[oi]
#                 c_base, c_diac = c_list[ci]
#                 # Check shadda specifically
#                 o_has_shadda = 'ّ' in o_diac
#                 c_has_shadda = 'ّ' in c_diac
#                 if o_has_shadda and not c_has_shadda:
#                     issues.append(f"❌ Missing Shadda (ّ) on '{o_base}' at base-pos {oi} (expected shadda).")
#                 elif (not o_has_shadda) and c_has_shadda:
#                     issues.append(f"❌ Extra Shadda (ّ) on '{c_base}' at base-pos {ci} (input has shadda but reference doesn't).")
#                 # Check other diacritics differences (presence/absence)
#                 # list diacritics except shadda
#                 o_other = ''.join([ch for ch in o_diac if ch != 'ّ'])
#                 c_other = ''.join([ch for ch in c_diac if ch != 'ّ'])
#                 if o_other != c_other:
#                     issues.append(f"❌ Diacritics differ on '{o_base}' at base-pos {oi}: expected '{o_other or '—'}' vs input '{c_other or '—'}'.")
#                 pos_index += 1
#         elif tag == 'replace':
#             # Bases differ -> but still check if diacritics include shadda and warn
#             # For each pair in ranges, report base mismatch and diacritic differences if any
#             length = max(i2 - i1, j2 - j1)
#             for k in range(length):
#                 oi = i1 + k
#                 ci = j1 + k
#                 o_text = o_list[oi] if oi < len(o_list) else ("—", "")
#                 c_text = c_list[ci] if ci < len(c_list) else ("—", "")
#                 issues.append(f"❌ Base mismatch at base-pos approx {oi}: expected '{o_text[0]}' (diacritics '{o_text[1] or '—'}') → input '{c_text[0]}' (diacritics '{c_text[1] or '—'}').")
#         elif tag == 'delete':
#             for oi in range(i1, i2):
#                 o_base, o_diac = o_list[oi]
#                 if 'ّ' in o_diac:
#                     issues.append(f"❌ Missing base (and its Shadda) in input at base-pos {oi}: '{o_base}' with diacritics '{o_diac}'")
#                 else:
#                     issues.append(f"❌ Missing base in input at base-pos {oi}: '{o_base}'")
#         elif tag == 'insert':
#             for ci in range(j1, j2):
#                 c_base, c_diac = c_list[ci]
#                 if 'ّ' in c_diac:
#                     issues.append(f"❌ Extra base in input with Shadda at base-pos {ci}: '{c_base}' (diacritics '{c_diac}')")
#                 else:
#                     issues.append(f"❌ Extra base in input at base-pos {ci}: '{c_base}' (diacritics '{c_diac or '—'}')")

#     summary = "✅ No harakat/tashdid issues." if not issues else f"❌ Found {len(issues)} harakat/tashdid issues."
#     return {"summary": summary, "issues": issues}

# # --- MAIN EXECUTION ---
# if __name__ == "__main__":
#     # 1) Transcribe audio
#     audio_path = "./1. Surah Al-Fatihah 1st verse.mp3"
#     input_sentence = audio_to_text(audio_path)
#     print("🎤 Transcribed Text:")
#     print(input_sentence)
#     print("-" * 60)

#     # 2) Reference sentences list (you can extend)
#     sentence_list = [
#       "بسم الله الرحمن الرحيم",
#       "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
#       "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
#       "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
#       "قُلْ هُوَ اللَّهُ أَحَدٌ",
#       "اللَّهُ الصَّمَدُ",
#       "لَمْ يَلِدْ وَلَمْ يُولَدْ",
#       "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ",
#       "إِنَّ اللَّهَ مَعَ الَّذِينَ اتَّقَوْا وَالَّذِينَ هُم مُّحْسِنُونَ",
#       "وَعِبَادُ الرَّحْمَٰنِ الَّذِينَ يَمْشُونَ عَلَى الْأَرْضِ هَوْنًا",
#       "وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ فَهَلْ مِن مُّدَّكِرٍ"
#     ]

#     # 3) Find best match using fuzzy ratio (keeps original diacritics; no normalization)
#     matches = [(sentence, fuzz.ratio(input_sentence, sentence)) for sentence in sentence_list]
#     matches.sort(key=lambda x: x[1], reverse=True)
#     best_match_sentence, score = matches[0]

#     print("✅ Top match (reference):")
#     print(best_match_sentence)
#     print(f"Similarity score: {score}%")
#     print("-" * 60)

#     # 4) Character-level & word-level diffs
#     print("🔎 Character-level differences:")
#     print(highlight_differences(input_sentence, best_match_sentence))
#     print("-" * 40)
#     print("🔎 Word-level differences:")
#     print(word_level_diff(input_sentence, best_match_sentence))
#     print("-" * 40)

#     # 5) Harakat & Tashdid check (detailed)
#     harakat_report = check_harakat_and_tashdid(best_match_sentence, input_sentence)
#     print("🔎 Harakat & Tashdid check summary:")
#     print(harakat_report["summary"])
#     if harakat_report["issues"]:
#         print("\nDetailed issues:")
#         for issue in harakat_report["issues"]:
#             print(issue)
#     else:
#         print("No issues found.")






























# # -*- coding: utf-8 -*-
# """
# কুরআন উচ্চারণ ও তাসদীদ (শাদ্দা) চেকার
# ------------------------------------------
# এই কোড:
# - অডিও থেকে আরবি টেক্সট তৈরি করবে
# - শাদ্দা (ـّ) চেক করবে
# - উচ্চারণের মান মূল্যায়ন করবে
# - ত্রুটি ছাড়াই কাজ করবে
# """

# import torch
# import torchaudio
# from transformers import AutoProcessor, Wav2Vec2ForCTC
# from fuzzywuzzy import fuzz
# from difflib import SequenceMatcher
# import warnings

# # ওয়ার্নিং উপেক্ষা করুন (torchaudio ভবিষ্যতের জন্য সতর্ক করছে)
# warnings.filterwarnings("ignore", category=UserWarning, module="torchaudio")

# # ========================================
# # 1. মডেল লোড (আরবি সমর্থনকারী)
# # ========================================
# print("🔄 মডেল লোড হচ্ছে...")

# try:
#     # processor = AutoProcessor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
#     # model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53")
#     processor = AutoProcessor.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-arabic")
#     model = Wav2Vec2ForCTC.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-arabic")
#     print("✅ মডেল সফলভাবে লোড হয়েছে!")
# except Exception as e:
#     print("❌ মডেল লোড করতে ব্যর্থ হয়েছে:", str(e))
#     print("💡 ইন্টারনেট চালু করুন বা ভিপিএন ব্যবহার করুন।")
#     print("💡 অথবা ম্যানুয়ালি মডেল ডাউনলোড করুন।")
#     exit(1)  # মডেল না থাকলে প্রোগ্রাম বন্ধ করুন

# # ========================================
# # 2. শাদ্দা (Tasdid) চেক ফাংশন
# # ========================================
# def has_shadda(text):
#     """টেক্সটে শাদ্দা (ـّ) আছে কিনা চেক করে"""
#     SHADDA = '\u0651'  # Unicode for شَدَّة
#     return SHADDA in text

# # ========================================
# # 3. অডিও থেকে টেক্সট তৈরি
# # ========================================
# def audio_to_text(audio_path, processor, model):
#     """
#     অডিও ফাইল থেকে আরবি টেক্সট তৈরি করে
#     :param audio_path: অডিও ফাইলের পাথ
#     :param processor: Wav2Vec2 প্রসেসর
#     :param model: Wav2Vec2 মডেল
#     :return: ট্রান্সক্রাইবড টেক্সট
#     """
#     try:
#         speech, rate = torchaudio.load(audio_path)
#     except Exception as e:
#         print("❌ অডিও ফাইল লোড করতে ব্যর্থ:", str(e))
#         exit(1)

#     # 16kHz এ রিস্যাম্পল (Wav2Vec2 এর জন্য জরুরি)
#     if rate != 16000:
#         resampler = torchaudio.transforms.Resample(orig_freq=rate, new_freq=16000)
#         speech = resampler(speech)
#     speech = speech.squeeze().numpy()

#     # মডেল ইনপুট
#     inputs = processor(speech, sampling_rate=16000, return_tensors="pt", padding=True)

#     # ট্রান্সক্রিপশন
#     with torch.no_grad():
#         logits = model(inputs.input_values).logits
#     predicted_ids = torch.argmax(logits, dim=-1)
#     transcription = processor.decode(predicted_ids[0])
#     return transcription.strip()

# # ========================================
# # 4. উচ্চারণ ও তাসদীদ মূল্যায়ন
# # ========================================
# def check_pronunciation_and_tasdid(user_audio, reference_text, processor, model):
#     """
#     উচ্চারণ ও শাদ্দা চেক করে
#     """
#     print("🔊 অডিও থেকে টেক্সট তৈরি হচ্ছে...")
#     user_text = audio_to_text(user_audio, processor, model)
#     print(f"🗣️ ব্যবহারকারী বলেছেন: {user_text}")
#     print(f"📖 সঠিক আয়াত: {reference_text}")

#     # মিল স্কোর
#     similarity = fuzz.ratio(user_text, reference_text)
#     print(f"\n📊 মিল: {similarity}%")

#     # শাদ্দা চেক
#     ref_has = has_shadda(reference_text)
#     user_has = has_shadda(user_text)

#     print(f"\n🔍 শাদ্দা পরীক্ষা:")
#     print(f"  সঠিক টেক্সটে শাদ্দা আছে: {ref_has}")
#     print(f"  ব্যবহারকারীর টেক্সটে শাদ্দা আছে: {user_has}")

#     if ref_has and not user_has:
#         print("❌ ⚠️ তাসদীদ (শাদ্দা) উচ্চারণ করা হয়নি!")
#     elif ref_has and user_has:
#         print("✅ শাদ্দা ঠিক আছে।")
#     else:
#         print("ℹ️ শাদ্দা লাগে না।")

#     # পার্থক্য দেখানো
#     matcher = SequenceMatcher(None, reference_text, user_text)
#     print("\n📌 পার্থক্য:")
#     for tag, i1, i2, j1, j2 in matcher.get_opcodes():
#         if tag != 'equal':
#             print(f"  [{tag.upper()}] '{reference_text[i1:i2]}' → '{user_text[j1:j2]}'")

#     return {
#         "user_text": user_text,
#         "similarity": similarity,
#         "shadda_correct": ref_has == user_has,
#         "details": {
#             "reference_has_shadda": ref_has,
#             "user_has_shadda": user_has
#         }
#     }

# # ========================================
# # 5. মূল প্রোগ্রাম
# # ========================================
# if __name__ == "__main__":
#     # 🔧 আপনার ডেটা এখানে দিন
#     AUDIO_FILE = "./1. Surah Al-Fatihah 1st verse.mp3"  # আপনার অডিও ফাইল
#     CORRECT_AYAH = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"  # সঠিক আয়াত (শাদ্দা সহ)

#     print("🎯 উচ্চারণ ও তাসদীদ চেক শুরু হচ্ছে...\n")
    
#     result = check_pronunciation_and_tasdid(AUDIO_FILE, CORRECT_AYAH, processor, model)

#     print("\n✅ চেক সম্পন্ন!")
#     print(f"সামগ্রিক মিল: {result['similarity']}%")
#     if result['shadda_correct']:
#         print("🎉 শাদ্দা ঠিক আছে।")
#     else:
#         print("🔴 শাদ্দা ভুল হয়েছে।")








































#  pip install torch torchaudio transformers librosa fuzzywuzzy python-Levenshtein



# -*- coding: utf-8 -*-
"""
Quran Recitation: Pronunciation & Shadda (Tasdid) Checker
--------------------------------------------------------
This script:
- Transcribes Arabic speech from audio using a fine-tuned Wav2Vec2 model
- Checks if Shadda (ـّ) is present in both reference and transcription
- Compares similarity using fuzzy matching
- Highlights differences
- Works reliably with torchaudio (no experimental libraries)
"""

import torch
import torchaudio
from transformers import AutoProcessor, Wav2Vec2ForCTC
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher
import warnings

# Suppress torchaudio deprecation warning (safe for now)
warnings.filterwarnings("ignore", category=UserWarning, module="torchaudio")

# ========================================
# 1. Load Arabic-Optimized Model
# ========================================
print("🔄 Loading Arabic-optimized model...")
try:
    processor = AutoProcessor.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-arabic")
    model = Wav2Vec2ForCTC.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-arabic")
    print("✅ Model loaded Successfully!")
except Exception as e:
    print("❌ Failed to load model:", str(e))
    print("💡 Check internet, use a VPN, or download model manually.")
    exit(1)

# ========================================
# 2. Shadda (Tasdid) Detection
# ========================================
def has_shadda(text):
    """Check if the text contains Shadda (ـّ)"""
    SHADDA = '\u0651'  # Unicode for ـّ
    return SHADDA in text

# ========================================
# 3. Audio to Text (Using torchaudio - Stable & Reliable)
# ========================================
def audio_to_text(audio_path, processor, model):
    """
    Load audio and transcribe using Wav2Vec2
    :param audio_path: Path to audio file (.mp3, .wav)
    :return: Transcribed Arabic text
    """
    try:
        speech, rate = torchaudio.load(audio_path)
    except Exception as e:
        print("❌ Failed to load audio file:", str(e))
        exit(1)

    # Resample to 16kHz (required by Wav2Vec2)
    if rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=rate, new_freq=16000)
        speech = resampler(speech)
    speech = speech.squeeze().numpy()  # Convert to 1D array

    # Process input
    inputs = processor(speech, sampling_rate=16000, return_tensors="pt", padding=True)

    # Inference
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    return transcription.strip()

# ========================================
# 4. Evaluate Pronunciation & Shadda
# ========================================
def check_pronunciation_and_tasdid(user_audio, reference_text, processor, model):
    """
    Full evaluation of user's recitation
    """
    print("🔊 Transcribing user audio...")
    user_text = audio_to_text(user_audio, processor, model)
    print(f"🗣️ User said: {user_text}")
    print(f"📖 Reference: {reference_text}")

    # Similarity score
    similarity = fuzz.ratio(user_text, reference_text) # i will use partial_ratio
    print(f"\n📊 Similarity Score: {similarity}%")

    # Shadda check
    ref_has = has_shadda(reference_text)
    user_has = has_shadda(user_text)

    print(f"\n🔍 Shadda (Tasdid) Check:")
    print(f"  Reference has Shadda: {ref_has}")
    print(f"  User transcription has Shadda: {user_has}")

    if ref_has and not user_has:
        print("❌ ⚠️ Warning: Shadda is missing! It should be pronounced.")
    elif ref_has and user_has:
        print("✅ Shadda is correctly present.")
    else:
        print("ℹ️ No Shadda required.")

    # Highlight differences
    matcher = SequenceMatcher(None, reference_text, user_text)
    print("\n📌 Differences:")
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':
            print(f"  [{tag.upper()}] '{reference_text[i1:i2]}' → '{user_text[j1:j2]}'")

    return {
        "user_text": user_text,
        "similarity": similarity,
        "shadda_correct": ref_has == user_has,
        "details": {
            "reference_has_shadda": ref_has,
            "user_has_shadda": user_has
        }
    }

# ========================================
# 5. Main Execution
# ========================================
if __name__ == "__main__":
    # 🔧 Configure your inputs
    AUDIO_FILE = "./1.mp3"
    CORRECT_AYAH ="بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِیمِ" # teacher's pronunciation
    print("🎯 Starting pronunciation and Tasdid check...\n")
    
    result = check_pronunciation_and_tasdid(AUDIO_FILE, CORRECT_AYAH, processor, model)

    print("\n✅ Evaluation Complete!")
    print(f"Overall Similarity: {result['similarity']}%")
    if result['shadda_correct']:
        print("🎉 Shadda is correctly used.")
    else:
        print("🔴 Shadda is missing or incorrectly applied.")