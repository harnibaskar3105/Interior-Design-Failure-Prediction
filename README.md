Overview

The Interior Design Failure Prediction System is a project developed to identify possible issues in interior design plans before implementation. The main goal of this project is to reduce design mistakes by analyzing factors such as space usage, lighting, material selection, and layout planning at an early stage.

This project helped in understanding how technology can assist in improving planning and decision-making in interior design.

Key Features:
-Detects possible design inconsistencies early
-Analyzes important design factors like space, lighting, materials, and layout
-Provides suggestion-based improvements 
-Simple and easy-to-use interface
-Helps reduce unnecessary cost, time, and rework

Tech Stack:
Programming Language: Python
Frameworks: Django, Flask (Basic)
Frontend: HTML, CSS
Database: SQLite
Project Preview

⚠️ Note:
This project is not currently deployed as a fully working live website because it is built using Django backend functionalities.
The GitHub Pages/live link may not work properly, but you can still explore the project through the "Project Screenshots" folder available in this repository.

How It Works:
The system takes input related to an interior design plan and processes it using predefined logic and conditions. Based on the inputs provided, it predicts possible design failures and suggests improvements to achieve a better and more efficient design plan.

Setup Instructions :
1. Clone the repository
git clone https://github.com/yourusername/interior-design-prediction.git
cd interior-design-prediction
2. Create a virtual environment
python -m venv venv
3. Activate the environment
Windows
venv\Scripts\activate
macOS/Linux
source venv/bin/activate
4. Install required packages
pip install -r requirements.txt
5. Create a .env file in the project root directory and add the required settings such as:
SECRET_KEY
ALLOWED_HOSTS
Database configurations
6. Apply migrations
python manage.py migrate
7. Create admin account
python manage.py createsuperuser
8. Run the project
python manage.py runserver
10. Open in browser
http://127.0.0.1:8000/

Important Notes : 
-The ML model files (interior_model.pkl, room_encoder.pkl, etc.) are necessary for prediction functionality.
-Make sure these files are placed inside the appropriate project directory.
-The project uses SQLite as the default database.
-This project was mainly developed for learning and academic purposes.
-Future Improvements
-Integration of advanced Machine Learning model.
-Better UI/UX design
-Deployment as a live web application
-Use of real-world datasets for improved prediction accuracy

What I Learned :
Through this project, I gained practical experience in:
-Django and basic Flask development
-Backend logic implementation
-Building prediction-based systems
-Managing a complete project structure from frontend to backend

Author - Harni S B

Disclaimer - This project was created for academic learning and practice purposes.
