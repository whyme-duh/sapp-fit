from website.models import Testimonial
from faker import Faker

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Automate the creation of model objects'

    review = [
        "Loved it! Would love to go more.",
        "The service was mid, Could have been better",
        "Like the vibes of the group class.",
        "Sappfit being great as usual",
        "Always loved to get trained by Sappfit",
        "What a service she provides, highly recommended.",
        "Would love to work with her more!"
    ]

    def handle(self, *awrgs, **kwargs):
        self.stdout.write("Starting automation...")

        fake = Faker()
        for i in range(len(self.review)):
            Testimonial.objects.create(
                testimonial = self.review[i],
                user_name = fake.name()

            )
        self.stdout.write(self.style.SUCCESS("Successfully created objects!"))