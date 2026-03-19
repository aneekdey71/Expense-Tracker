import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ======================================================
# SESSION DATA (NO FILES)
# ======================================================
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=["Date", "Category", "Amount", "Note"]
    )

df = st.session_state.expenses

# ======================================================
# TITLE
# ======================================================
st.title("💰 Expense Tracker Dashboard")

# ======================================================
# ADD EXPENSE
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

        st.session_state.expenses = pd.concat(
            [df, new_row], ignore_index=True
        )

        st.success("Expense added successfully ✅")
        st.rerun()

    else:
        st.error("Amount must be greater than 0 ⚠️")

df = st.session_state.expenses

# ======================================================
# METRICS
# ======================================================
total_spent = df["Amount"].sum()

today_spent = (
    df[df["Date"].dt.date == date.today()]["Amount"].sum()
    if not df.empty else 0
)

col1, col2, col3 = st.columns(3)

col1.metric("💸 Total Spent", f"₹{total_spent:,.2f}")
col2.metric("📅 Today", f"₹{today_spent:,.2f}")
col3.metric("🧾 Entries", len(df))

# ======================================================
# TABLE
# ======================================================
st.subheader("📋 Expense History")

if not df.empty:
    st.dataframe(
        df.sort_values("Date", ascending=False),
        use_container_width=True
    )
else:
    st.info("No expenses yet — add one 👆")

# ======================================================
# CHARTS
# ======================================================
if not df.empty:

    st.subheader("📊 Spending Insights")

    colA, colB = st.columns(2)

    # Pie Chart
    with colA:
        cat_data = df.groupby("Category")["Amount"].sum()

        fig1, ax1 = plt.subplots()
        ax1.pie(cat_data, labels=cat_data.index,
                autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

    # Bar Chart
    with colB:
        fig2, ax2 = plt.subplots()
        cat_data.sort_values().plot(kind="barh", ax=ax2)
        ax2.set_xlabel("Amount (₹)")
        st.pyplot(fig2)

# ======================================================
# CHATBOT
# ======================================================
st.subheader("🤖 Smart Expense Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask about your expenses...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    text = user_input.lower()

    if df.empty:
        reply = "⚠️ Add expenses first."

    elif "total" in text:
        reply = f"You spent ₹{total_spent:,.2f} 💸"

    elif "today" in text:
        reply = f"Today's spending: ₹{today_spent:,.2f} 📅"

    elif "biggest" in text:
        max_row = df.loc[df["Amount"].idxmax()]
        reply = (
            f"Biggest expense: ₹{max_row['Amount']} "
            f"on {max_row['Category']} 💣"
        )

    else:
        reply = "Ask about total, today, or biggest expense 🤖"

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()

# ======================================================
# CLEAR DATA
# ======================================================
st.subheader("⚠️ Clear All Data")

if st.button("Clear All Expenses"):
    st.session_state.expenses = pd.DataFrame(
        columns=["Date", "Category", "Amount", "Note"]
    )
    st.success("All data cleared ✅")
    st.rerun()