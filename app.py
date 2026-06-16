import os
import base64
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

# --------------------------------------------------
# Page Configurations & Theme Baseline
# --------------------------------------------------
st.set_page_config(
    page_title="QA Stack AI Test Architect",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# Premium SaaS Style Injection
st.markdown("""
<style>
    /* Global Background & Typography Tuning */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    
    /* Premium Metric & Feature Container Card */
    .premium-card {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .premium-card h2 {
        color: #F3F4F6;
        font-weight: 600;
        font-size: 1.5rem;
        margin-bottom: 12px;
    }
    
    /* Sleek Title & Subtitle Treatments */
    .hero-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #FFFFFF, #9CA3AF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -10px;
    }
    .hero-subtitle {
        text-align: center;
        color: #9CA3AF;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    /* Telemetry / Metric Indicators */
    .telemetry-box {
        background: #111827;
        border-left: 4px solid #4F46E5;
        padding: 12px 20px;
        border-radius: 6px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Core Domain Knowledge & Sample Requirements
# --------------------------------------------------
examples = {
    "FinTech - Customer Onboarding": """As a new customer,

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
8. User should be redirected to dashboard.""",

    "Ride Hailing - Ride Booking": """As a rider,

I want to book a ride from my current location to a destination,

So that I can travel conveniently.

Acceptance Criteria:

1. User should select pickup location.
2. User should select destination.
3. Available ride options should be displayed.
4. Fare estimate should be displayed.
5. User should be able to confirm booking.
6. Driver should be assigned.
7. Booking confirmation should be shown.""",

    "Ecommerce - Product Search": """As a customer,

I want to search products using keywords,

So that I can find products quickly.

Acceptance Criteria:

1. User enters search keyword.
2. Matching products are displayed.
3. Search supports partial matching.
4. Search results display name, price and rating.
5. Empty state is shown when no results are found."""
}

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
# Infrastructure & Client Verification (Safe Mode)
# --------------------------------------------------
load_dotenv()

if "request_count" not in st.session_state:
    st.session_state.request_count = 0
MAX_REQUESTS = 2

api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("🔒 Missing API Key: Please add GROQ_API_KEY to your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# --------------------------------------------------
# 1. HEADER HERO SECTION
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "qa_stack_logo.png")

if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f'<div style="display:flex;justify-content:center;margin-bottom:15px;">'
        f'<img src="data:image/png;base64,{encoded}" width="90"></div>',
        unsafe_allow_html=True
    )

st.markdown('<div class="hero-title">QA Stack AI Test Architect</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Principal SDET Copilot for Test Design, Risk Analysis and Release Sign-Off</div>', unsafe_allow_html=True)

# --------------------------------------------------
# 2. METRICS / TELEMETRY BAR
# --------------------------------------------------
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.markdown('<div class="telemetry-box"><small style="color:#9CA3AF">DOMAINS</small><br><b style="font-size:1.4rem;color:#FFF">5+ Engines</b></div>', unsafe_allow_html=True)
with m_col2:
    st.markdown('<div class="telemetry-box"><small style="color:#9CA3AF">COVERAGE MATRIX</small><br><b style="font-size:1.4rem;color:#FFF">10 Layers</b></div>', unsafe_allow_html=True)
with m_col3:
    st.markdown('<div class="telemetry-box"><small style="color:#9CA3AF">AI CORE</small><br><b style="font-size:1.4rem;color:#4F46E5">Llama 3.3 70B</b></div>', unsafe_allow_html=True)
with m_col4:
    remaining = MAX_REQUESTS - st.session_state.request_count
    st.markdown(f'<div class="telemetry-box"><small style="color:#9CA3AF">SESSION LIMIT</small><br><b style="font-size:1.4rem;color:#EF4444">{remaining} / {MAX_REQUESTS} Left</b></div>', unsafe_allow_html=True)

st.markdown("<br><hr style='border-color:#1F2937;'><br>", unsafe_allow_html=True)

# --------------------------------------------------
# 3. SPLIT WORKSPACE INTERFACE (Modern 2-Column SaaS Grid)
# --------------------------------------------------
left_workspace, right_workspace = st.columns([2, 3], gap="large")

# --- LEFT COLUMN: CONTROL & INPUT PANEL ---
with left_workspace:
    st.markdown("### 🎛️ Configuration & Controls")
    
    domain = st.selectbox(
        "Target System Domain Context",
        ["Generic", "FinTech", "Banking", "Ecommerce", "Ride Hailing", "Food Delivery"]
    )
    
    story = st.text_area(
        "User Story / Product Requirements Document (PRD)",
        value=st.session_state.get("story", ""),
        height=320,
        placeholder="Paste your agile user stories or raw features here..."
    )
    
    expert_mode = st.toggle("Enable Principal SDET Deep-Review Mode", value=True)
    
    generate_btn = st.button("🚀 Analyze & Generate Test Suite", use_container_width=True)

# --- RIGHT COLUMN: LIVING ARCHITECT OUTPUT ---
with right_workspace:
    st.markdown("### 📋 Test Architecture Output")
    
    if "last_output" not in st.session_state:
        st.session_state.last_output = None

    if not generate_btn and st.session_state.last_output is None:
        st.markdown(
            """
            <div style="border: 2px dashed #374151; border-radius: 8px; padding: 60px; text-align: center; color: #6B7280;">
                <h4>Awaiting Requirements Engine Input</h4>
                <p style="font-size:0.9rem;">Configure parameters on the left and click execute to assemble the structural test blueprint.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    if generate_btn:
        if st.session_state.request_count >= MAX_REQUESTS:
            st.error("Demo limit reached. Maximum 2 generations are allowed per session.")
        elif not story.strip():
            st.warning("Analysis engine aborted: Empty input text matrix provided.")
        else:
            with st.spinner("Generating enterprise-grade test cases..."):
                try:
                    prompt = f"""
Requirement:

{story}

Domain:

{domain}

Additional Domain Guidance:

{DOMAIN_CONTEXT.get(domain, '')}

Generate:

1. Requirement Analysis
   - Business Intent
   - Key User Flows
   - Critical Risks

2. Assumptions

3. Functional Test Cases (Generate at least 10 explicit test cases)

4. Negative Test Cases (Generate at least 10 explicit test cases)

5. Boundary Test Cases (Generate at least 10 explicit test cases)

6. API Test Cases (Generate at least 10 explicit test cases)

7. Security Test Cases (Generate at least 10 explicit test cases)

8. Performance Test Scenarios (Generate at least 10 explicit scenarios)

9. Automation Candidate Scenarios (Generate at least 10 explicit scenarios)

10. Risk Areas

CRITICAL RULE: You MUST write out at least 10 distinct, unique test cases or scenarios for each testing category requested above. Do not truncate, summarize, or skip lines.

For all test cases use the markdown table format:

| Test ID | Category | Scenario | Preconditions | Test Steps | Expected Result | Priority |

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

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.2,
                        max_tokens=2500
                    )
                    
                    st.session_state.last_output = response.choices[0].message.content
                    st.session_state.request_count += 1
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Render results with download functionality if output exists
    # Render results with dual-download functionality if output exists
    if st.session_state.last_output is not None:
        st.success("Analysis Complete.")
        
        # --------------------------------------------------
        # EXPORT TOOLBAR PANEL (Side-by-Side Dual Format)
        # --------------------------------------------------
        st.markdown("### 📥 Export Architecture Deliverables")
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            # Option 1: Full Markdown Document Download
            st.download_button(
                label="📄 Download Full Review (.MD)",
                data=st.session_state.last_output,
                file_name=f"qa_stack_review_{domain.lower()}.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with exp_col2:
            # Option 2: Extract and Build a Pure CSV Matrix Download
            raw_text = st.session_state.last_output
            csv_buffer = ""
            
            # Simple algorithmic extraction of markdown table lines to parse out text prose
            table_lines = [
                line.strip() for line in raw_text.split("\n") 
                if line.strip().startswith("|") and "---" not in line
            ]
            
            if table_lines:
                # Convert Markdown pipes to standard CSV comma rows
                csv_rows = []
                for line in table_lines:
                    # Clean out boundaries and change delimiters
                    cells = [cell.strip().replace(",", ";") for cell in line.split("|")[1:-1]]
                    csv_rows.append(",".join(cells))
                csv_buffer = "\n".join(csv_rows)
                
            if csv_buffer:
                st.download_button(
                    label="📊 Download Test Cases (.CSV)",
                    data=csv_buffer,
                    file_name=f"qa_stack_matrix_{domain.lower()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                # Disabled state fallback if no tables have completed generation yet
                st.button("📊 No Test Matrix Tables Found", disabled=True, use_container_width=True)

        st.markdown("<br><hr style='border-color:#1F2937;'><br>", unsafe_allow_html=True)
        
        # Display the live report layout downstream
        st.markdown("### 🛡️ Core Verification Strategy Matrix")
        st.markdown(st.session_state.last_output)
# --------------------------------------------------
# 4. SIDEBAR UTILITIES
# --------------------------------------------------
st.sidebar.markdown("🎯 Requirement Blueprints")
selected_example = st.sidebar.selectbox("Select PRD Blueprint", list(examples.keys()))
if st.sidebar.button("Load Blueprint into Editor", use_container_width=True):
    st.session_state["story"] = examples[selected_example]
    st.session_state.last_output = None  # Clear previous results context on shift
    st.rerun()
# --------------------------------------------------
# 6. GLOBAL MAIN WORKSPACE FOOTER
# --------------------------------------------------
# --------------------------------------------------
# 6. GLOBAL MAIN WORKSPACE FOOTER
# --------------------------------------------------
st.markdown("<br><br><br><hr style='border-color:#1F2937;'>", unsafe_allow_html=True)

footer_html = """
<div style="text-align: center; color: #6B7280; font-size: 0.85rem; padding-bottom: 20px;">
    <p style="margin-bottom: 12px;">
        Built with ⚡ by <span style="color: #4F46E5; font-weight: 600;">Varsha Yadav</span> | Staff SDET & Test Architect
    </p>
    <p style="margin-bottom: 12px; display: flex; justify-content: center; align-items: center; gap: 16px;">
        <span style="display: inline-flex; align-items: center; gap: 4px;">
            <span style="color: #0A66C2; font-size: 1rem; font-weight: bold;">in</span> 
            <a href="https://www.linkedin.com/in/varsha-yadav-1b63375a/" target="_blank" style="color: #9CA3AF; text-decoration: underline; font-weight: 500;">
                Connect on LinkedIn
            </a>
        </span>
        <span style="color: #374151;">|</span>
        <span style="display: inline-flex; align-items: center; gap: 4px;">
            <span style="color: #EF4444; font-size: 1rem;">▶</span> 
            <a href="https://www.youtube.com/@QAStack/videos" target="_blank" style="color: #9CA3AF; text-decoration: underline; font-weight: 500;">
                Watch on YouTube
            </a>
        </span>
    </p>
    <p>
        Have feedback or feature requests? Reach out at 
        <a href="mailto:varsha.y675423@gmail.com?subject=QA%20Stack%20Feedback" style="color: #9CA3AF; text-decoration: underline;">
            varsha.y675423@gmail.com
        </a>
    </p>
</div>
"""
