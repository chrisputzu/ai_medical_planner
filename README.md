# Ai Medical Planner 📅💊

Welcome to the **Ai Medical Planner**! This tool uses cutting-edge AI to extract and structure the medication details from images and generate a comprehensive, easy-to-read table.

---

### 🛠 Features:
- Extracts the details of a patient's medication plan from an uploaded image 🖼️.
- Creates a well-organized medication schedule table with relevant columns 📊:
  - **Time** 🕐
  - **Medication Name** 💊
  - **Medication Type** 🧬
  - **Dosage** ⚖️
  - **Details** 📝
- Converts the extracted data into a structured Excel file 📈.
- Provides a downloadable file containing the organized medication schedule 📥.

---

### ⚙️ How it Works:
1. Upload an image 📸 containing the prescription or medical instructions.
2. Enter the patient's name 👤.
3. The AI processes the image and extracts medication details.
4. The medication schedule is displayed on your screen and can be downloaded as an Excel file 📄.

---

### 📝 Example Data:

| Time  | Medication Name | Medication Type | Dosage    | Details                                           |
|-------|-----------------|-----------------|-----------|---------------------------------------------------|
| 07:00 | Paracetamol     | Analgesic       | 1000 mg   | 2 tablets per day for 7 days, then 1 tablet for the next 10 days. |

---

### 🔑 Requirements:
- Python 3.x
- `streamlit` 🖥️
- `google.generativeai` 🧠
- `pandas` 📊
- `PIL` (Pillow) 📷
- `dotenv` for environment variables 🔒

To install the necessary dependencies:

```bash
pip install streamlit google-generativeai pandas pillow python-dotenv
```

---

### 📑 Configuration:
1. Make sure to create a `.env` file with your **Google API key** for accessing the AI model.

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

### 🚀 Run the App:
To run the Medication Schedule Generator app locally:

```bash
streamlit run app.py
```

Enjoy the efficiency of generating precise medication schedules for patients! 🩺
