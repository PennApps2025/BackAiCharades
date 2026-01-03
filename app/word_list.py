# app/word_list.py

# app/word_list.py

WORD_DICT = {
    # Everyday actions — easy to act out without props, large and clear movements
    "Everyday actions": [
        "waving",        # waving hand left/right
        "clapping",      # clapping hands
        "pointing",      # pointing with finger
        "shrugging",     # shrugging shoulders
        "sitting down",  # motion of sitting
        "stretching",    # stretching arms/body
        "yawning",       # yawning (open mouth, cover with hand)
        "kicking",        # kicking motion
        "punching",
        "thumbs up",
        "thumbs down",
        "peace sign",
        "salute",
        "hands on hips",
        "covering mouth",
        "swimming"
    ],

    # Emotions — mainly facial expressions, easy for VLM to classify
    "Emotions": [
        "happy",
        "sad",
        "surprised",
        "scared",
        "excited",
        "bored",
        "confused",
        "nervous"
    ],

    # Occupations — chosen so they can be acted out with gestures only
    "Occupations": [
        "ballet dancer",    # dancing motion
        "teacher",   # pointing/explaining gesture
        "doctor",    # checking pulse or listening motion
        "pianist",  # playing piano
        "guitarist", # playing guitar
        "photographer",
        "soldier",  # 오타 수정: solider → soldier
        "waiter/waitress",
        "boxer",
        "swimmer",
    ]
}
