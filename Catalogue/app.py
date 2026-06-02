import streamlit as st
import requests

API_URL = "http://localhost:8000/extract"

st.set_page_config(page_title="AI Cataloguer", layout="centered")

st.title("📚 AI Book Title Extractor")
st.write("Capture or upload a book image to extract the title")

# -----------------------------
# 📷 Camera Input
# -----------------------------
st.subheader("📷 Capture Image")
camera_image = st.camera_input("Take a picture")

# -----------------------------
# 📁 File Upload
# -----------------------------
st.subheader("📁 Upload Image")
uploaded_files = st.file_uploader(
    "Upload book image",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# -----------------------------
# 📦 Prepare Images
# -----------------------------
images = []

if camera_image is not None:
    images.append(
        ("images", ("camera.jpg", camera_image.getvalue(), "image/jpeg"))
    )

if uploaded_files:
    for file in uploaded_files:
        images.append(
            ("images", (file.name, file.getvalue(), file.type))
        )

# -----------------------------
# 🚀 Extract Button
# -----------------------------
if st.button("🔍 Extract Title"):

    if not images:
        st.warning("Please capture or upload an image.")
    else:
        with st.spinner("Extracting title using AI..."):

            try:
                response = requests.post(API_URL, files=images)

                if response.status_code == 200:
                    data = response.json()

                    st.success("✅ Title Extracted!")

                    # Display result
                    title = data.get("title", "")
                    st.text_input("Book Title", value=title)

                else:
                    st.error(f"API Error: {response.status_code}")

            except Exception as e:
                st.error("Failed to connect to API")
                st.exception(e)

# -----------------------------
# 🔄 Fetch Latest
# -----------------------------
st.markdown("---")
st.subheader("🔄 Fetch Latest Title")

if st.button("Fetch Latest"):
    try:
        res = requests.get("http://localhost:8000/latest")

        if res.status_code == 200:
            data = res.json()

            st.success("Latest Title Retrieved")
            st.text_input("Latest Title", value=data.get("title", ""))

        else:
            st.error("Could not fetch latest data")

    except Exception as e:
        st.error("API not reachable")
        st.exception(e)
