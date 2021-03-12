from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext, ugettext_lazy as _
from projects.models import Epic, Initiative, Product


@receiver(post_save, sender=Product)
def product_creation_handler(sender, instance, created, **kwargs):
    if created:
        # créer un objet « Initiative » avec le même titre que l'objet « Product »
        obj, created = Initiative.objects.get_or_create(
            title=instance.title,
            description=_(
                "This initiative was created automatically to collect all the project epics not yet assigned to a specific initiative."
            ),
            owner=instance.owner,
            product=instance,
        )
    else:
        # modifier l'initiative par default
        previous_title = instance.history.latest().prev_record.title
        initiative = Initiative.objects.get(
            title=previous_title,
            product=instance,
        )
        initiative.title = instance.title
        initiative.save()


@receiver(post_save, sender=Initiative)
def initiative_creation_handler(sender, instance, created, **kwargs):
    if created:
        # créer un objet « Epic » avec le même titre que l'objet « Initiative »
        obj, created = Epic.objects.get_or_create(
            title=instance.title,
            description=_(
                "This epic was created automatically to collect all the initiative stories not yet assigned to a specific epic."
            ),
            owner=instance.owner,
            initiative=instance,
        )
    else:
        # modifier l'initiative par default
        previous_title = instance.history.latest().prev_record.title
        epic = Epic.objects.get(
            title=previous_title,
            initiative=instance,
        )
        epic.title = instance.title
        epic.save()
