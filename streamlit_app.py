import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Загружаем токен из .env
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

# Подключаемся к клиенту HuggingFace
client = InferenceClient(token=hf_token)
# Установи путь для конфигов Streamlit в текущей папке проекта
os.environ["STREAMLIT_CONFIG_DIR"] = os.path.join(os.getcwd(), ".streamlit")
# Настройка интерфейса Streamlit
st.set_page_config(page_title="LexGap AI", layout="wide")
st.title("LexGap AI - Анализ законодательства")

col1, col2 = st.columns([2, 1])

# Модель генерации на русском/испанском языке (подходит и для суммаризации и переформулировки)
model_id = "google/flan-t5-large"

with col1:
    law_text = st.text_area("Вставьте текст закона для анализа:", height=400)

    if st.button("Анализировать"):
        if law_text.strip():
            st.success("✅ Анализ завершен. Выявленные бреши:")

            # Промпт для генерации рекомендаций
            prompt = f"Проанализируй следующий текст закона и предложи 3 улучшения формулировки:\n\n{law_text}\n\nФормат: Была → Стала"

            with st.spinner("ИИ анализирует и предлагает варианты..."):
                try:
                    result = client.text_generation(
                        model=model_id,
                        prompt=prompt,
                        max_new_tokens=300,
                        temperature=0.7
                    )
                    suggestions_text = result.strip()
                except Exception as e:
                    suggestions_text = f"⚠️ Ошибка при запросе к HuggingFace: {e}"
        else:
            st.warning("⚠️ Пожалуйста, вставьте текст закона для анализа.")

with col2:
    st.markdown("#### 🔁 Альтернативные формулировки от ИИ:")

    if 'suggestions_text' in locals():
        for line in suggestions_text.split("\n"):
            if line.strip():
                st.markdown(f"🔹 {line.strip()}")
    else:
        st.info("💡 Ожидается текст от ИИ после анализа.")
