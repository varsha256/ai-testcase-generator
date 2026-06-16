import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Principal SDET AI Assistant",
    page_icon="🧪",
    layout="wide"
)

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

api_key = None

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# --------------------------------------------------
# UI Header
# --------------------------------------------------

st.title("🧪 Principal SDET AI Assistant")

st.caption(
    "Generate enterprise-grade test cases, risk analysis, API coverage, "
    "security scenarios, and automation candidates."
)

# --------------------------------------------------
# Sample Requirements
# --------------------------------------------------

examples = {
    "FinTech - Customer Onboarding": """
As a new customer,

I want to register my account using my mobile number and OTP verification,

So that I can access the fintech application securely.

Acceptance Criteria:

1. User should be able to enter a valid mobile number.
2. OTP should be be sent successfully.
3. User should be able to verify OTP.
4. Invalid OTP should display an error.
5. Expired OTP should display an error.
6. User should be able to resend OTP.
7. User profile should be created after successful verification.
8. User should be redirected to dashboard.
""",

    "Ride Hailing - Ride Booking": """
As a rider,

I want to book a ride from my current location to a destination,

So that I can travel conveniently.

Acceptance Criteria:

1. User should select pickup location.
2. User should select destination.
3. Available ride options should be displayed.
4. Fare estimate should be displayed.
5. User should be able to confirm booking.
6. Driver should be assigned.
7. Booking confirmation should be shown.
""",

    "Ecommerce - Product Search": """
As a customer,

I want to search products using keywords,

So that I can find products quickly.

Acceptance Criteria:

1. User enters search keyword.
2. Matching products are displayed.
3. Search supports partial matching.
4. Search results display name, price and rating.
5. Empty state is shown when no results are found.
"""
}

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("AI QA Assistant")

selected_example = st.sidebar.selectbox(
    "Try Sample Requirement",
    list(examples.keys())
)

if st.sidebar.button("Load Example"):
    st.session_state["story"] = examples[selected_example]

# --------------------------------------------------
# Domain Selection
# --------------------------------------------------

domain = st.selectbox(
    "Select Domain",
    [
        "Generic",
        "FinTech",
        "Banking",
        "Ecommerce",
        "Ride Hailing",
        "Food Delivery"
    ]
)

# --------------------------------------------------
# Requirement Input
# --------------------------------------------------

story = st.text_area(
    "Enter User Story / Requirement",
    value=st.session_state.get("story", ""),
    height=300
)

expert_mode = st.checkbox(
    "Principal SDET Review Mode",
    value=True
)

# --------------------------------------------------
# System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are a Principal Software Development Engineer in Test (SDET)
with 15+ years of experience.

Your expertise includes:

- Functional Testing
- API Testing
- Mobile Testing
- Web Testing
- Security Testing
- Performance Testing
- Database Testing
- Integration Testing
- Distributed Systems Testing
- Test Automation

For every requirement:

1. Analyze business intent.
2. Identify hidden requirements.
3. Identify risks.
4. Generate comprehensive test coverage.
5. Think like a release sign-off reviewer.

Always generate practical production-grade test scenarios.

Focus on real-world risks, edge cases and failure scenarios.
"""

# --------------------------------------------------
# Domain Context
# --------------------------------------------------

DOMAIN_CONTEXT = {
    "FinTech": """
Focus on:
- OTP validation
- KYC
- Fraud prevention
- AML compliance
- Payment integrity
- Account security
""",

    "Banking": """
Focus on:
- Fund transfer
- Beneficiary validation
- Transaction limits
- Regulatory compliance
- Transaction integrity
""",

    "Ecommerce": """
Focus on:
- Search relevance
- Inventory consistency
- Checkout
- Promotions
- Refunds
""",

    "Ride Hailing": """
Focus on:
- GPS accuracy
- Driver assignment
- Fare calculation
- Trip cancellation
- Network failures
""",

    "Food Delivery": """
Focus on:
- Restaurant availability
- Menu consistency
- Cart validation
- Checkout
- Delivery tracking
""",

    "Generic": ""
}

# --------------------------------------------------
# Generate
# --------------------------------------------------

if st.button("Generate Test Cases"):

    if not story.strip():
        st.warning("Please enter a requirement.")
        st.stop()

    prompt = f"""
Requirement:

{story}

Domain:

{domain}

Additional Domain Guidance:

{DOMAIN_CONTEXT[domain]}

Generate:

1. Requirement Analysis
   - Business Intent
   - Key User Flows
   - Critical Risks

2. Assumptions

3. Functional Test Cases

4. Negative Test Cases

5. Boundary Test Cases

6. API Test Cases

7. Security Test Cases

8. Performance Test Scenarios

9. Automation Candidate Scenarios

10. Risk Areas

For all test cases use the format:

| Test ID | Scenario | Preconditions | Test Steps | Expected Result | Priority |

Priority:
P0 = Critical
P1 = High
P2 = Medium
P3 = Low

Requirements:

- Generate production-grade scenarios.
- Include UI and backend validation.
- Include data validation.
- Include concurrency scenarios.
- Include failure recovery scenarios.
- Avoid duplicates.
- Maximize risk coverage.
"""

    if expert_mode:
        prompt += """

Before generating test cases:

Review the requirement as a Principal SDET and provide:

1. Missing Acceptance Criteria
2. Ambiguous Requirements
3. Testability Concerns
4. Security Concerns
5. Scalability Concerns
6. Recommendations for Product Team

Then generate the complete test suite.
"""

    try:

        with st.spinner("Generating enterprise-grade test cases..."):

            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error: {str(e)}")