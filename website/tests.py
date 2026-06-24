from django.test import TestCase
from . form import CustomServiceForm


class FormTest(TestCase):
    def test_custom_service_form_valid_or_not(self):
        form = CustomServiceForm(
            data = {"name" : "Ritik",
                "age" : 25, 
                "weight" : 55, 
                "phone_number": 9860930990,
                "goal_choices" : "Fat Loss & Toning",
                "preferred_duration" : "1 Week Plan",
                "workout_time" : "45 minutes",
                "gender" : "Male",
                "email" : "riitk@gmail.comd",
                "equipment_used": "nm.a",
                "special_notes" : "adf",
                "activity_level" : "Sedentary"
                }
            )
        self.assertTrue(form.is_valid())
        print("✅ Passed! When the custom service form is provded with correct values, is_valid returns True")

    def test_custom_service_form_error(self):
        form = CustomServiceForm(
            data = {"name" : "Ritik",
                "age" : 1, 
                "weight" : 1, 
                "phone_number": 9860930990,
                "goal_choices" : "Fat Loss & Toning",
                "preferred_duration" : "1 Week Plan",
                "workout_time" : "45 minutes",
                "gender" : "Male",
                "email" : "riitk@gmail.comd",
                "equipment_used": "nm.a",
                "special_notes" : "adf",
                "activity_level" : "Sedentary"
                }
            )
        self.assertEqual(form.errors["age"], ["I can only provide services to people aged 10 to 60."])
        self.assertEqual(form.errors["weight"], ["Please enter a valid weight in kg."])
        print("✅ Passed! When the custom service form is provded with incorrect values, it returns form.errors text")


    # this function is to check whether the system can identify whether the request is for human or for AI
    def test_custom_service_form_action_type(self):
        form = CustomServiceForm(
            data = {
                "name" : "Ritik",
                "age" : 20, 
                "weight" : 55, 
                "gender" : "Male",
                "goal_choices" : "Fat Loss & Toning",
                "preferred_duration" : "1 Week Plan",
                "workout_time" : "45 minutes",
                "equipment_used": "nm.a",
                "special_notes" : "adf",
                "activity_level" : "Sedentary"
                },
            action_type = "ai_preview"
            )
        
        self.assertTrue(form.is_valid())
        print("✅ Passed! When the user clciks 'AI Preview' the form should not validate phone and other user detail")
