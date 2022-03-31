from sqlite3 import DatabaseError
from django.db import models
from django.utils import timezone


class DeactivateQuerySet(models.query.QuerySet):
    """Overrides batch delete"""
    def delete(self):
        return super(DeactivateQuerySet, self).update(active=False, deleted_at=timezone.now())

    def hard_delete(self):
        return super(DeactivateQuerySet, self).delete()

    def active(self):
        return self.filter(active=True)


class NoDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.active_only = kwargs.pop('active_only', True)
        super(NoDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.active_only:
            return DeactivateQuerySet(self.model).active()    
        
        return DeactivateQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

    def delete(self):
        return self.get_queryset().delete()


class NoDeleteModel(models.Model):
    active = models.BooleanField(default=True, editable=False, db_index=True)
    deleted_at = models.DateTimeField(default=None, editable=False, null=True)

    objects = NoDeleteManager()
    all_objects = NoDeleteManager(active_only=False)

    class Meta:
        abstract = True

    """Overrides single delete"""
    def delete(self):
        self.deleted_at = timezone.now()
        self.active = False
        self.save()

    def hard_delete(self):
        super(NoDeleteModel, self).delete()

