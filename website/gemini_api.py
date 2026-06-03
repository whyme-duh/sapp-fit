from sapfit import settings


def gemini_response(duration, age, gender, weight, goal, equipment, notes, workout_time, activity_level):
    from google import genai

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents =f"""
            You are Saprina, an elite, highly sought-after personal trainer. 
            Your task is to design a highly effective, customized {workout_time}-minute workout plan for a client for {duration} weeks.

            CLIENT PROFILE:
            - Age: {age}
            - Gender: {gender}
            - Weight: {weight} kg
            - Primary Goal: {goal}
            - Available Equipment: {equipment}
            - Special Notes/Injuries: {notes}
            - Activity Level: {activity_level}

            CRITICAL INSTRUCTIONS:
            1. You must respond ONLY with a valid JSON object. Do not include markdown formatting like ```json, do not include introductory text, and do not include concluding text. Just the raw JSON object.
            2. The workout must safely accommodate any listed injuries or special notes.
            3. Keep the tone in the "pro_tips" encouraging, empowering, and professional.

            Ensure your JSON strictly follows this exact structure:
            {{
            "workout_title": "A catchy, motivating title for the routine",
            "estimated_duration_minutes": {duration},
            "warmup": [
                {{"exercise": "Name", "duration": "e.g., 60 seconds", "instructions": "Brief how-to"}}
            ],
            "main_workout": [
                {{
                "exercise": "Name",
                "sets": "Number of sets",
                "reps": "Number of reps or time",
                "rest": "Rest between sets (e.g., 60 seconds)",
                "instructions": "Brief form cue"
                }}
            ],
            "cooldown": [
                {{"exercise": "Name", "duration": "e.g., 60 seconds", "instructions": "Brief how-to"}}
            ],
            "pro_tips": [
                "Tip 1 from Saprina regarding form or nutrition",
                "Tip 2 regarding hydration or recovery"
            ]

            Furthermore, add a notice on the importance of consulting with a healthcare provider before starting any new workout routine, especially if they have pre-existing conditions or injuries.
            }}
            """
        )
    return response.text
