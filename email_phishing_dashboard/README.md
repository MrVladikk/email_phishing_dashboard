# Phishing Dashboard

**Интерактивный дашборд для анализа email‑сообщений и выявления фишинга.**

---

## 📂 Структура проекта

```
email_phishing_dashboard/
├── app.py                  # основной скрипт Streamlit
├── requirements.txt        # зависимости проекта
├── email_phishing_data.csv # пример исходных данных
└── README.md               # документация по установке и использованию
```

---

## ⚙️ Установка

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone https://github.com/MrVladikk/email_phishing_dashboard.git
   cd email_phishing_dashboard
   ```
2. Создайте и активируйте виртуальное окружение:
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows (CMD)**:
     ```cmd
     python -m venv venv
     venv\Scripts\activate.bat
     ```
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Запуск

```bash
streamlit run app.py
```

Если команда `streamlit` не распознаётся, используйте:

```bash
python -m streamlit run app.py
```

Перейдите в браузер по адресу `http://localhost:8501`.

---

## 📖 Использование

1. **Загрузка данных**
   - Исходный CSV: `email_phishing_data.csv`
   - Дополнительные CSV: через боковую панель → «Загрузить CSV с новыми письмами»
2. **Фильтры** (в боковом меню):
   - **Тип письма**: Легитимное / Фишинг
   - **Количество слов**
   - **Уникальные слова**
   - **Стоп‑слова**
   - **Ссылки**
   - **Уникальные домены**
   - **Email‑адреса внутри письма**
   - **Орфографические ошибки**
   - **Срочные ключевые слова**
3. **Метрики**
   - Всего писем
   - Количество фишинговых
   - Среднее число слов
4. **Визуализация**
   - Гистограмма распределения числа слов для легитимных и фишинговых писем
5. **Таблица**
   - Просмотр отфильтрованных строк
6. **Экспорт**
   - Кнопка «Скачать .xlsx» для сохранения результатов