import streamlit as st
import re


# ---------- EMAIL VALIDATION ----------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


# ---------- CONTACT FORM DIALOG ----------
@st.dialog("📩 Contact Me")
def contact_form():

    with st.form("Contact form"):
        name = st.text_input("First name")
        email = st.text_input("Email Address")
        message = st.text_area("Your message")

        submit_button = st.form_submit_button("Submit")

        if submit_button:

            if not name or not email or not message:
                st.error("Please fill all fields ⚠️")

            elif not is_valid_email(email):
                st.error("Please enter a valid email address 📧")

            else:
                st.success("Your message has been submitted successfully ✅")


# ---------- HERO SECTION ----------
col1, col2 = st.columns(2, gap='small', vertical_alignment='center')

with col1:
    st.image("./assets/my image.jpeg", width=250)

with col2:
    st.title("Aneek Dey", anchor=False)

    st.write(
        "B.Tech CSE (AI & ML) Student @ Cambridge Institute of Technology, "
        "North Campus | Aspiring AI/ML Engineer | Skilled in Python | "
        "NumPy & Pandas | Passionate About Innovation & Emerging Tech | Fresher"
    )

    if st.button("📩 Contact Me", type="primary"):
        contact_form()
    
    

#----SKILLS----

st.write("\n")
st.subheader("🚀 Core Technical Skills")
st.write("""
    
• Python Programming
         
• Data Analysis (NumPy, Pandas)
         
• Data Visualization (Matplotlib)
         
• Interactive Web Apps with Streamlit
         
• Problem Solving & Logical Thinking
         
• Basic DBMS Knowledge
"""
)
st.write("\n")
st.subheader("🧠 Personal Strengths")
st.write("""
    
• Fast Learner
         
• Self-Driven & Consistent
         
• Strong Work Ethic
         
• Attention to Detail
         
• Passion for Technology
         
• Growth Mindset
"""
)



    
