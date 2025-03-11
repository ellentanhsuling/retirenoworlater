import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

def calculate_retirement(api_key, user_data):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    Based on the following financial information, estimate the retirement age and provide brief financial advice:
    - Current Age: {user_data['age']}
    - Monthly Income: ${user_data['monthly_income']}
    - Monthly Expenses: ${user_data['monthly_expenses']}
    - Current Savings: ${user_data['current_savings']}
    - Monthly Savings: ${user_data['monthly_savings']}
    - Expense Categories: {user_data['expense_categories']}
    - Financial Habits: {user_data['financial_habits']}
    
    Provide the response in JSON format with exactly these keys:
    - estimated_retirement_age
    - monthly_savings_needed
    - recommendations
    """
    
    response = model.generate_content(prompt)
    return json.loads(response.text)

def main():
    st.title("AI Retirement Planning Assistant")
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Enter Your Gemini API Key")
        api_key = st.text_input("Gemini API Key", type="password")
        
        # Show example output
        st.subheader("Example Output Preview")
        example_output = {
            "estimated_retirement_age": 65,
            "monthly_savings_needed": 2500,
            "recommendations": [
                "Increase your emergency fund",
                "Diversify your investment portfolio",
                "Reduce discretionary spending"
            ]
        }
        st.info("Your results will look like this:")
        st.json(example_output)
    
    with col2:
        st.subheader("Enter Your Financial Information")
        age = st.number_input("Current Age", min_value=18, max_value=80, value=30)
        monthly_income = st.number_input("Monthly Income ($)", min_value=0, value=5000)
        current_savings = st.number_input("Current Savings ($)", min_value=0, value=10000)
        monthly_savings = st.number_input("Current Monthly Savings ($)", min_value=0, value=1000)
        monthly_expenses = st.number_input("Total Monthly Expenses ($)", min_value=0, value=3000)
    
    # Expense categories in expandable section
    with st.expander("Expense Categories", expanded=False):
        expense_categories = {}
        categories = ['Housing', 'Transportation', 'Food', 'Healthcare', 'Entertainment', 'Others']
        
        for category in categories:
            expense_categories[category] = st.slider(
                f"{category} (% of monthly expenses)",
                min_value=0,
                max_value=100,
                value=round(100/len(categories))
            )
    
    # Financial habits in expandable section
    with st.expander("Financial Habits", expanded=False):
        habits = st.multiselect(
            "Select your financial habits",
            [
                "Regular budgeting",
                "Impulse buying",
                "Investment in stocks",
                "Investment in real estate",
                "Credit card debt",
                "Emergency fund maintenance",
                "Regular financial review"
            ]
        )
    
    if api_key and st.button("Calculate Retirement Age"):
        user_data = {
            "age": age,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "current_savings": current_savings,
            "monthly_savings": monthly_savings,
            "expense_categories": expense_categories,
            "financial_habits": habits
        }
        
        with st.spinner("Analyzing your financial situation..."):
            try:
                result = calculate_retirement(api_key, user_data)
                
                st.success("Analysis Complete!")
                st.subheader("Results")
                st.write(f"Estimated Retirement Age: {result['estimated_retirement_age']}")
                st.write(f"Recommended Monthly Savings: ${result['monthly_savings_needed']}")
                
                st.subheader("Recommendations")
                for idx, recommendation in enumerate(result['recommendations'], 1):
                    st.write(f"{idx}. {recommendation}")
            except Exception as e:
                st.error("Please check your API key and try again.")

if __name__ == "__main__":
    main()
