from flask import Flask, render_template, request
import joblib
import pandas as pd
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',   # or your SMTP server
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email@gmail.com',
    MAIL_PASSWORD='your_email_password',  # use App Password for Gmail
)
mail = Mail(app)

app = Flask(
    __name__,
    template_folder="inte_des/templates",
    static_folder="inte_des/static"
)

# -------------------------------
# Load trained pipeline model
# -------------------------------
model = joblib.load("interior_pipeline.pkl")

# -------------------------------
# Rule-based override function
# -------------------------------
def logical_override(budget, room, material, lighting):
    """
    Ensure extreme cases are HIGH RISK.
    Example: very low budget + premium material → HIGH RISK
    """
    if budget < 200000 and material == "Marble":
        return 1, 90  # force HIGH RISK with 90% probability
    if budget < 150000 and room == "large":
        return 1, 85
    if budget < 150000 and lighting == "high":
        return 1, 80
    return None, None

# -------------------------------
# Flask Routes
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # -------------------------------
        # Get user inputs
        # -------------------------------
        try:
            budget = float(request.form["budget"])
            room_size = request.form["room_size"]
            material = request.form["material"]
            lighting = request.form["lighting"]
        except:
            return render_template("predict.html", result="⚠ Invalid input!")

        # -------------------------------
        # Rule-based override
        # -------------------------------
        override_prediction, override_prob = logical_override(budget, room_size, material, lighting)
        if override_prediction is not None:
            prediction = override_prediction
            probability = override_prob
        else:
            # -------------------------------
            # Convert to DataFrame for pipeline
            # -------------------------------
            input_data = pd.DataFrame({
                "budget": [budget],
                "room_size": [room_size],
                "material": [material],
                "lighting": [lighting]
            })

            # -------------------------------
            # Predict using ML model
            # -------------------------------
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1] * 100

        # -------------------------------
        # Determine result string
        # -------------------------------
        if prediction == 1:
            result_text = "✅ HIGH RISK: Interior Design May Fail"
            risk_class = "result-high"
        else:
            result_text = "✅ LOW RISK: Interior Design Looks Safe"
            risk_class = "result-low"

        # -------------------------------
        # Recommendations
        # -------------------------------
        recommendations = []

        if budget < 200000:
            recommendations.append("Increase budget for better quality materials.")
        elif budget > 800000:
            recommendations.append("Consider optimizing costs without compromising quality.")

        if room_size == "small":
            recommendations.append("Use compact furniture and maximize vertical storage.")
        elif room_size == "medium":
            recommendations.append("Ensure furniture layout allows free movement.")
        else:  # large
            recommendations.append("Add partitions or furniture zones for better functionality.")

        if lighting == "low":
            recommendations.append("Improve lighting using LEDs and natural light.")
        elif lighting == "medium":
            recommendations.append("Add task lighting for work/study areas.")
        else:
            recommendations.append("Use diffused lighting to avoid glare.")

        if material == "Wood":
            recommendations.append("Avoid wood in humid areas; consider PVC or marble.")
        elif material == "PVC":
            recommendations.append("PVC is durable but ensure proper finishing.")
        else:
            recommendations.append("Marble is premium; maintain regularly to prevent stains.")

        # -------------------------------
        # Render result page
        # -------------------------------
        return render_template(
            "result.html",
            result=result_text,
            probability=round(probability, 2),
            recommendations=recommendations,
            risk_class=risk_class
        )

    # -------------------------------
    # GET request → show form
    # -------------------------------
    return render_template("predict.html")


if __name__ == "__main__":
    app.run(debug=True)
