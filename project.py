import streamlit as st
import pandas as pd
import os
import requests
import random
from streamlit_lottie import st_lottie
from streamlit_globe import streamlit_globe
# ---------------- CONFIG ----------------
st.set_page_config(page_title="EcoTrack AI", layout="wide")
def load_lottie(url):
    r = requests.get(url)
    return r.json()
lottie_hand = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")

st.sidebar.title("🌱 EcoTrack AI")
st.sidebar.image(
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
    use_container_width=True
)
tips = ["🌳 Plant Trees", "🚲 Use Cycle", "💡 Save Electricity", "🚍 Use Public Transport"]
st.sidebar.success(random.choice(tips))
st.sidebar.info("Reduce CO₂ 🌍")
st.sidebar.warning("Save Earth ♻️")

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Signup", "Solution", "Nagar Nigam", "Location",  "Eco Products", "Problems"]
)
# ---------- BACKGROUND IMAGE ----------
def banner(img):
    st.image(img, use_container_width=True)
    st.markdown("##")

# ---------- COMMON PROBLEMS FUNCTION ----------
def carbon_problems():
    st.subheader("⚠️ Carbon Emission Problems")
    st.markdown("""
    *Humans:* Respiratory issues, asthma, cardiovascular diseases, heat stress  
    *Animals & Birds:* Habitat loss, food scarcity, migration disruption, population decline  
    *Climate:* Global warming, heatwaves, droughts, floods, extreme weather events  
    *Environment:* Air & water pollution, melting glaciers, loss of biodiversity
    """)

# ---------- SIGNUP ----------
if menu == "Signup":
    banner("https://images.unsplash.com/photo-1521737604893-d14cc237f11d")
    st.subheader("Create Account")
    carbon_problems()
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Signup"):
        if os.path.exists("users.csv"):
            df = pd.read_csv("users.csv")
        else:
            df = pd.DataFrame(columns=["username", "password"])
        if new_user in df["username"].values:
            st.error("User already exists")
        else:
            df = pd.concat(
                [df, pd.DataFrame([[new_user, new_pass]], columns=["username", "password"])],
                ignore_index=True,
            )
            df.to_csv("users.csv", index=False)
            st.success("Account created!")
# ---------- LOGIN ----------
if menu == "Login":
    bg_image_url = "https://images.unsplash.com/photo-1532619187601-3c81b7d3e1d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80"
    st.markdown(
        f"""
        <div style="
            background-image: url('{bg_image_url}');
            background-size: cover;
            background-position: center;
            padding: 100px;
            border-radius: 10px;
            position: relative;
        ">
            <div style="
                background-color: rgba(0,0,0,0.6);
                padding: 40px;
                border-radius: 10px;
            ">
                <h1 style='text-align:center; color:white;'>🌿Track carbon, Track control , Save the future ,</h1>
                <p style='text-align:center; color:white; font-size:18px;'>
                    Carbon emissions affect humans, birds, and our planet. Login to track your impact.
                </p>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if os.path.exists("users.csv"):
            df = pd.read_csv("users.csv")
            if ((df["username"] == username) & (df["password"] == password)).any():
                st.session_state["user"] = username
                st.success(f"Welcome {username} 🎉")
            else:
                st.error("Invalid login")

    st.markdown("</div></div>", unsafe_allow_html=True)
# ---------- HOME AFTER LOGIN ----------
if "user" in st.session_state and menu == "Login":
    
    st.write(f"👤 Logged in as: {st.session_state['user']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=200)
        
    with col2:
        st_lottie(lottie_hand, height=150)
        
        distance = st.number_input("Distance (km)", min_value=0.0)
        transport = st.selectbox("Transport", ["Car", "Bus", "Bike"])
        electricity = st.number_input("Electricity units", min_value=0.0)
        food = st.selectbox("Food", ["Veg", "Non-Veg"])

#---------------CO2 CALCULATION--------------
co2 = 0
    if transport == "Car":
        co2 += distance * 0.21
    elif transport == "Bus":
        co2 += distance * 0.1
    else:
        co2 += distance * 0.05
    co2 += electricity * 0.5
    co2 += 2 if food == "Non-Veg" else 1
    st.subheader(f"🌍 CO₂ Emission: {co2:.2f} kg/day")

#-----------SAVE DATA-----------
if st.button("Save Data"):
        user = st.session_state["user"]
        new_data = pd.DataFrame([{"user": user, "co2": co2}])
        if os.path.exists("data.csv"):
            old = pd.read_csv("data.csv")
            df = pd.concat([old, new_data])
        else:
            df = new_data
        df.to_csv("data.csv", index=False)
        st.success("Saved!")


    #------------DASHBOARD--------
    st.subheader("📊 Dashboard")

    if os.path.exists("data.csv"):
        df = pd.read_csv("data.csv")
        user_data = df[df["user"] == st.session_state["user"]]
        
        if not user_data.empty:
            st.line_chart(user_data["co2"])
        else:
            st.info("No data yet")
    else:
        st.info("No data file found")


# ---------- SOLUTION ----------
if menu == "Solution":
    banner("https://images.unsplash.com/photo-1470770841072-f978cf4d019e")
    st.title("🌍 Eco Solutions & Impact")
    carbon_problems()
    st.info("Without action, carbon emissions can cause:")
    st.markdown("""
    - Heatwaves & droughts 🌞
    - Flooding & storms 🌊
    - Species extinction 🐦🐘
    """)
    streamlit_globe(pointsData=[{"lat":20.59,"lng":78.96}],
                    labelsData=[{"lat":20.59,"lng":78.96,"text":"India"}])
    st.success("🌳 Plant trees, reduce CO₂")
    st.success("🚶 Walk more, avoid vehicles")
    st.success("💡 Save electricity")

#--------- NAGAR NIGAM ----------
if menu == "Nagar Nigam":
    banner("https://images.unsplash.com/photo-1503387762-592deb58ef4e")
    st.title("🏢 Nagar Nigam & Carbon Threats")
    carbon_problems()
    st.success("📞 Contact: +91 9876543210")
    st.success("🚨 Emergency: 112")
    issue = st.text_area("Report Issue")
    if st.button("Submit"):
        st.success("Complaint submitted!")
    
#---------- LOCATION ----------
if menu == "Location":
    st.title("📍 India Carbon Map & Risks")
    carbon_problems()

    data = [
{"State":"Maharashtra","CO2":18,"lat":19.07,"lon":72.87,"level":"High"},
{"State":"Delhi","CO2":15,"lat":28.70,"lon":77.10,"level":"High"},
{"State":"Gujarat","CO2":14,"lat":22.25,"lon":71.19,"level":"High"},
{"State":"Uttar Pradesh","CO2":16,"lat":26.85,"lon":80.94,"level":"High"},
{"State":"Tamil Nadu","CO2":14,"lat":11.00,"lon":78.00,"level":"High"},
{"State":"West Bengal","CO2":13,"lat":22.57,"lon":88.36,"level":"High"},
{"State":"Karnataka","CO2":10,"lat":15.31,"lon":75.12,"level":"Medium"},
{"State":"Rajasthan","CO2":11,"lat":27.02,"lon":74.22,"level":"Medium"},
{"State":"Andhra Pradesh","CO2":10,"lat":15.91,"lon":79.74,"level":"Medium"},
{"State":"Telangana","CO2":10,"lat":17.41,"lon":78.47,"level":"Medium"},
{"State":"Madhya Pradesh","CO2":11,"lat":23.30,"lon":77.41,"level":"Medium"},
{"State":"Punjab","CO2":10,"lat":30.90,"lon":75.85,"level":"Medium"},
{"State":"Haryana","CO2":10,"lat":29.06,"lon":76.08,"level":"Medium"},
{"State":"Kerala","CO2":6,"lat":10.85,"lon":76.27,"level":"Low"},
{"State":"Bihar","CO2":7,"lat":25.61,"lon":85.13,"level":"Low"},
{"State":"Odisha","CO2":11,"lat":20.95,"lon":85.98,"level":"Medium"},
{"State":"Chhattisgarh","CO2":10,"lat":21.25,"lon":81.63,"level":"Medium"},
{"State":"Assam","CO2":6,"lat":26.20,"lon":92.79,"level":"Low"},
{"State":"Himachal Pradesh","CO2":5,"lat":31.10,"lon":77.16,"level":"Low"},
{"State":"Uttarakhand","CO2":5,"lat":30.06,"lon":79.10,"level":"Low"},
{"State":"Jammu & Kashmir","CO2":4,"lat":33.77,"lon":76.55,"level":"Low"},
{"State":"Goa","CO2":4,"lat":15.48,"lon":73.83,"level":"Low"},
{"State":"Sikkim","CO2":2,"lat":27.33,"lon":88.62,"level":"Very Low"},
{"State":"Tripura","CO2":2,"lat":23.83,"lon":91.28,"level":"Very Low"},
{"State":"Manipur","CO2":2,"lat":24.82,"lon":93.95,"level":"Very Low"},
{"State":"Nagaland","CO2":2,"lat":26.15,"lon":94.56,"level":"Very Low"},
{"State":"Mizoram","CO2":1,"lat":23.16,"lon":92.83,"level":"Very Low"},
{"State":"Arunachal Pradesh","CO2":1,"lat":28.21,"lon":94.41,"level":"Very Low"},
{"State":"Meghalaya","CO2":2,"lat":25.57,"lon":91.88,"level":"Very Low"},
{"State":"Ladakh","CO2":1,"lat":34.15,"lon":77.57,"level":"Very Low"},
{"State":"Chandigarh","CO2":5,"lat":30.73,"lon":76.78,"level":"Medium"},
{"State":"Puducherry","CO2":2,"lat":11.93,"lon":79.83,"level":"Low"},
{"State":"Andaman & Nicobar","CO2":1,"lat":11.67,"lon":92.73,"level":"Very Low"},
{"State":"Daman & Diu","CO2":2,"lat":20.42,"lon":72.83,"level":"Low"},
{"State":"Lakshadweep","CO2":1,"lat":10.57,"lon":72.64,"level":"Very Low"},
{"State":"Jharkhand","CO2":3,"lat":23.33,"lon":85.33,"level":"Low"}
]

df = pd.DataFrame(data)
st.map(df.rename(columns={"lat":"latitude","lon":"longitude"}))

def level_color(level):
    if level == "High":
        return "🔴"
    elif level == "Medium":
        return "🟠"
    elif level == "Low":
        return "🟢"
    else:
        return "🟡"  # Very Low

df["Level"] = df["level"].apply(level_color)
st.dataframe(df[["State","CO2","Level"]])

state = st.selectbox("Select State", df["State"])
row = df[df["State"] == state].iloc[0]

if row["level"] == "High":
    st.error(f"🚨 {state} HIGH EMISSION")
    st.markdown("""
    *Risks:* 
    - Humans: High respiratory & cardiovascular risk  
    - Wildlife: Habitat loss & stress  
    - Climate: Extreme weather events  
    - Reports: Pollution alerts, migration disruptions
    """)
elif row["level"] == "Medium":
    st.warning(f"⚠️ {state} Medium Emission")
    st.markdown("""
    *Risks:* 
    - Humans: Moderate pollution, asthma  
    - Wildlife: Migration disruption  
    - Climate: Rising temperature  
    - Reports: Localized air pollution
    """)
else:
    st.success(f"✅ {state} Low Emission")
    st.markdown("""
    *Risks:* 
    - Humans: Lower health risk  
    - Wildlife: Safer habitats  
    - Climate: Stable conditions  
    - Reports: Normal air quality
    """)



#---------- ECO PRODUCTS ----------
if menu == "Eco Products":
    banner("https://images.unsplash.com/photo-1469474968028-56623f02e42e")
    st.title("🌱 Eco Products & Carbon Reduction")
    
    product = st.selectbox(
        "Choose Product",
        ["Toothbrush", "Water Bottle", "Shopping Bag", "Cleaning Product", "Straws"]
    )
    col1, col2 = st.columns(2)
    if product == "Toothbrush":
        with col1: st.error("❌ Plastic")
        with col2: st.success("✅ Bamboo")
        st.metric("Carbon Saving", "80%")
    elif product == "Water Bottle":
        with col1: st.error("❌ Plastic")
        with col2: st.success("✅ Steel")
        st.metric("Carbon Saving", "90%")
    elif product == "Shopping Bag":
        with col1: st.error("❌ Plastic")
        with col2: st.success("✅ Cloth")
        st.metric("Carbon Saving", "85%")
    elif product == "Cleaning Product":
        with col1: st.error("❌ Chemical")
        with col2: st.success("✅ Eco")
        st.metric("Carbon Saving", "70%")
    elif product == "Straws":
        with col1: st.error("❌ Plastic")
        with col2: st.success("✅ Steel")
        st.metric("Carbon Saving", "95%")
 st.markdown("""
    *Why it matters:*  
    Reducing plastic & chemical usage prevents:
    - Pollution of rivers & oceans 🐠  
    - CO₂ release from manufacturing 🏭  
    - Wildlife ingestion of plastic 🐦  
    - Climate & health improvements
    """)
# ---------- PROBLEMS ----------
if menu == "Problems":
    st.title("⚠️ Carbon Emission Problems & Life Impact")
    banner("https://images.unsplash.com/photo-1506744038136-46273834b3fb")
    st.markdown("""
    Carbon emissions affect every aspect of life. Understanding these problems helps us take action.
    """)
problems_data = [
        {"Category": "Humans", 
         "Impact": "Respiratory issues, asthma, cardiovascular diseases, heat stress, premature deaths"},
        {"Category": "Animals & Birds", 
         "Impact": "Habitat loss, food scarcity, migration disruption, population decline, extinction"},
        {"Category": "Climate", 
         "Impact": "Global warming, heatwaves, droughts, floods, extreme weather events"},
        {"Category": "Environment", 
         "Impact": "Air & water pollution, melting glaciers, loss of biodiversity, soil degradation"},
        {"Category": "Economy", 
         "Impact": "Crop loss, energy costs, disaster damages, healthcare burden"}
    ]
df_problems = pd.DataFrame(problems_data)
st.dataframe(df_problems, use_container_width=True)

for row in problems_data:
    if row["Category"] == "Humans":
        st.error(f"👤 Humans: {row['Impact']}")
    elif row["Category"] == "Animals & Birds":
        st.warning(f"🐦 Wildlife: {row['Impact']}")
    elif row["Category"] == "Climate":
        st.info(f"🌡 Climate: {row['Impact']}")
    elif row["Category"] == "Environment":
        st.success(f"🌿 Environment: {row['Impact']}")
    elif row["Category"] == "Economy":
        st.markdown(f"💰 Economy: {row['Impact']}")
st.markdown("""
*Takeaway:*  
Every kg of CO₂ saved improves health, protects wildlife, and stabilizes climate.  
🌱 Reduce, Reuse, Recycle, and Switch to Eco-friendly products!
""")

# ---------- FOOTER ----------
st.write("🌿 EcoTrack AI | Final Version 🚀")
