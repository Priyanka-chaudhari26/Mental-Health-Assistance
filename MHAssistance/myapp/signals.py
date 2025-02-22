from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assessment, Question, Option

@receiver(post_save, sender=Assessment)
def create_related_questions(sender, instance, created, **kwargs):
    if created:
        # Example: Create default questions after assessment is created
        # Create Questions
        question1 = Question.objects.create(assessment=instance, text="Default Question 1")
        question2 = Question.objects.create(assessment=instance, text="Default Question 2")
        
        # Create Options for Question 1
        Option.objects.create(question=question1, text="Option A1")
        Option.objects.create(question=question1, text="Option B1")
        
        # Create Options for Question 2
        Option.objects.create(question=question2, text="Option A2")
        Option.objects.create(question=question2, text="Option B2")
