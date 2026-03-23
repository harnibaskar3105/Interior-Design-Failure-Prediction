from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .models import UserProfile, Prediction
import joblib
import numpy as np
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Feedback
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# -----------------------------
# Load ML model + encoders
# -----------------------------
MODEL_PATH = os.path.join(settings.BASE_DIR, "inte_des", "interior_model.pkl")
ROOM_ENCODER_PATH = os.path.join(settings.BASE_DIR, "inte_des", "room_encoder.pkl")
MATERIAL_ENCODER_PATH = os.path.join(settings.BASE_DIR, "inte_des", "material_encoder.pkl")
LIGHT_ENCODER_PATH = os.path.join(settings.BASE_DIR, "inte_des", "light_encoder.pkl")

model = joblib.load(MODEL_PATH)
room_encoder = joblib.load(ROOM_ENCODER_PATH)
material_encoder = joblib.load(MATERIAL_ENCODER_PATH)
light_encoder = joblib.load(LIGHT_ENCODER_PATH)


# ============================
# Home Page
# ============================
def home(request):
    return render(request, "home.html")


# ============================
# Login
# ============================
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request,
                "Invalid Username or Password",
                extra_tags="login_page"
            )
            return redirect("login_view")

    return render(request, "login_view.html")




# ============================
# Register
# ============================
def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        home_type = request.POST.get("home_type")
        role = request.POST.get("role")

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        # Username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        # Email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        # 🔥 Password strength validation
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        UserProfile.objects.create(user=user, role=role, home_type=home_type)

        messages.success(
            request,
            "Registration successful! Please login.",
            extra_tags="login_page"
        )

        return redirect("login_view")

    return render(request, "register.html")



# ============================
# Dashboard
# ============================
@login_required
def dashboard(request):

    total_predictions = Prediction.objects.count()
    user_num = UserProfile.objects.count()
    failure_count = Prediction.objects.filter(predicted_failure=True).count()
    success_count = Prediction.objects.filter(predicted_failure=False).count()

    context = {
        'total_predictions': total_predictions,
        'user_num' : user_num,
        'success_count': success_count,
        'failure_count': failure_count,
    }

    return render(request, 'dashboard.html', context)


# ============================
# Predict View
# ============================
@login_required
def predict_view(request):
    if request.method == "POST":
        try:
            budget = int(request.POST.get("budget"))
            room_size = request.POST.get("room_size").lower()
            material = request.POST.get("material").lower()
            lighting = request.POST.get("lighting").lower()

            # -------------------------
            # Encode inputs
            # -------------------------
            room_encoded = room_encoder.transform([room_size])[0]
            material_encoded = material_encoder.transform([material])[0]
            light_encoded = light_encoder.transform([lighting])[0]

            input_data = np.array([[budget, room_encoded, material_encoded, light_encoded]])

            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1] * 100

            result = (
                "HIGH RISK: Interior Design May Fail"
                if prediction == 1
                else "LOW RISK: Interior Design Looks Safe"
            )

            # ==========================
            # Generate Recommendations FIRST
            # ==========================
            recommendations = []

            # Budget suggestions
            estimated_costs = {
                "small": {"wood": 40000, "pvc": 30000, "marble": 70000},
                "medium": {"wood": 60000, "pvc": 50000, "marble": 100000},
                "large": {"wood": 100000, "pvc": 80000, "marble": 150000}
            }

            lighting_costs = {"low": 2000, "medium": 5000, "high": 12000}

            expected_total = (
                estimated_costs.get(room_size, {}).get(material, 0)
                + lighting_costs.get(lighting, 0)
            )

            if budget < expected_total:
                percent_increase = round(
                    (expected_total - budget) / expected_total * 100, 1
                )
                recommendations.append(
                    f"<b>Budget:</b> Increase budget by ~{percent_increase}% (≈₹{expected_total - budget})"
                )
            elif budget >= expected_total * 1.5:
                recommendations.append(
                    "<b>Budget:</b> High budget, consider premium materials."
                )
            else:
                recommendations.append("Budget: Budget is sufficient.")

            # Furniture suggestions
            furniture_options = {
                "small": ["IKEA LACK Coffee Table", "Foldable Study Desk", "Compact Sofa Bed"],
                "medium": ["IKEA MALM Bed", "L-shaped Sofa", "Storage TV Unit"],
                "large": ["King-size Bed", "Modular Sofa Set", "Dining Table Set"]
            }

            recommendations.append(
                "<b>Furniture:</b> " + ", ".join(furniture_options.get(room_size, []))
            )

            # Material suggestions
            material_options = {
                "wood": ["Oak veneer cabinets", "Teak wood dining table", "Mahogany study desk"],
                "pvc": ["PVC kitchen cabinets", "PVC storage racks", "PVC wall panels"],
                "marble": ["Carrara marble countertop", "Marble coffee table", "Marble floor tiles"]
            }

            recommendations.append(
                "<b>Material:</b> " + ", ".join(material_options.get(material, []))
            )

            # Lighting suggestions
            lighting_options = {
                "low": ["Philips Hue LED Panels", "Warm-white Floor Lamp", "Wall-mounted sconces"],
                "medium": ["Ceiling LED lights with dimmer", "Task lamp", "Pendant lights"],
                "high": ["Diffused curtains", "Edison bulbs", "Overhead + floor lamps"]
            }

            recommendations.append(
                "<b>Lighting:</b> " + ", ".join(lighting_options.get(lighting, []))
            )

            # Convert list → string for database
            recommendations_text = "\n".join(recommendations)

            # ==========================
            # Save Prediction to Database
            # ==========================
            prediction_obj=Prediction.objects.create(
                user=request.user,
                room_type=room_size,
                material_type=material,
                lighting=lighting,
                predicted_failure=bool(prediction),
                probability=round(probability, 2),
                recommendations=recommendations_text
            )

            # ==========================
            # Update UserProfile stats
            # ==========================
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.total_predictions += 1

            if prediction == 1:
                profile.failures += 1
            else:
                profile.successes += 1

            profile.save()

            # ==========================
            # Store in session for result page
            # ==========================
            request.session["prediction_result"] = {
                "result": result,
                "probability": round(probability, 2),
                "recommendations": recommendations,
                "prediction_id": prediction_obj.id,
            }

            return redirect("result")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("predict")

    return render(request, "predict.html")



# ============================
# Profile
# ============================
@login_required
def profile(request):
    userprofile, _ = UserProfile.objects.get_or_create(user=request.user)
    predictions = Prediction.objects.filter(user=request.user)

    return render(request, "profile.html", {
        "userprofile": userprofile,
        "predictions": predictions
    })

@login_required
def edit(request):
    user = request.user
    userprofile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # --- Update User ---
        user.first_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')

        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()

        # --- Update Profile ---
        userprofile.role = request.POST.get('role')
        userprofile.home_type = request.POST.get('home_type')

        selected_avatar = request.POST.get("profile_pic")

        # If user clicked remove profile picture
        selected_avatar = request.POST.get("profile_pic")

# If user selected remove
        if selected_avatar == "remove":
            userprofile.profile_pic = "default.png"

# If user selected new avatar
        elif selected_avatar and selected_avatar != userprofile.profile_pic:
           userprofile.profile_pic = selected_avatar

# If nothing selected → do nothing (keep old avatar)

        userprofile.save()

        messages.success(request, "Profile updated successfully!")

        if password:
            update_session_auth_hash(request, user)

        return redirect('profile')

    # ✅ FILTER DEFAULT AVATAR HERE
    avatar_choices = [
        choice for choice in UserProfile.AVATAR_CHOICES
        if choice[0] != "default.png"
    ]

    return render(request, 'edit.html', {
        'user': user,
        'userprofile': userprofile,
        'avatar_choices': avatar_choices
    })

@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user

        messages.success(
            request,
            "Profile deleted successfully.",
            extra_tags="login_page"
        )

        logout(request)   # AFTER message
        user.delete()

        return redirect("login_view")


# ============================
# Logout
# ============================
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login_view')


# ============================
# About
# ============================
def about(request):
    return render(request, "about.html")


# ============================
# Password Reset Views
# ============================

class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"



@login_required
def history(request):
    predictions = (
        Prediction.objects
        .select_related("user")
        .filter(user_id=request.user.id)
        .order_by("-predicted_at")
    )

    return render(request, "history.html", {
        "predictions": predictions
    })



@login_required
def prediction_detail(request, pk):
    prediction = get_object_or_404(
        Prediction,
        pk=pk,
        user=request.user
    )

    result_text = (
        "HIGH RISK: Interior Design May Fail"
        if prediction.predicted_failure
        else "LOW RISK: Interior Design Looks Safe"
    )

    context = {
        "prediction": prediction,   # 👈 important
        "result": result_text,
        "from_history": True,
    }

    return render(request, "result.html", {
    "prediction": prediction,
    "result": result_text,
    "from_history": True,
})

@login_required
def result(request):
    data = request.session.get("prediction_result")

    if not data:
        messages.info(request, "Please make a prediction first.")
        return redirect("predict")

    prediction = get_object_or_404(
        Prediction,
        id=data["prediction_id"],
        user=request.user
    )

    context = {
        "result": data["result"],
        "probability": data.get("probability"),
        "recommendations": data.get("recommendations"),
        "prediction": prediction,      # 🔥 THIS FIXES BUTTON
        "from_history": False,
    }

    del request.session["prediction_result"]

    return render(request, "result.html", context)



@login_required
def feedback_view(request):
    if request.method == "POST":
        rating = request.POST.get("rating")
        message = request.POST.get("message")

        if not rating:
            messages.error(request, "Please select a star rating.")
            return redirect("feedback")

        rating = int(rating)

        feedback, created = Feedback.objects.get_or_create(
            user=request.user,
            defaults={
                "rating": rating,
                "message": message
            }
        )

        if not created:
            feedback.rating = rating
            feedback.message = message
            feedback.save()
            messages.success(request, "Feedback updated successfully!")
        else:
            messages.success(request, "Feedback submitted successfully!")

        return redirect("feedback")

    return render(request, "feedback.html", {"show_home": True})

@login_required
def download_prediction_pdf(request, prediction_id):
    prediction = get_object_or_404(
        Prediction,
        id=prediction_id,
        user=request.user   # 🔒 security fix
    )

    template = get_template("prediction_pdf.html")
    html = template.render({
    "prediction": prediction,
    "user": request.user,
    "STATIC_ROOT": settings.STATIC_ROOT,  # 👈 ADD HERE
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="prediction_{prediction.id}.pdf"'
    )

    pisa_status = pisa.CreatePDF(
        src=html,
        dest=response
    )

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response

def design(request):
    return render(request, 'design.html')


@login_required
def contact(request):

    profile = UserProfile.objects.get(user=request.user)

    context = {
        "name": profile.username,
        "role": profile.role,
    }

    return render(request, "contact.html", context)

