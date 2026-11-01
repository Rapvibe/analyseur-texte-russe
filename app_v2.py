
import streamlit as st
import re
import pandas as pd

# --------------------------------
# CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Анализатор русского текста",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Анализатор сложности русского текста")

st.write(
    "Программа для лингвистического анализа "
    "сложности и читаемости русского текста."
)

# --------------------------------
# LINGUISTIC ANALYSIS
# --------------------------------

VOWELS = "аеёиоуыэюя"

def count_syllables(word):
    """Приближённый подсчёт слогов по гласным."""
    return sum(1 for letter in word.lower() if letter in VOWELS)


def analyze_text(text):

    words = re.findall(
        r"[а-яёА-ЯЁ]+(?:-[а-яёА-ЯЁ]+)*",
        text
    )

    sentences = [
        s.strip()
        for s in re.split(r"[.!?]+", text)
        if s.strip()
    ]

    if not words:
        return None

    word_count = len(words)
    sentence_count = len(sentences)

    word_lengths = [len(w.replace("-", "")) for w in words]
    syllables = [count_syllables(w) for w in words]

    average_word_length = sum(word_lengths) / word_count
    average_syllables = sum(syllables) / word_count

    average_sentence_length = (
        word_count / sentence_count if sentence_count else 0
    )

    long_words = sum(1 for s in syllables if s >= 4)

    long_word_percentage = long_words / word_count * 100

    # Experimental complexity index: 0 to 100

    sentence_score = min(average_sentence_length / 25 * 30, 30)

    word_score = min(average_word_length / 10 * 25, 25)

    syllable_score = min(average_syllables / 4 * 20, 20)

    long_word_score = min(long_word_percentage / 100 * 25, 25)

    complexity = (
        sentence_score
        + word_score
        + syllable_score
        + long_word_score
    )

    if complexity < 30:
        level = "Низкая сложность"
    elif complexity < 60:
        level = "Средняя сложность"
    else:
        level = "Высокая сложность"

    return {
        "Количество слов": word_count,
        "Количество предложений": sentence_count,
        "Средняя длина предложения": round(average_sentence_length, 2),
        "Средняя длина слова": round(average_word_length, 2),
        "Среднее количество слогов": round(average_syllables, 2),
        "Количество длинных слов": long_words,
        "Доля длинных слов (%)": round(long_word_percentage, 2),
        "Индекс сложности": round(complexity, 2),
        "Уровень сложности": level
    }


# --------------------------------
# USER INTERFACE
# --------------------------------

st.subheader("Введите русский текст")

user_text = st.text_area(
    "Текст для анализа:",
    height=220,
    placeholder="Введите или вставьте русский текст здесь..."
)

if st.button("🔍 Анализировать текст", type="primary"):

    result = analyze_text(user_text)

    if result is None:
        st.warning("Пожалуйста, введите русский текст.")

    else:
        st.session_state["result"] = result

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.header("📊 Результаты анализа")

    col1, col2, col3 = st.columns(3)

    col1.metric("Количество слов", result["Количество слов"])

    col2.metric(
        "Количество предложений",
        result["Количество предложений"]
    )

    col3.metric(
        "Средняя длина предложения",
        result["Средняя длина предложения"]
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Средняя длина слова",
        result["Средняя длина слова"]
    )

    col5.metric(
        "Среднее количество слогов",
        result["Среднее количество слогов"]
    )

    col6.metric(
        "Длинные слова",
        result["Количество длинных слов"]
    )

    st.divider()

    st.header("🎯 Оценка сложности")

    st.metric(
        "Индекс сложности",
        f'{result["Индекс сложности"]} / 100'
    )

    st.progress(result["Индекс сложности"] / 100)

    st.info(
        "Уровень: " + result["Уровень сложности"]
    )

    st.caption(
        "Индекс является экспериментальной эвристической "
        "оценкой, разработанной в рамках проекта."
    )

    st.divider()

    st.header("📥 Экспорт результатов")

    df = pd.DataFrame(
        list(result.items()),
        columns=["Показатель", "Значение"]
    )

    csv_data = df.to_csv(
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )

    st.download_button(
        "Скачать результаты CSV",
        data=csv_data,
        file_name="analiz_russkogo_teksta.csv",
        mime="text/csv"
    )
 