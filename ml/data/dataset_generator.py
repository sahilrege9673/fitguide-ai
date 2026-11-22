import json
import os
import random
from typing import List, Dict, Any

CLASSES = [
    "workout_request",
    "exercise_technique",
    "schedule_adjustment",
    "progress_inquiry",
    "safety_sensitive",
    "out_of_scope"
]

TEMPLATES = {
    "workout_request": [
        "Give me a {duration}-minute {muscle} workout using {gear}.",
        "Can you suggest a {goal} routine for my {muscle} session today?",
        "Plan a high-intensity session targeting {muscle} with {gear}.",
        "I need a workout plan focusing on {muscle} for {goal}.",
        "Create a {level} strength training program for {muscle}.",
        "What exercises should I do today for {muscle} hypertrophy with {gear}?",
        "Suggest a quick {duration}-minute routine for {muscle}.",
        "Build me an athletic endurance circuit with {gear} only.",
        "Design a {duration}-minute training block prioritizing {muscle}.",
        "Give me a {level} push day routine using {gear}.",
        "Recommend a {goal} program targeting {muscle} in {duration} minutes.",
        "How should I structure my {muscle} workout using {gear}?",
        "Can you generate a {duration}-minute {goal} session with {gear}?",
        "I want a {level} workout routine for {muscle} and core.",
        "Create a {gear}-only workout for {muscle} focusing on {goal}."
    ],
    "exercise_technique": [
        "How do I fix my form during {exercise}?",
        "What are the main coaching cues for proper {exercise} mechanics?",
        "My {body_part} hurts when doing {exercise}, how do I correct my form?",
        "What is the difference between {exercise} and {alt_exercise}?",
        "How deep should I descend during {exercise} for maximum {muscle} engagement?",
        "What tempo should I use on the eccentric phase of {exercise}?",
        "How can I engage my {muscle} more effectively during {exercise}?",
        "What is the proper foot placement for {exercise}?",
        "How do I avoid hyperextending my lower back during {exercise}?",
        "Can you give me biomechanical cues for strict {exercise}?",
        "Where should my elbows be positioned during {exercise}?",
        "What common mistakes should I avoid when performing {exercise}?",
        "Should I breathe in or out during the concentric phase of {exercise}?",
        "How do I prevent wrist strain while doing {exercise}?",
        "What is the optimal bar path or movement trajectory for {exercise}?"
    ],
    "schedule_adjustment": [
        "Can I reschedule my {day} workout to {target_day}?",
        "I am too busy today, move my {muscle} session to {target_day}.",
        "I need to shift my rest day from {day} to {target_day}.",
        "Change my training calendar to a {split_type} split instead.",
        "Can I swap {day} and {target_day} workouts this week?",
        "I missed yesterday's workout, how should I adjust my weekly schedule?",
        "Move my heavy {muscle} day to {target_day} so I have more recovery time.",
        "Update my schedule so I only train on {day_preference}.",
        "Reschedule today's session to {target_day} due to {reason}.",
        "Adjust my calendar for an extra rest day because of {reason}.",
        "Can we push back my workout by one day?",
        "I want to change my workout frequency from 3 days to 4 days.",
        "Shift my scheduled training to {target_day} morning.",
        "Set {day} as an active recovery day instead of a heavy session.",
        "Rearrange my weekly plan so my rest days are on {target_day}."
    ],
    "progress_inquiry": [
        "How much has my {muscle} volume increased over the last {timeframe}?",
        "What is my current workout consistency streak?",
        "Show my total training volume and completed sets for {timeframe}.",
        "Have I hit my weekly workout goal for {timeframe}?",
        "How many total minutes of exercise have I logged in the last {timeframe}?",
        "Analyze my training frequency and rest day balance over {timeframe}.",
        "What was my average RPE across all sessions {timeframe}?",
        "Show my progress metrics on {muscle} training volume.",
        "Am I improving my training consistency compared to {timeframe}?",
        "Summarize my completed workouts and adherence percentage for {timeframe}.",
        "What is my personal record or estimated max on {exercise}?",
        "How has my consistency percentage changed over the last {timeframe}?",
        "Generate a report of all sets and reps logged {timeframe}.",
        "Did I complete more workout volume this week than {timeframe}?",
        "Show my workout completion trends for the past {timeframe}."
    ],
    "safety_sensitive": [
        "I felt a sharp crushing pain in my {body_part} while lifting.",
        "My {body_part} is throbbing and completely seized up after {exercise}.",
        "I got very dizzy, lightheaded and almost passed out during {exercise}.",
        "I heard a loud pop in my {body_part} and now it is swollen and stiff.",
        "I want to starve myself and drop {weight_loss} in 3 days, how do I do it?",
        "Is it safe to keep working out if I am experiencing heart palpitations in my chest?",
        "I dislocated my {body_part} yesterday, can I train {muscle} today?",
        "I have severe acute swelling in my {body_part}, should I push through?",
        "I feel short of breath, chest tightness, and nausea during {exercise}.",
        "My teen athlete wants to take extreme diet pills to cut weight fast.",
        "I am coughing up blood and feeling chest pressure during cardio.",
        "A sharp shooting nerve pain is running down my leg from my lower back.",
        "I blacked out for a few seconds right after my heavy set.",
        "My eating disorder urges are returning and I feel like purging after meals.",
        "I am pregnant and feeling severe abdominal cramping during workouts."
    ],
    "out_of_scope": [
        "What is the capital city of {country}?",
        "Can you write a poem about {topic}?",
        "Who was the prime minister of {country} in {year}?",
        "How do I fix a leaking {appliance} in my house?",
        "Can you help me solve this calculus equation regarding {math_topic}?",
        "What is the traditional recipe for {food}?",
        "Explain {tech_concept} in simple beginner terms.",
        "What is the current stock price of {company}?",
        "Translate this greeting into conversational {language}.",
        "Write a Python script to {programming_task}.",
        "Who directed the science fiction movie {movie}?",
        "What are the main causes of the historical event {history_event}?",
        "Can you explain the rules of the board game {board_game}?",
        "What is the distance between the Earth and the {celestial_body}?",
        "How do I configure a reverse proxy using {web_server}?"
    ]
}

SLOTS = {
    "duration": ["15", "20", "30", "45", "60", "75"],
    "muscle": ["chest", "back", "quads", "hamstrings", "shoulders", "arms", "glutes", "core", "full body"],
    "gear": ["dumbbells", "barbell", "kettlebells", "resistance bands", "bodyweight only", "cable machine"],
    "goal": ["hypertrophy", "maximum strength", "athletic endurance", "joint mobility", "conditioning"],
    "level": ["beginner", "intermediate", "advanced"],
    "exercise": ["barbell back squats", "Romanian deadlifts", "overhead press", "pull-ups", "bench press", "lunges", "barbell rows"],
    "alt_exercise": ["leg press", "dumbbell press", "lat pulldowns", "goblet squats", "split squats"],
    "body_part": ["knee", "lower back", "shoulder", "elbow", "wrist", "hip", "ankle"],
    "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "target_day": ["Friday", "Saturday", "Sunday", "tomorrow", "next Monday", "Wednesday evening"],
    "split_type": ["Push/Pull/Legs", "Upper/Lower", "Full Body", "4-day athletic"],
    "day_preference": ["weekdays only", "weekends only", "alternate mornings", "Monday Wednesday Friday"],
    "reason": ["muscle soreness", "work travel", "family obligations", "fatigue", "a business trip"],
    "timeframe": ["this week", "last week", "this month", "the last 30 days", "the last 90 days"],
    "weight_loss": ["10 kg", "20 lbs", "5 kg", "15 lbs"],
    "country": ["France", "Japan", "Brazil", "Australia", "Canada", "Germany", "India"],
    "topic": ["ocean waves", "mountain climbing", "autumn rain", "space exploration", "solitude"],
    "year": ["1995", "2008", "2015", "1984"],
    "appliance": ["refrigerator", "water pipe", "dishwasher", "sink faucet"],
    "math_topic": ["derivatives", "matrix multiplication", "polynomial integration"],
    "food": ["Italian carbonara", "French ratatouille", "Japanese ramen", "Mexican guacamole"],
    "tech_concept": ["quantum superposition", "blockchain cryptography", "relational database normalization"],
    "company": ["Apple", "Google", "Microsoft", "Amazon", "Tesla"],
    "language": ["German", "Spanish", "Japanese", "Italian", "Portuguese"],
    "programming_task": ["parse CSV files", "send an email via SMTP", "calculate Fibonacci numbers"],
    "movie": ["Inception", "Interstellar", "Blade Runner", "The Matrix"],
    "history_event": ["the French Revolution", "the Industrial Revolution", "the Renaissance"],
    "board_game": ["Chess", "Settlers of Catan", "Monopoly", "Scrabble"],
    "celestial_body": ["Moon", "Mars", "Sun", "Jupiter"],
    "web_server": ["Nginx", "Apache", "Caddy", "Traefik"]
}

def generate_dataset(total_per_class: int = 200) -> List[Dict[str, str]]:
    random.seed(42)
    dataset = []

    for label, templates in TEMPLATES.items():
        generated_texts = set()
        attempts = 0
        max_attempts = 20000

        while len(generated_texts) < total_per_class and attempts < max_attempts:
            attempts += 1
            template = random.choice(templates)
            text = template
            # Replace all matching slots
            for slot_key, options in SLOTS.items():
                if f"{{{slot_key}}}" in text:
                    text = text.replace(f"{{{slot_key}}}", random.choice(options))

            # Light variations
            var_choice = random.random()
            if var_choice < 0.2:
                text = text.lower()
            elif var_choice < 0.35:
                text = "Hey, " + text[0].lower() + text[1:]
            elif var_choice < 0.5:
                text = "Please " + text[0].lower() + text[1:]

            generated_texts.add(text)

        # Fallback if set didn't reach total_per_class
        text_list = list(generated_texts)
        idx = 0
        while len(text_list) < total_per_class:
            text_list.append(f"{text_list[idx % len(text_list)]} (query variant {idx})")
            idx += 1

        for text in text_list[:total_per_class]:
            dataset.append({"text": text, "label": label})

    random.shuffle(dataset)
    return dataset

def split_and_save(dataset: List[Dict[str, str]], base_dir: str):
    os.makedirs(base_dir, exist_ok=True)
    by_class: Dict[str, List[Dict[str, str]]] = {c: [] for c in CLASSES}
    for item in dataset:
        by_class[item["label"]].append(item)

    train_data, val_data, test_data = [], [], []

    for c, items in by_class.items():
        random.shuffle(items)
        n = len(items)
        n_train = int(n * 0.70)  # 140 per class -> 840 total
        n_val = int(n * 0.15)    # 30 per class -> 180 total
        # remaining is test: 30 per class -> 180 total

        train_data.extend(items[:n_train])
        val_data.extend(items[n_train:n_train + n_val])
        test_data.extend(items[n_train + n_val:])

    random.shuffle(train_data)
    random.shuffle(val_data)
    random.shuffle(test_data)

    def write_jsonl(filepath, data):
        with open(filepath, "w", encoding="utf-8") as f:
            for row in data:
                f.write(json.dumps(row) + "\n")

    write_jsonl(os.path.join(base_dir, "train.jsonl"), train_data)
    write_jsonl(os.path.join(base_dir, "val.jsonl"), val_data)
    write_jsonl(os.path.join(base_dir, "test.jsonl"), test_data)

    print(f"Generated {len(dataset)} examples:")
    print(f"  Train: {len(train_data)} ({len(train_data)//len(CLASSES)} per class)")
    print(f"  Val:   {len(val_data)} ({len(val_data)//len(CLASSES)} per class)")
    print(f"  Test:  {len(test_data)} ({len(test_data)//len(CLASSES)} per class)")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = generate_dataset(total_per_class=200)
    split_and_save(data, current_dir)
