import streamlit as st
import pandas as pd
import nltk, requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from deep_translator import GoogleTranslator
import re


# NLTK downloads
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/careers.csv")

# Preprocessing

def preprocess_text(text):
    # Tokenize with regex instead of NLTK's word_tokenize
    tokens = re.findall(r'\b\w+\b', text.lower())
    stop_words = set(stopwords.words('english'))
    return [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]


# Career recommendation
def recommend_career(user_input, df, personality=None):
    tokens = preprocess_text(user_input)
    scores = {}
    for _, row in df.iterrows():
        keywords = [k.strip() for k in row.keywords.split(',')]
        score = sum(1 for t in tokens if t in keywords)
        if personality:
            score += sum(personality.get(c, 0) for c in row.get("personality_traits", "").split(","))
        if score > 0:
            scores[row.interest] = {'score': score, 'careers': row.careers.split(", ")}
    return max(scores.items(), key=lambda x: x[1]['score'])[1] if scores else None

def fetch_job_data(career, location="in"):
    app_id = "89dc0881"
    app_key = "c7c0a907f3d157ccfc1ed872e19faa3c"
    url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": career,
        "content-type": "application/json"
    }

    try:
        r = requests.get(url, params=params)
        data = r.json()
        results = data.get("results", [])

        salaries = []
        for job in results:
            min_salary = job.get("salary_min")
            max_salary = job.get("salary_max")
            if isinstance(min_salary, (int, float)) and isinstance(max_salary, (int, float)):
                avg = (min_salary + max_salary) / 2
                salaries.append(avg)

        avg_salary = sum(salaries) / len(salaries) if salaries else None

        return {
            "count": data.get("count", 0),
            "avg_salary": avg_salary
        }

    except Exception as e:
        print("Adzuna API Error:", e)
        return {"count": 0, "avg_salary": None}

fallback_salary = {
    "Software Developer": 700000,
    "Data Scientist": 800000,
    "Doctor": 1000000,
    "Mechanical Engineer": 600000,
    "Lawyer": 900000,
    "Journalist": 500000,
    "Social Worker": 400000,
    "Athlete": 300000,
    "Environmental Scientist": 550000
}


# Career learning resources
career_resources = {
    "Software Developer": [
        "🔗 [freeCodeCamp](https://www.freecodecamp.org)",
        "🔗 [Harvard CS50](https://cs50.harvard.edu)",
        "🔗 [LeetCode](https://leetcode.com)"
    ],
    "Data Scientist": [
        "🔗 [Kaggle Learn](https://www.kaggle.com/learn)",
        "🔗 [Coursera - Data Science](https://www.coursera.org/specializations/jhu-data-science)",
        "🔗 [DataCamp](https://www.datacamp.com)"
    ],
    "Doctor": [
        "🔗 [Khan Academy Health](https://www.khanacademy.org/science/health-and-medicine)",
        "🔗 [Coursera Medical Courses](https://www.coursera.org/courses?query=medicine)",
        "🔗 [YouTube - Osmosis](https://www.youtube.com/user/OsmosisOrg)"
    ],
    "Mechanical Engineer": [
        "🔗 [MIT OpenCourseWare - Mechanical Engineering](https://ocw.mit.edu/courses/mechanical-engineering/)",
        "🔗 [Coursera - Engineering Mechanics](https://www.coursera.org/learn/engineering-mechanics-statics)",
        "🔗 [edX - Mechanical Behavior of Materials](https://www.edx.org/course/mechanical-behavior-of-materials-part-1)"
    ],
    "Lawyer": [
        "🔗 [Harvard Law Open Courses](https://online-learning.harvard.edu/subject/law)",
        "🔗 [Coursera - Legal Courses](https://www.coursera.org/courses?query=law)",
        "🔗 [YouTube - LegalEagle](https://www.youtube.com/c/LegalEagle)"
    ],
    "Journalist": [
        "🔗 [edX - Journalism Courses](https://www.edx.org/learn/journalism)",
        "🔗 [Coursera - News Reporting](https://www.coursera.org/courses?query=journalism)",
        "🔗 [YouTube - Journalism Skills](https://www.youtube.com/results?search_query=journalism+skills)"
    ],
    "Social Worker": [
        "🔗 [Coursera - Social Work](https://www.coursera.org/courses?query=social%20work)",
        "🔗 [edX - Social Work](https://www.edx.org/learn/social-work)",
        "🔗 [UNICEF Volunteer Portal](https://www.unv.org/become-volunteer)"
    ],
    "Athlete": [
        "🔗 [Coursera - Sports Coaching](https://www.coursera.org/learn/sports-coaching)",
        "🔗 [Udemy - Fitness Coach](https://www.udemy.com/course/becomeafitnesscoach/)",
        "🔗 [YouTube - Sports Training](https://www.youtube.com/results?search_query=sports+training)"
    ],
    "Environmental Scientist": [
        "🔗 [Coursera - Environmental Science](https://www.coursera.org/specializations/environmental-science)",
        "🔗 [edX - Sustainability](https://www.edx.org/learn/sustainability)",
        "🔗 [NASA Climate Kids](https://climatekids.nasa.gov/)"
    ]
}


# Translate input to English
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

# Streamlit UI
# UI
st.set_page_config(page_title="AI Career Counsellor", layout="centered")

st.image("assets/banner.png", use_column_width=True)
st.title("💼 AI Career Counsellor Chatbot")
st.caption("Powered by NLP, job market data, and learning links.")

st.sidebar.title("📚 About")
st.sidebar.info("This AI bot suggests careers based on your interests using NLP and job trends from Adzuna API.")
st.sidebar.markdown("🌐 [Source Code](https://github.com/Prathaam08/AI-Virtual-Career-Counsellor.git)")

# Load data
df = load_data()

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Hi! What are your interests or hobbies? (Eg: Coding , Maths , Arts , Media , etc)"}]
if "last_recommendation" not in st.session_state:
    st.session_state.last_recommendation = None
if "personality_score" not in st.session_state:
    st.session_state.personality_score = {}

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Handle chat input
if user_input := st.chat_input("Describe your interests or ask for resources..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    translated = translate_to_english(user_input.lower())

    if translated in ["yes", "yeah", "sure", "ok", "give links"]:
        last = st.session_state.last_recommendation
        if last in career_resources:
            links = "\n".join(career_resources[last])
            reply = f"Here are great resources to begin your **{last}** journey:\n\n{links}"
        else:
            reply = "Sorry, I don't have specific resources for that career yet."
    else:
        result = recommend_career(translated, df, st.session_state.personality_score)
        if result:
            main = result["careers"][0]
            st.session_state.last_recommendation = main
            others = ", ".join(result["careers"][1:]) if len(result["careers"]) > 1 else ""
            reply = f"Based on your input, a great career would be **{main}**! 🎯"
            if others:
                reply += f"\n\nOther roles: {others}"

            job_data = fetch_job_data(main)
            if job_data["count"] > 0:
              reply += f"\n\n📈 Currently, there are about **{job_data['count']}** jobs for **{main}**."
              if job_data["avg_salary"]:
                reply += f" Average salary: **₹{int(job_data['avg_salary']):,}**."
              elif main in fallback_salary:
                reply += f" Estimated average salary: **₹{fallback_salary[main]:,}**."
              else:
                reply += " Salary data not available currently."
            reply += "\n\nWould you like learning resources?"
        else:
            reply = "I couldn't detect any specific interest. Try rephrasing?"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

  


