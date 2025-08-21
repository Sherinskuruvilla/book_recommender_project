import sys, os
import pandas as pd
import base64
import streamlit as st
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from book_recommender_model import recommend_books

# --- Paths ---
bg_path = os.path.join(os.path.dirname(__file__), "..", "images", "presentation_bg.jpg")  # Background image
img_path1 = os.path.join(os.path.dirname(__file__), "..", "images", "flow_chart.png")  # flow chart
flow_img = Image.open(img_path1)
flow_img = flow_img.resize((800, 600))  # shrink to fit nicely


# --- Set background image ---
def set_bg_image(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: auto;  /* keep natural size */
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: right top; /* 👈 top-right corner */
            }}
            .block-container {{
                text-align: left;
                max-width: 900px;
                margin-left: 0;
                margin-right: auto;
            }}
            div[data-testid="stTextInput"] > div > div {{
                background-color: #f5f5dc;
                border: 2px solid #8b5e3c;
                border-radius: 8px;
                padding: 4px 8px;
            }}
            div[data-testid="stTextInput"] input {{
                color: #4b2e2e !important;
            }}
            div[data-testid="stTextInput"] input::placeholder {{
                color: #7a6151;
                opacity: 0.9;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )


set_bg_image(bg_path)

# --- Sidebar background image ---
sidebar_img_path = os.path.join(os.path.dirname(__file__), "..", "images", "green.jpeg")
if os.path.exists(sidebar_img_path):
    with open(sidebar_img_path, "rb") as f:
        sidebar_encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-image: url("data:image/png;base64,{sidebar_encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] * {
            color: #0D1B2A !important;
            font-weight: bold !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# --- Sidebar Menu ---
st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Book Recommender", "About"])


# --- PAGE 1: Book Recommender ---
if page == "Book Recommender":
    st.title("Book Recommender")

    col_input, _ = st.columns([1, 2])
    with col_input:
        book_title = st.text_input("Enter a Book Title", key="book_input", placeholder="e.g., The Hobbit")

    if st.button("Recommend"):
        if book_title:
            recommended_books = recommend_books(book_title, top_n=6)

            if recommended_books.empty:
                st.write(f"No recommendations found for '{book_title}'.")
            else:
                st.subheader("Recommended Books:")
                df = recommended_books.reset_index()

                for i in range(0, len(df), 2):  # 2 per row
                    col1, col2 = st.columns(2)

                    with col1:
                        if pd.notna(df['image_url'][i]) and df['image_url'][i].lower() != "image is not available":
                            try:
                                st.image(df['image_url'][i], width=150)  # 🔹 fixed size
                            except Exception:
                                st.write("Image not available")
                        st.markdown(f"**{i+1}. {df['title'][i]}**")
                        st.text(f"Written by: {df['author'][i]} ")
                        st.text(f"Genre: {df['genre'][i]} ")
                        

                    if i + 1 < len(df):
                        with col2:
                            if pd.notna(df['image_url'][i+1]) and df['image_url'][i+1].lower() != "image is not available":
                                try:
                                    st.image(df['image_url'][i+1], width=150)  # 🔹 fixed size
                                except Exception:
                                    st.write("Image not available")
                            st.markdown(f"**{i+2}. {df['title'][i+1]}**")
                            st.text(f"Written by: {df['author'][i+1]} ")
                            st.text(f"Genre: {df['genre'][i+1]} ")
                            
# --- PAGE 2: Project Presentation ---
elif page == "About":
    st.title("About Book Recommender")

    if 'slide' not in st.session_state:
        st.session_state.slide = 1

    def next_slide():
        st.session_state.slide += 1

    def prev_slide():
        st.session_state.slide -= 1

    slide = st.session_state.slide

    # --- Slides ---
    if slide == 1:
        st.header("Project Overview")
        st.markdown("""
        - **Objective:** Build a book recommender system.    
        - **Goal:** Recommend books similar to a given title.
        """)

    elif slide == 2:
        st.header("Why a Book Recommender?")
        st.markdown("""
        - 🔍 Discover new books 
        - 🎯 Personalized suggestions  
        - ⏳ Saves time  
        - 📚 Encourages reading  
        - 📈 Supports authors & bookstores 
        """)

    elif slide == 3:
        st.header("📊 Data Overview")
        st.markdown("""
        - 📚 **1,000 books** → scraped from *Books to Scrape*  
        - 📖 **18,000 books** → collected from *Google Books*  
        - 🧹 Cleaned & merged → single **Books DataFrame**  
        - 🔑 Features:  
            • Title  
            • Author  
            • Genre  
            • Description  
            • Image URL  
        """)

    elif slide == 4:
        st.image(flow_img, width=500)

    else:
        st.image("https://gifdb.com/images/high/girl-bowing-thank-you-nbiuw5lhj9ehqay1.webp")

     # --- Navigation buttons at the bottom ---
    st.markdown("<br><br>", unsafe_allow_html=True)  # spacing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.slide > 1:
            st.button("Previous", on_click=prev_slide)
    with col3:
        st.button("Next", on_click=next_slide)
