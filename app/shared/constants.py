from typing import Literal


MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 255
MAX_PHONE_LENGTH = 20
MAX_PASSWORD_HASH_LENGTH = 255
MAX_GOAL_LENGTH = 100
MAX_ACTIVITY_LEVEL_LENGTH = 50
MAX_EXPERIENCE_LEVEL_LENGTH = 50
MAX_DIET_PREFERENCE_LENGTH = 50
MAX_WORKOUT_LOCATION_LENGTH = 50
MAX_WORKOUT_SPLIT_LENGTH = 100
MAX_GENDER_LENGTH = 20

Gender = Literal[
    "Male",
    "Female",
    "Other",
    "Prefer not to say",
]

ActivityLevel = Literal[
    "Sedentary",
    "Lightly Active",
    "Moderately Active",
    "Very Active",
    "Extremely Active",
]

ExperienceLevel = Literal[
    "Beginner",
    "Intermediate",
    "Advanced",
]

WorkoutLocation = Literal[
    "Home",
    "Gym",
    "Hybrid",
]

FitnessGoal = Literal[
    "Weight Loss",
    "Muscle Gain",
    "Strength",
    "Endurance",
    "General Fitness",
    "Athletic Performance",
]

DietPreference = Literal[
    "Vegetarian",
    "Vegan",
    "Eggetarian",
    "Non-Vegetarian",
    "Pescatarian",
]