import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Ultimate OMR System")

st.title("📄 Ultimate OMR + Registration Reader")

# ---------------------------
# Answer Key
# ---------------------------
ANSWER_KEY = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "A"
}

# ---------------------------
# Registration Reader
# ---------------------------
def read_registration(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Dummy logic (replace later with real OMR grid)
    reg_number = "REG" + str(np.random.randint(1000,9999))
    return reg_number


# ---------------------------
# OMR Detection (Basic)
# ---------------------------
def detect_answers(image):

    # Dummy detected answers
    detected = {
        1: "A",
        2: "B",
        3: "D",
        4: "D",
        5: "A"
    }

    return detected


# ---------------------------
# Score Calculation
# ---------------------------
def calculate_score(detected):

    score = 0
    result = []

    for q in ANSWER_KEY:
        correct = ANSWER_KEY[q]
        marked = detected[q]

        if correct == marked:
            score += 1
            status = "Correct"
        else:
            status = "Wrong"

        result.append([q, correct, marked, status])

    return score, result


# ---------------------------
# Upload Section
# ---------------------------
uploaded = st.file_uploader("Upload OMR Sheet", type=["jpg","png","jpeg"])

if uploaded:

    image = Image.open(uploaded)
    image_np = np.array(image)

    st.image(image, caption="Uploaded Sheet")

    reg = read_registration(image_np)
    detected = detect_answers(image_np)

    score, table = calculate_score(detected)

    st.success(f"Registration Number: {reg}")
    st.success(f"Score: {score}/{len(ANSWER_KEY)}")

    df = pd.DataFrame(
        table,
        columns=["Question","Correct","Marked","Status"]
    )

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Result CSV",
        csv,
        "result.csv",
        "text/csv"
    )
