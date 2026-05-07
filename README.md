Interior Design Failure Prediction System

Overview -
The Interior Design Failure Prediction System is developed to identify potential issues in interior design plans before execution. It helps in detecting design flaws related to space utilization, material selection, lighting, and layout, allowing improvements at an early stage.
This project focuses on making design planning more efficient by reducing the chances of costly mistakes and rework.

Key Features -
*Early detection of design inconsistencies
*Analysis of multiple design factors (space, lighting, materials, layout)
*Suggestion-based improvements for better decision-making
*Simple and user-friendly interface
*Helps reduce cost, time, and resource wastage

Tech Stack - 
*Programming Language: Python
*Frameworks: Django, Flask (basic)
*Frontend: HTML, CSS
*Database: SQLite

How It Works -
The system takes input parameters related to an interior design plan and processes them using a rule-based, data-driven approach. Based on predefined conditions and logic, it identifies possible design failures and provides suggestions to improve the overall design quality.

Setup Instructions - 
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/interior-design-prediction.git
   cd interior-design-prediction
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```
   Update `.env` with your settings (SECRET_KEY, ALLOWED_HOSTS, etc.)

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Open in browser:
   ```
   http://127.0.0.1:8000/
   ```

9. Admin panel (optional):
   ```
   http://127.0.0.1:8000/admin
   ```

Important Notes:
- The ML model files (interior_model.pkl, room_encoder.pkl, etc.) are required to run predictions. Make sure these files are in the `inte_des/` directory.
- See `train_model.py` to regenerate the model files if needed.
- Database is SQLite by default; for production, configure PostgreSQL in `.env`

Future Enhancements -
*Integration of Machine Learning models for advanced predictions
*Enhanced UI/UX for better user experience
*Deployment as a live web application
*Use of real-world datasets for improved accuracy

Learning Outcome - 
*Gained hands-on experience with Django and Flask
*Improved understanding of backend development
*Learned to design logic-based predictive systems
*Worked on structuring a complete end-to-end project

Author -
Harni S B

Disclaimer -
This project is developed for academic and learning purposes.
