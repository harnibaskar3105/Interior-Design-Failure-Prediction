from django.contrib import admin
from .models import Prediction, UserProfile
from .models import Feedback

admin.site.register(Feedback)

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "room_type",
        "material_type",
        "lighting",
        "predicted_failure",
        "predicted_at",
        "recommendations_preview",   # ✅ valid
    )

    list_filter = ("predicted_failure", "room_type", "material_type")
    search_fields = ("user__username",)

    def recommendations_preview(self, obj):
        """
        Safe admin preview.
        Works ONLY if recommendations are stored in DB.
        """
        if hasattr(obj, "recommendations") and obj.recommendations:
            return obj.recommendations[:50] + "..."
        return "—"

    recommendations_preview.short_description = "Recommendations"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "home_type",
        "total_predictions",
        "successes",
        "failures",
    )

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "message")
