import factory
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f"user{n}@test.dev")
    name = factory.Faker("name")
    is_active = True
    is_email_verified = True  # helpful default for protected routes

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        pwd = extracted or "Passw0rd!"
        self.set_password(pwd)
        if create:
            self.save()