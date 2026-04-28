from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.code