import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model
model = joblib.load("model.pkl")  # pastikan file ini ada di folder yang sama

st.set_page_config(page_title="Prediksi Dropout Mahasiswa - Jaya Jaya Institut", layout="centered")
st.title("🎓 Prediksi Dropout Mahasiswa")
st.markdown("Isi data mahasiswa di bawah ini untuk memprediksi apakah mahasiswa berpotensi **Dropout** atau **Lulus**.")

# Form input pengguna
with st.form("form_prediksi"):
    st.subheader("Data Mahasiswa")

    age = st.slider("Umur saat masuk", 17, 70, 20)
    admission_grade = st.number_input("Nilai ujian masuk", min_value=0.0, max_value=200.0, value=120.0)
    previous_qualification_grade = st.number_input("Nilai kualifikasi sebelumnya", min_value=0.0, max_value=43.0, value=21.0)

    application_mode = st.selectbox(
        "Metode Pendaftaran",
        options=[1, 2, 5, 7, 10, 15, 16, 17, 18, 26, 27, 39, 42, 43, 44, 51, 53, 57],
        format_func=lambda x: {
            1: "1st phase - general contingent",
            2: "Ordinance No. 612/93",
            5: "1st phase - special contingent (Azores Island)",
            7: "Holders of other higher courses",
            10: "Ordinance No. 854-B/99",
            15: "International student (bachelor)",
            16: "1st phase - special contingent (Madeira Island)",
            17: "2nd phase - general contingent",
            18: "3rd phase - general contingent",
            26: "Ordinance No. 533-A/99, item b2) (Different Plan)",
            27: "Ordinance No. 533-A/99, item b3 (Other Institution)",
            39: "Over 23 years old",
            42: "Transfer",
            43: "Change of course",
            44: "Technological specialization diploma holders",
            51: "Change of institution/course",
            53: "Short cycle diploma holders",
            57: "Change of institution/course (International)"
        }[x]
    )

    application_order = st.slider("Urutan Pilihan Pendaftaran (0: Pilihan Pertama, 9: Terakhir)", 0, 9, 0)

    course = st.selectbox(
        "Program Studi",
        options=[33, 171, 8014, 9003, 9070, 9085, 9119, 9130, 9147, 9238, 9254, 9500, 9556, 9670, 9773, 9853, 9991],
        format_func=lambda x: {
            33: "Biofuel Production Technologies",
            171: "Animation and Multimedia Design",
            8014: "Social Service (evening attendance)",
            9003: "Agronomy",
            9070: "Communication Design",
            9085: "Veterinary Nursing",
            9119: "Informatics Engineering",
            9130: "Equinculture",
            9147: "Management",
            9238: "Social Service",
            9254: "Tourism",
            9500: "Nursing",
            9556: "Oral Hygiene",
            9670: "Advertising and Marketing Management",
            9773: "Journalism and Communication",
            9853: "Basic Education",
            9991: "Management (evening attendance)"
        }[x]
    )

    curricular_units_1st_sem_approved = st.slider("Mata kuliah disetujui di semester 1", 0, 26, 10)
    curricular_units_2nd_sem_approved = st.slider("Mata kuliah disetujui di semester 2", 0, 20, 10)
    curricular_units_1st_sem_grade = st.number_input("Rata-rata nilai semester 1", min_value=0.0, max_value=20.0, value=11.0)
    curricular_units_2nd_sem_grade = st.number_input("Rata-rata nilai semester 2", min_value=0.0, max_value=20.0, value=11.0)

    debtor = st.selectbox("Apakah mahasiswa menunggak biaya kuliah?", [0, 1], format_func=lambda x: "Tidak" if x == 0 else "Ya")
    tuition_fees_up_to_date = 0 if debtor == 1 else 1
    scholarship_holder = st.selectbox("Penerima beasiswa?", [0, 1])

    submitted = st.form_submit_button("Prediksi")

    if submitted:
        input_data = pd.DataFrame([[ 
            age,
            admission_grade,
            previous_qualification_grade,
            application_mode,
            application_order,
            course,
            curricular_units_1st_sem_approved,
            curricular_units_2nd_sem_approved,
            curricular_units_1st_sem_grade,
            curricular_units_2nd_sem_grade,
            debtor,
            tuition_fees_up_to_date,
            scholarship_holder
        ]], columns=[
            'Age_at_enrollment',
            'Admission_grade',
            'Previous_qualification_grade',
            'Application_mode',
            'Application_order',
            'Course',
            'Curricular_units_1st_sem_approved',
            'Curricular_units_2nd_sem_approved',
            'Curricular_units_1st_sem_grade',
            'Curricular_units_2nd_sem_grade',
            'Debtor',
            'Tuition_fees_up_to_date',
            'Scholarship_holder'
        ])

        prediction = model.predict(input_data)[0]
        status = "Dropout ❌" if prediction == 1 else "Lulus ✅"
        st.success(f"Mahasiswa diprediksi akan: **{status}**")