import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Personal Finance Manager", layout="wide")

st.title("💰 AI-Powered Personal Finance Management System")
st.markdown("Track your income, expenses, and get AI-driven spending insights.")

# Initialize session state for transactions
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Description"])

# Sidebar for adding transactions
st.sidebar.header("Add Transaction")
with st.sidebar.form("transaction_form"):
    t_date = st.date_input("Date")
    t_type = st.selectbox("Type", ["Income", "Expense"])
    t_category = st.selectbox("Category", ["Salary", "Food", "Rent", "Utilities", "Entertainment", "Other"])
    t_amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
    t_desc = st.text_input("Description")
    submitted = st.form_submit_button("Add Transaction")
    
    if submitted:
        new_row = {"Date": t_date, "Type": t_type, "Category": t_category, "Amount": t_amount, "Description": t_desc}
        st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Transaction added successfully!")

# Main Dashboard View
df = st.session_state.transactions

if not df.empty:
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    net_savings = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:.2f}")
    col2.metric("Total Expenses", f"${total_expense:.2f}")
    col3.metric("Net Savings", f"${net_savings:.2f}")

    st.subheader("Transaction History")
    st.dataframe(df, use_container_width=True)

    st.subheader("Expense Breakdown by Category")
    expense_df = df[df["Type"] == "Expense"]
    if not expense_df.empty:
        category_summary = expense_df.groupby("Category")["Amount"].sum()
        fig, ax = plt.subplots()
        category_summary.plot(kind="pie", autopct="%1.1f%%", ax=ax, startangle=90)
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.info("Add some expenses to see the category breakdown chart.")

    # AI Insights Section
    st.subheader("🤖 AI Financial Advisor Recommendations")
    if total_expense > total_income:
        st.warning("⚠️ **Alert:** Your expenses currently exceed your income. Consider cutting back on discretionary categories like Entertainment or Dining out.")
    elif total_income > 0 and (total_expense / total_income) > 0.7:
        st.info("💡 **Tip:** You are spending over 70% of your income. Try aiming for the 50/30/20 rule to boost your savings rate.")
    else:
        st.success("✨ **Great Job:** Your savings rate is healthy! Consider moving excess funds into an index fund or high-yield savings account.")
else:
    st.info("👈 Use the sidebar to add your first income or expense transaction to get started.")
