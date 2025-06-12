import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By

# --- Load correct answers from DB ---
correct_answers = {}

conn = sqlite3.connect("instance/quiz.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT q.text, a.text 
    FROM question q
    JOIN answer_option a ON q.id = a.question_id
    WHERE a.is_correct = 1
""")
for q_text, a_text in cursor.fetchall():
    correct_answers[q_text.strip()] = a_text.strip()
conn.close()

# --- Set up Selenium ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: remove this to see browser
driver = webdriver.Chrome(options=options)

try:
    # Login
    driver.get("http://localhost:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "password").send_keys("test123")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)

    # Navigate to quiz
    driver.get("http://localhost:5000/qualification")
    time.sleep(2)

    # For each .question block, find correct answer
    question_blocks = driver.find_elements(By.CLASS_NAME, "question")
    for block in question_blocks:
        question_text = block.find_element(By.TAG_NAME, "h4").text
        # Extract only the question (remove "Q1. ..." prefix)
        question_clean = question_text.split(". ", 1)[-1].strip()

        correct_answer = correct_answers.get(question_clean)
        if not correct_answer:
            print(f"⚠️ No correct answer found for: {question_clean}")
            continue

        # Find all <label> elements in the block
        labels = block.find_elements(By.TAG_NAME, "label")
        for label in labels:
            if correct_answer.lower() in label.text.strip().lower():
                label.find_element(By.TAG_NAME, "input").click()
                break
        else:
            print(
                f"❌ Correct answer not found in options for: {question_clean}")

    # Submit the quiz
    driver.find_element(By.CSS_SELECTOR, ".submit-btn").click()
    time.sleep(2)

    # Check result
    page_text = driver.find_element(By.TAG_NAME, "body").text
    if "passed" in page_text.lower():
        print("✅ Quiz passed successfully!")
    else:
        print("❌ Quiz failed.")

finally:
    driver.quit()
