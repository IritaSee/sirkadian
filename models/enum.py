import enum

#defining enums
class user_gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"

class user_lang(enum.Enum):
    ENG = "english"
    IDN = "indonesian"

class song_mood(enum.Enum):
    UPLIFTING = "uplifting"
    DEPRESSED = "depressed"
    RELAX = "relax"
    AMBIENT = "ambient"

class activity_level(enum.Enum):
    SEDENTARY = "sedentary"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class sport_difficulty(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class mood_state(enum.Enum):
    VLOW = "very low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VHIGH = "very high"

class food_type(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class FoodType(enum.Enum):
    POKOK = "pokok"
    LAUK = "lauk"
    SAYUR = "sayur"
    MINUM = "minum"
    SNACK = "snack"

class organ_system(enum.Enum):
    ALI = "alimentary"
    BHV = "behavior"
    CRV = "cardiovascular"
    END = "endocrine"
    HEA = "hearing"
    HEM = "hematologic"
    HEP = "hepatobiliary"
    IMN = "immune"
    MUS = "musculoskeletal"
    NEU = "neurologic"
    NUT = "nutrition"
    REP = "reproduction"
    RES = "respiratory"
    SKN = "skin"
    URI = "urinary"
    VIS = "visual"

# class food_prohibition(enum.Enum):
#     PROTEIN = "protein"
#     FAT = "fat"
#     CARBOHYDRATE = "carbohydrate"
#     FIBER = "fiber"
#     CALCIUM = "calcium"
#     PHOSPHOR = "phosphor"
#     IRON = "iron"
#     SODIUM = "sodium"
#     POTASSIUM = "potassium"
#     COPPER = "copper"
#     ZINC = "zinc"

# class sport_prohibition(enum.Enum):
#     DIFFICULTY = "difficulty"
#     DURATION = "duration"

# # Semua prohibition artinya high (protein = high protein, difficulty = high difficulty)

# end of defining enums