from django.contrib import admin

from .models import (
    Text,
    Token,
    Dictionary,
)

admin.site.register(Text)
admin.site.register(Token)
admin.site.register(Dictionary)

