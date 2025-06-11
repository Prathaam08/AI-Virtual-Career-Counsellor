# 💼 AI Virtual Career Counsellor

An intelligent, multilingual career guidance chatbot built with **Streamlit**, **NLP**, and **machine learning**. This virtual counsellor recommends ideal career paths based on your interests, personality, and current job market trends.

![Banner](assets/banner.png)

---

## 🚀 Features

- 🔍 **Interest-based career suggestions**
- 🌍 **Multilingual input support** (via Google Translate)
- 📈 **Real-time job & salary data** (powered by Adzuna API)
- 📚 Curated **learning resources** per career path
- 🧠 Clean, modern, and interactive UI (Streamlit + custom CSS)

---

## 🖼️ Demo

![Demo GIF](https://github.com/your-username/demo-career-bot.gif)  
> *Enter interests like “I love coding and solving logical problems” or “I like helping others” to get instant career recommendations!*

---

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Prathaam08/AI-Virtual-Career-Counsellor.git
   cd AI-Virtual-Career-Counsellor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 🧠 Dataset

The `data/careers.csv` file includes:
- `interest`: Broad career domains (e.g., Technology, Arts)
- `careers`: Career suggestions (e.g., Data Scientist, Doctor)
- `keywords`: Matched against user input for suggestions
---

## 🌐 API Integration

This app fetches **live job data** and **average salary** using the [Adzuna Job API](https://developer.adzuna.com/overview). You can get your free API key and add it to `app.py`:

```python
app_id = "your_app_id"
app_key = "your_app_key"
```

---

---

## 🌟 Credits

- **Streamlit** – UI framework
- **Hugging Face Transformers** – NLP tools
- **Adzuna** – Job & salary data
- **Deep Translator** – Language translation
- **NLTK** – Preprocessing & tokenization

---



