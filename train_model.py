import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# -----------------------------
# Step 1: Create Dataset
# -----------------------------
data = pd.DataFrame([
    # Data Scientist
    ["Experienced in Python, Machine Learning, TensorFlow, NLP, data analysis using pandas and numpy.", "Data Scientist"],
    ["Worked on deep learning, computer vision, PyTorch, neural networks.", "Data Scientist"],

    # Web Application Developer
    ["Skilled in HTML, CSS, JavaScript, React.js, building responsive web applications.", "Web Application Developer"],
    ["Built full-stack applications using Django, Node.js, MongoDB and REST APIs.", "Web Application Developer"],

    # Java Developer
    ["Strong knowledge of Java, Spring Boot, MySQL, backend API development.", "Java Developer"],

    # HR / MBA
    ["Handled recruitment process, onboarding, payroll management, employee engagement.", "HR"],
    ["Managed talent acquisition, training, and performance evaluation.", "HR"],
    ["Experience in HR policies, employee engagement programs, and payroll management.", "HR"]
], columns=['resume_text','category'])

# -----------------------------
# Step 2: Vectorize Resumes
# -----------------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['resume_text'])
y = data['category']

# -----------------------------
# Step 3: Train Model
# -----------------------------
model = MultinomialNB()
model.fit(X, y)

# -----------------------------
# Step 4: Save Model & Vectorizer
# -----------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model and vectorizer saved successfully!")