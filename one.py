#  pip install torch torchaudio transformers librosa fuzzywuzzy python-Levenshtein



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
# 4. Calculate Pronunciation & Shadda Score
# ========================================
def calculate_pronunciation_and_tasdid_score(user_text, reference_text):
    """
    Calculate detailed pronunciation and shadda (tasdid) score.
    :param user_text: Transcribed user text
    :param reference_text: Correct reference text
    :return: Dictionary with scores and mistake details
    """
    # 1. Overall similarity (0-100%)
    similarity = fuzz.ratio(user_text, reference_text)
    
    # 2. Partial ratio (better for partial matches)
    partial_similarity = fuzz.partial_ratio(user_text, reference_text)

    # 3. Shadda Check
    SHADDA = '\u0651'  # ـّ
    ref_has_shadda = [i for i, c in enumerate(reference_text) if c == SHADDA]
    user_has_shadda = [i for i, c in enumerate(user_text) if c == SHADDA]

    # Find shadda positions in reference (on the letter after shadda)
    shadda_letters_ref = []
    for i in ref_has_shadda:
        if i > 0:
            shadda_letters_ref.append(reference_text[i-1])  # Letter before shadda

    shadda_letters_user = []
    for i in user_has_shadda:
        if i > 0:
            shadda_letters_user.append(user_text[i-1])

    # Missing or extra shadda
    missing_shadda = set(shadda_letters_ref) - set(shadda_letters_user)
    extra_shadda = set(shadda_letters_user) - set(shadda_letters_ref)

    # 4. Detailed difference analysis
    matcher = SequenceMatcher(None, reference_text, user_text)
    mistakes = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":
            mistakes.append({
                "type": "Replace",
                "expected": reference_text[i1:i2],
                "got": user_text[j1:j2]
            })
        elif tag == "delete":
            mistakes.append({
                "type": "Missing",
                "expected": reference_text[i1:i2],
                "got": ""
            })
        elif tag == "insert":
            mistakes.append({
                "type": "Extra",
                "expected": "",
                "got": user_text[j1:j2]
            })

    # 5. Calculate weighted score
    base_score = partial_similarity
    shadda_penalty = 10  # Penalty per shadda mistake (can be tuned)

    shadda_mistake_count = len(missing_shadda) + len(extra_shadda)
    final_score = max(0, base_score - (shadda_penalty * shadda_mistake_count))

    return {
        "pronunciation": {
            "similarity_score": similarity,
            "partial_similarity": partial_similarity,
            "mistake_count": len(mistakes),
            "mistakes": mistakes
        },
        "tasdid": {
            "reference_has_shadda_letters": list(shadda_letters_ref),
            "user_has_shadda_letters": list(shadda_letters_user),
            "missing_shadda_on": list(missing_shadda),
            "extra_shadda_on": list(extra_shadda),
            "shadda_mistake_count": shadda_mistake_count
        },
        "final_score": round(final_score, 2),
        "feedback": {
            "overall": "Excellent!" if final_score > 85 else "Good" if final_score > 70 else "Needs Improvement" if final_score > 50 else "Poor"
        }
    }


#  highlight_differences
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


# ========================================
# 5. Main Execution
# ========================================
if __name__ == "__main__":
    AUDIO_FILE = "./1.mp3"
    CORRECT_AYAH = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِیمِ"
    
    print("🎯 Starting pronunciation and Tasdid check...\n")
    
    # Get transcription
    user_text = audio_to_text(AUDIO_FILE, processor, model)
    print(f"🗣️ User said: {user_text}")
    print(f"📖 Reference: {CORRECT_AYAH}")

    # Get detailed score
    score_result = calculate_pronunciation_and_tasdid_score(user_text, CORRECT_AYAH)

    print("\n" + "="*50)
    print("📊 DETAILED EVALUATION REPORT")
    print("="*50)
    print(f"🗣️  User Text: {user_text}")
    print(f"📖 Reference: {CORRECT_AYAH}")
    print(f"📈 Similarity Score: {score_result['pronunciation']['similarity_score']}%")
    print(f"🔍 Partial Match: {score_result['pronunciation']['partial_similarity']}%")

    print(f"\n❌ Pronunciation Mistakes: {score_result['pronunciation']['mistake_count']}")
    for m in score_result['pronunciation']['mistakes']:
        if m['expected']:
            print(f"   ➡️ Replace '{m['expected']}' with '{m['got']}'")
        else:
            print(f"   ➡️ Extra: '{m['got']}'")

    print(f"\n💥 Tasdid (Shadda) Errors: {score_result['tasdid']['shadda_mistake_count']}")
    if score_result['tasdid']['missing_shadda_on']:
        print(f"   🔺 Missing Shadda on: {', '.join(score_result['tasdid']['missing_shadda_on'])}")
    if score_result['tasdid']['extra_shadda_on']:
        print(f"   🔻 Extra Shadda on: {', '.join(score_result['tasdid']['extra_shadda_on'])}")

    # ========================================
    print("\nDifferences highlighted:")
    print(highlight_differences(user_text, CORRECT_AYAH))

    print(f"\n⭐ Final Score: {score_result['final_score']}/100")
    print(f"📌 Feedback: {score_result['feedback']['overall']}")
    print("="*50)