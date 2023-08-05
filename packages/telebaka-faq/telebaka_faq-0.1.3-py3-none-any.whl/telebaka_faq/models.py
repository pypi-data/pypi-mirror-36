from django.db import models

from bots.models import TelegramBot


class FAQSection(models.Model):
    hidden = models.BooleanField(default=False)
    command = models.CharField(max_length=64, unique=True, db_index=True)
    title = models.CharField(max_length=128, unique=True, db_index=True)
    text = models.TextField(max_length=4096)
    bot = models.ForeignKey(TelegramBot, on_delete=models.SET_NULL, null=True,
                            limit_choices_to={'plugin_name': 'telebaka_faq'})

    def __str__(self):
        return self.title




