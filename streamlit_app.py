import streamlit as st
import pandas as pd
import openai

# Set page config
st.set_page_config(page_title="The Grind Theory | Coffee Match", page_icon="☕", layout="wide")

# Updated styling with Tailwind CSS and modern design
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        /* Modern theme */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d1f1f 100%);
            color: #fff;
        }
        
        /* Card Container Fix */
        .element-container {
            position: relative;
        }
        
        /* Survey Cards */
        .card-click-wrapper {
            position: relative;
            width: 100%;
            height: 400px;
            margin-bottom: 1rem;
        }
        .survey-card {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 15px;
            overflow: hidden;
            background: rgba(255,255,255,0.05);
            transition: all 0.3s ease;
        }
        .survey-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .survey-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: all 0.3s ease;
        }
        .survey-card:hover img {
            transform: scale(1.05);
        }
        .survey-card-title {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px);
            color: #fff;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
        }
        
        /* Button Overlay Fix */
        .stButton {
            position: absolute !important;
            inset: 0 !important;
            z-index: 100 !important;
        }
        .stButton > button {
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            opacity: 0 !important;
            cursor: pointer !important;
        }
        
        /* Minimalist Profile Design */
        .profile-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 2rem auto;
            max-width: 1200px;
        }
        .profile-item {
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 1.5rem;
            flex: 1;
            min-width: 200px;
            border-bottom: 2px solid #d4a574;
            transition: transform 0.2s ease;
        }
        .profile-item:hover {
            transform: translateY(-2px);
        }
        .profile-label {
            color: #d4a574;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 0.5rem;
            opacity: 0.8;
        }
        .profile-value {
            color: #fff;
            font-size: 1.25rem;
            font-weight: 300;
        }
    </style>
""", unsafe_allow_html=True)

# Improved CSS for full clickable cards and minimalist, polished design
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/@fontsource-variable/inter@latest/index.min.css" rel="stylesheet">
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter Variable', Inter, Arial, sans-serif !important;
            background: linear-gradient(135deg, #18181b 0%, #23272f 100%);
            color: #f3f4f6;
        }
        .card-click-wrapper {
            position: relative;
            width: 100%;
            height: 340px;
            margin-bottom: 1.5rem;
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 2px 16px 0 rgba(0,0,0,0.10);
            background: #23272f;
            transition: box-shadow 0.2s;
        }
        .card-click-wrapper:hover {
            box-shadow: 0 6px 32px 0 rgba(0,0,0,0.18);
        }
        .survey-card-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition: transform 0.3s;
        }
        .card-click-wrapper:hover .survey-card-img {
            transform: scale(1.04);
        }
        .survey-card-title {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1.1rem 1rem 1.1rem 1rem;
            background: rgba(24,24,27,0.82);
            color: #f3f4f6;
            text-align: center;
            font-size: 1.18rem;
            font-weight: 500;
            letter-spacing: 0.01em;
            border-bottom-left-radius: 18px;
            border-bottom-right-radius: 18px;
        }
        .card-btn-overlay {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
            background: none;
            border: none;
            padding: 0;
            margin: 0;
            opacity: 0;
            cursor: pointer;
        }
        /* Minimalist Profile */
        .profile-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            justify-content: center;
            margin: 2.5rem 0 2rem 0;
        }
        .profile-item {
            background: #23272f;
            border-radius: 14px;
            padding: 1.5rem 2rem;
            min-width: 180px;
            box-shadow: 0 2px 8px 0 rgba(0,0,0,0.08);
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .profile-label {
            color: #a3a3a3;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 0.4rem;
        }
        .profile-value {
            color: #f3f4f6;
            font-size: 1.3rem;
            font-weight: 500;
            letter-spacing: 0.01em;
        }
        /* Recommendations */
        .recommendation-container {
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            justify-content: center;
            margin: 2.5rem 0 2rem 0;
        }
        .recommendation-card {
            background: #23272f;
            border-radius: 16px;
            box-shadow: 0 2px 12px 0 rgba(0,0,0,0.10);
            padding: 1.5rem 1.5rem 1.2rem 1.5rem;
            min-width: 260px;
            max-width: 340px;
            flex: 1 1 260px;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            transition: box-shadow 0.2s;
        }
        .recommendation-card:hover {
            box-shadow: 0 6px 32px 0 rgba(0,0,0,0.18);
        }
        .coffee-name {
            color: #fbbf24;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.7rem;
            letter-spacing: 0.01em;
        }
        .coffee-detail {
            color: #f3f4f6;
            font-size: 1.05rem;
            margin-bottom: 0.3rem;
            font-weight: 400;
        }
        .coffee-label {
            color: #a3a3a3;
            font-size: 0.92rem;
            font-weight: 500;
            margin-right: 0.3rem;
        }
    </style>
""", unsafe_allow_html=True)

# Add new styles after existing CSS
st.markdown("""
    <style>
        /* Button Styles */
        .stButton > button {
            background-color: #d4a574 !important;
            color: #1a0f0a !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 500 !important;
            border: none !important;
            margin-top: 10px !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            opacity: 1 !important;
            position: relative !important;
            cursor: pointer !important;
        }
        .stButton > button:hover {
            background-color: #b88b5c !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        }
        
        /* Share Button */
        .share-button {
            display: inline-flex;
            align-items: center;
            padding: 0.75rem 1.5rem;
            background: #1DA1F2;
            color: white;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }
        .share-button:hover {
            background: #1991db;
            transform: translateY(-2px);
        }
        .share-container {
            text-align: center;
            margin: 2rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Add audio for a jazz coffee song
#st.markdown("""
    #<audio autoplay loop>
        #<source src="https://www.bensound.com/bensound-music/bensound-jazzyfrenchy.mp3" type="audio/mpeg">
        #Your browser does not support the audio element.
    #</audio>
#""", unsafe_allow_html=True)

# Load product catalog
@st.cache_data
def load_catalog():
    return pd.read_csv("the_grind_theory_catalog.csv")

df_catalog = load_catalog()

# Initialize session state
if 'preferences' not in st.session_state:
    st.session_state.preferences = {}
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'gpt_message' not in st.session_state:
    st.session_state.gpt_message = ""

# Page Title
st.title("\u2615 The Grind Theory: Find Your Perfect Coffee")
st.markdown("""
<div style='text-align: center; font-size:18px;'>
Welcome! Let's discover your perfect coffee match.<br>
Answer a few quick questions! 🚀
</div>
""", unsafe_allow_html=True)

st.markdown("---")

def create_card(title, image_url, key):
    col = st.container()
    with col:
        st.markdown(f"""
            <div class="card-click-wrapper">
                <img class="survey-card-img" src="{image_url}" alt="{title}">
            </div>
        """, unsafe_allow_html=True)
        return st.button(f"Choose {title}", key=key)

# Update image URLs with fixed dimensions
IMAGES = {
    "hot": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500&h=500&fit=crop",
    "cold": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=500&h=500&fit=crop",
    "chocolatey": "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=500&h=500&fit=crop",
    "fruity": "https://images.unsplash.com/photo-1546173159-315724a31696?w=500&h=500&fit=crop",
    "nutty": "https://images.unsplash.com/photo-1604492176339-c8172326fc25?w=500&h=500&fit=crop",
    "espresso": "https://images.unsplash.com/photo-1587075706555-c1329c8a75fc?w=500&h=500&fit=crop",
    "french": "https://images.unsplash.com/photo-1544887534-3d1169e69487?w=500&h=500&fit=crop",
    "pour": "https://images.unsplash.com/photo-1545665225-b23b99e4d45e?w=500&h=500&fit=crop",
    "mild": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500&h=500&fit=crop",
    "medium": "https://images.unsplash.com/photo-1511537190424-bbbab87ac5eb?w=500&h=500&fit=crop",
    "strong": "https://images.unsplash.com/photo-1521302080334-4bebac2763a6?w=500&h=500&fit=crop"
}

# Step 1: Temperature
if st.session_state.step == 1:
    st.markdown("<h2 style='text-align: center;'>How do you prefer your coffee?</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if create_card("Hot ☕", IMAGES["hot"], "hot"):
            st.session_state.preferences['Temperature'] = 'Hot'
            st.session_state.step += 1
            st.rerun()
            
    with col2:
        if create_card("Cold ❄️", IMAGES["cold"], "cold"):
            st.session_state.preferences['Temperature'] = 'Cold'
            st.session_state.step += 1
            st.rerun()

# Step 2: Flavor Notes
elif st.session_state.step == 2:
    st.markdown("<h2 style='text-align: center;'>What flavor notes do you prefer?</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    flavors = {
        "Chocolatey 🍫": (IMAGES["chocolatey"], col1),
        "Fruity 🍒": (IMAGES["fruity"], col2),
        "Nutty 🌰": (IMAGES["nutty"], col3)
    }
    
    for flavor, (img, col) in flavors.items():
        with col:
            if create_card(flavor, img, f"flavor_{flavor}"):
                st.session_state.preferences['Flavor'] = flavor.split()[0]
                st.session_state.step += 1
                st.rerun()

# Step 3: Brewing Method
elif st.session_state.step == 3:
    st.markdown("<h2 style='text-align: center;'>How do you usually brew your coffee?</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    methods = {
        "Espresso Machine ☕": (IMAGES["espresso"], col1),
        "French Press 🍶": (IMAGES["french"], col2),
        "Pour Over 💧": (IMAGES["pour"], col3)
    }
    
    for method, (img, col) in methods.items():
        with col:
            if create_card(method, img, f"method_{method}"):
                st.session_state.preferences['Brew Method'] = method.split()[0]
                st.session_state.step += 1
                st.rerun()

# Step 4: Strength
elif st.session_state.step == 4:
    st.markdown("<h2 style='text-align: center;'>How strong do you like your coffee?</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    strengths = {
        "Mild 🌿": (IMAGES["mild"], col1),
        "Medium ⚖️": (IMAGES["medium"], col2),
        "Strong 💪": (IMAGES["strong"], col3)
    }
    
    for strength, (img, col) in strengths.items():
        with col:
            if create_card(strength, img, f"strength_{strength}"):
                st.session_state.preferences['Strength'] = strength.split()[0]
                st.session_state.step += 1
                st.rerun()

# Step 5: Results
elif st.session_state.step == 5:
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Your Perfect Coffee Match</h2>", unsafe_allow_html=True)
    prefs = st.session_state.preferences

    # Minimalist profile display
    st.markdown("<div class='profile-container'>", unsafe_allow_html=True)
    
    for key, value in prefs.items():
        st.markdown(f"""
            <div class='profile-item'>
                <div class='profile-label'>{key}</div>
                <div class='profile-value'>{value}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Filter and display recommendations
    filtered = df_catalog[
        df_catalog['Flavor Notes'].str.contains(prefs['Flavor'], case=False) &
        df_catalog['Brew Method'].str.contains(prefs['Brew Method'], case=False) &
        df_catalog['Strength'].str.contains(prefs['Strength'], case=False)
    ]

    if not filtered.empty:
        top_recs = filtered.sample(min(3, len(filtered)))
        st.markdown("<h3 style='color: #fbbf24; margin: 2.5rem 0 1.5rem;'>🌟 Recommended Coffees</h3>", unsafe_allow_html=True)
        st.markdown("<div class='recommendation-container'>", unsafe_allow_html=True)
        for _, row in top_recs.iterrows():
            st.markdown(f"""
                <div class="recommendation-card">
                    <div class="coffee-name">{row['Product Name']}</div>
                    <div class="coffee-detail"><span class="coffee-label">Roast:</span>{row['Roast Level']}</div>
                    <div class="coffee-detail"><span class="coffee-label">Notes:</span>{row['Flavor Notes']}</div>
                    <div class="coffee-detail"><span class="coffee-label">Brew:</span>{row['Brew Method']}</div>
                    <div class="coffee-detail"><span class="coffee-label">Strength:</span>{row['Strength']}</div>
                    <div class="coffee-detail"><span class="coffee-label">Price:</span>€{row['Price (€)']}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Generate GPT message with loading spinner
        if st.session_state.gpt_message == "":
            openai.api_key = st.secrets["openai"]["OPENAI_API_KEY"]
            user_pref_summary = f"Flavor: {prefs['Flavor']}, Brew Method: {prefs['Brew Method']}, Strength: {prefs['Strength']}, Temperature: {prefs['Temperature']}"
            prompt = f"""You are a friendly barista. A customer described their coffee preferences as follows: {user_pref_summary}.
Write a short, warm, and engaging paragraph recommending them coffee based on these preferences."""

            with st.spinner("Brewing your personalized recommendation... 🍵"):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.session_state.gpt_message = response['choices'][0]['message']['content']
                except Exception as e:
                    st.error(f"An error occurred while contacting the AI service: {e}")

        st.markdown("---")
        st.subheader("Barista's Personalized Recommendation")
        st.success(st.session_state.gpt_message)

    else:
        st.warning("No exact matches found. Please try different preferences!")

    # Add Twitter share button
    share_url = "https://your-app-url.com"  # Replace with your actual app URL
    share_text = "I just found my perfect coffee at The Grind Theory! ☕✨ Try yours here: "
    twitter_url = f"https://twitter.com/intent/tweet?text={share_text}{share_url}&hashtags=CoffeeLovers,AI"
    
    st.markdown(f"""
        <div class="share-container">
            <a href="{twitter_url}" target="_blank" class="share-button">
                Share on Twitter 🐦
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # Add centered restart button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↺ Take the Quiz Again", use_container_width=True):
            st.session_state.preferences = {}
            st.session_state.gpt_message = ""
            st.session_state.step = 1
            st.rerun()

st.markdown("""
---
<div style='text-align: center; font-size:14px;'>
This app is powered by AI. No personal data is stored. 🚀
</div>
""", unsafe_allow_html=True)
