import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

# ======================================================
# CONFIG
# ======================================================
st.set_page_config(
    page_title="Expense Tracker Pro",
    page_icon="💰",
    layout="wide"
)

DATA_FILE = "expenses.csv"

# ======================================================
# LOAD DATA
# ======================================================
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
    else:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
    return df

df = load_data()

# ======================================================
# TITLE
# ======================================================
st.title("💰 Expense Tracker Dashboard")

# ======================================================
# ADD EXPENSE FORM
# ======================================================
st.subheader("➕ Add New Expense")

with st.form("expense_form", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        expense_date = st.date_input("Date", date.today())
        category = st.selectbox(
            "Category",
            ["Food", "Transport", "Shopping", "Bills",
             "Entertainment", "Health", "Other"]
        )

    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
        note = st.text_input("Note (optional)")

    add_btn = st.form_submit_button("Add Expense")

if add_btn:
    if amount > 0:

        new_row = pd.DataFrame({
            "Date": [pd.to_datetime(expense_date)],
            "Category": [category],
            "Amount": [amount],
            "Note": [note]
        })

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success("Expense added successfully ✅")
        df = load_data()

    else:
        st.error("Amount must be greater than 0 ⚠️")

# ======================================================
# METRICS
# ======================================================
total_spent = df["Amount"].sum()
today_spent = df[df["Date"].dt.date == date.today()]["Amount"].sum() if not df.empty else 0

col1, col2, col3 = st.columns(3)

col1.metric("💸 Total Spent", f"₹{total_spent:,.2f}")
col2.metric("📅 Today", f"₹{today_spent:,.2f}")
col3.metric("🧾 Total Entries", len(df))

# ======================================================
# TABLE
# ======================================================
st.subheader("📋 Expense History")

if not df.empty:
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
else:
    st.info("No expenses yet — start by adding one 👆")

# ======================================================
# CHARTS (PROFESSIONAL)
# ======================================================
if not df.empty:

    st.subheader("📊 Spending Insights")

    colA, colB = st.columns(2)

    # Pie Chart
    with colA:
        cat_data = df.groupby("Category")["Amount"].sum()

        fig1, ax1 = plt.subplots()
        ax1.pie(cat_data, labels=cat_data.index, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

    # Category Bar Chart
    with colB:
        fig2, ax2 = plt.subplots()
        cat_data.sort_values().plot(kind="barh", ax=ax2)
        ax2.set_xlabel("Amount (₹)")
        st.pyplot(fig2)

    # Monthly Spending
    st.subheader("📅 Monthly Spending")

    df["Month"] = df["Date"].dt.to_period("M")
    monthly = df.groupby("Month")["Amount"].sum()

    fig3, ax3 = plt.subplots()
    monthly.plot(kind="bar", ax=ax3)

    ax3.set_xlabel("Month")
    ax3.set_ylabel("Amount (₹)")
    st.pyplot(fig3)

# ======================================================
# CHATBOT
# ======================================================
st.subheader("🤖 Smart Expense Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask about your expenses...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    text = user_input.lower()

    # ❌ No data case
    if df.empty:
        reply = (
            "⚠️ I don’t have any expense data yet.\n\n"
            "👉 Please add some expenses first using the tracker above "
            "to get meaningful insights 💡"
        )

    else:
        # ---------- TOTAL ----------
        if "total" in text:
            reply = f"You have spent ₹{total_spent:,.2f} in total 💸"

        # ---------- TODAY ----------
        elif "today" in text:
            reply = f"Today's spending is ₹{today_spent:,.2f} 📅"

        # ---------- MONTH ----------
        elif "month" in text:
            this_month = df[df["Date"].dt.month == date.today().month]["Amount"].sum()
            reply = f"This month's spending: ₹{this_month:,.2f} 📊"

        # ---------- CATEGORY ----------
        elif "food" in text:
            food_total = df[df["Category"] == "Food"]["Amount"].sum()
            reply = f"You spent ₹{food_total:,.2f} on Food 🍔"

        # ---------- BIGGEST ----------
        elif "biggest" in text or "highest" in text:
            max_row = df.loc[df["Amount"].idxmax()]
            reply = (
                f"Your biggest expense was ₹{max_row['Amount']:,.2f} "
                f"on {max_row['Category']} 💣"
            )

        # ---------- AVERAGE ----------
        elif "average" in text:
            days = (df["Date"].max() - df["Date"].min()).days + 1
            avg = total_spent / days if days > 0 else 0
            reply = f"Your average daily spend is ₹{avg:,.2f} 📊"

        # ---------- DEFAULT ----------
        else:
            reply = (
                "I can help with:\n"
                "• Total spending\n"
                "• Today's spending\n"
                "• Monthly spending\n"
                "• Category spending\n"
                "• Biggest expense\n"
                "• Average spending 🤖"
            )

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()

# ======================================================
# DELETE OPTION
# ======================================================
st.subheader("⚠️ Clear All Data")

if st.button("Delete All Expenses"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    st.success("All data deleted successfully ✅")
    st.rerun()