# Infosys Internship Project - Group 5

## Team Members
- **Rahul Kothuri**
- **Akshar Rao Deshaveni**
- **Dhiraj Laulkar**
- **Kratin Verma**

---

## Project Title
**AI-Driven Patient Follow-Up and Health Outcome Prediction System for Telemedicine**

---

## Project Overview
This project focuses on leveraging AI and machine learning to enhance telemedicine services by analyzing lung cancer risk and enabling proactive patient follow-up. It consists of the following key components:

1. **Lung Cancer Analysis and Prediction**
   - Developed models using **K-Nearest Neighbors (KNN)** and **Random Forest** for lung cancer prediction based on medical data.

2. **Retrieval-Augmented Generation (RAG) Application**
   - A chatbot application was built to facilitate **Doctor-Patient Conversations**.
   - The chatbot provides intelligent responses, enabling streamlined communication between doctors and patients.

3. **Doctor-Patient Analysis Dashboard**
   - A web-based dashboard showcasing:
     - **Analysis of medical conversations.**
     - Patient risk levels and engagement metrics.

4. **Calendar Integration for Follow-Up Scheduling**
   - A Python script that:
     - Takes the patient conversation as input.
     - Predicts the lung cancer risk level.
     - Automatically schedules follow-up meetings in **Google Calendar**.

---

## Technologies Used

### Machine Learning
- **KNN** and **Random Forest** for lung cancer prediction.
- **Python** for model development and integration.

### AI Applications
- **Retrieval-Augmented Generation (RAG)** to power the chatbot system.

### Data Visualization
- **Dashboards** for real-time insights into patient analysis.

### Scheduling
- **Google Calendar API** for seamless follow-up meeting integration.

---

## How to Run

### Prerequisites
- Python 3.8+
- Libraries: `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `flask`, `google-api-python-client`
- Google Calendar API credentials file.

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/infosys-internship-project.git
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the dashboard and chatbot via the provided local server link.

---

## Features
- **Lung Cancer Prediction:**
  - Upload medical data to predict cancer risk using trained ML models.

- **Doctor-Patient Chatbot:**
  - Interact with the chatbot for personalized medical advice and responses.

- **Dashboard:**
  - View detailed analytics of patient conversations and predicted risk levels.

- **Google Calendar Integration:**
  - Schedule follow-up meetings automatically based on risk prediction.


## Acknowledgments
This project was completed as part of the **Infosys Springboard Internship Program**. We extend our gratitude to Infosys for the mentorship and resources provided.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For any queries or issues, please contact us via the repository or reach out to **Rahul Kothuri** (Team Lead).
