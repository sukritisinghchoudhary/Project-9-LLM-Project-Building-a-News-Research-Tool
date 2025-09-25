# ✅ Enhanced News Research Dashboard with Modern UI

import streamlit as st
import pandas as pd
from langchain_config import get_summary
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from datetime import datetime

# ⚙️ Setting up the app layout and title
st.set_page_config(
    page_title="AI News Research Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom CSS for modern dashboard styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main > div {
        padding-top: 2rem;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Login Container */
    .login-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 3rem;
        border-radius: 20px;
        max-width: 450px;
        margin: 2rem auto;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        color: white;
    }
    
    .login-container h3 {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Card Styles */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .summary-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .article-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border-left: 3px solid #4CAF50;
        transition: transform 0.2s ease;
    }
    
    .article-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .history-card {
        background: linear-gradient(135deg, #e3ffe7 0%, #d9e7ff 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Example Button Styles */
    .example-btn {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        color: #333;
        font-weight: 500;
        margin: 0.2rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .example-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 154, 158, 0.4);
    }
    
    /* Text Area Styles */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-family: 'Inter', sans-serif;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Stats Cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        flex: 1;
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-top: 4px solid;
    }
    
    .stat-card.queries {
        border-top-color: #4CAF50;
    }
    
    .stat-card.summaries {
        border-top-color: #2196F3;
    }
    
    .stat-card.articles {
        border-top-color: #FF9800;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Download Button Special Styling */
    .download-btn {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# 📊 Initialize session state for stats
if 'total_queries' not in st.session_state:
    st.session_state.total_queries = 0
if 'total_summaries' not in st.session_state:
    st.session_state.total_summaries = 0
if 'total_articles' not in st.session_state:
    st.session_state.total_articles = 0

# 📌 Enhanced User Authentication with modern UI
def handle_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("""
            <div class='login-container'>
                <h3>🔐 Welcome Back!</h3>
                <p style='text-align: center; margin-bottom: 2rem; opacity: 0.9;'>
                    Please login to access the AI News Research Dashboard
                </p>
                <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
                    <p style='margin: 0; font-size: 0.9rem;'>
                        <strong>Demo Credentials:</strong><br>
                        Username: <code>Sukriti</code><br>
                        Password: <code>Sukriti123</code>
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter username", key="username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password", key="password")
            
            if st.button("🚀 Login", use_container_width=True):
                if username == "Sukriti" and password == "Sukriti123":
                    st.session_state.authenticated = True
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        st.stop()

# 📈 Dashboard Stats Display
def show_dashboard_stats():
    st.markdown("""
        <div class='stats-container'>
            <div class='stat-card queries'>
                <div class='stat-number' style='color: #4CAF50;'>{}</div>
                <div class='stat-label'>Total Queries</div>
            </div>
            <div class='stat-card summaries'>
                <div class='stat-number' style='color: #2196F3;'>{}</div>
                <div class='stat-label'>Summaries Generated</div>
            </div>
            <div class='stat-card articles'>
                <div class='stat-number' style='color: #FF9800;'>{}</div>
                <div class='stat-label'>Articles Processed</div>
            </div>
        </div>
    """.format(
        st.session_state.total_queries,
        st.session_state.total_summaries,
        st.session_state.total_articles
    ), unsafe_allow_html=True)

# 📚 Enhanced History Display
def show_history():
    if 'history' in st.session_state and st.session_state.history:
        st.markdown("""
            <div style='margin-top: 2rem;'>
                <h3 style='text-align:center; color: #667eea; margin-bottom: 1rem;'>
                    📚 Recent Query History
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        for idx, (query, response) in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.markdown(f"""
                <div class='history-card'>
                    <h4 style='color: #333; margin-bottom: 0.5rem;'>
                        🔍 Query {idx}: {query}
                    </h4>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>
                        {response[:150]}{'...' if len(response) > 150 else ''}
                    </p>
                    <small style='color: #999;'>
                        📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}
                    </small>
                </div>
            """, unsafe_allow_html=True)

# ♻️ Enhanced Reset Function
def reset_all():
    preserved_keys = {'authenticated', 'total_queries', 'total_summaries', 'total_articles'}
    for key in list(st.session_state.keys()):
        if key not in preserved_keys:
            del st.session_state[key]
    st.session_state.query_input = ""
    st.success("🔄 Dashboard reset successfully!")
    st.rerun()

# 📄 Enhanced PDF Generation
def create_pdf(text_data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Add header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "AI News Research Summary")
    c.setFont("Helvetica", 10)
    c.drawString(72, height - 90, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add content
    textobject = c.beginText()
    textobject.setTextOrigin(72, height - 120)
    textobject.setFont("Helvetica", 11)
    
    wrap_width = 85
    for line in text_data.split("\n"):
        while len(line) > wrap_width:
            space_pos = line.rfind(' ', 0, wrap_width)
            if space_pos == -1:
                space_pos = wrap_width
            textobject.textLine(line[:space_pos])
            line = line[space_pos:].strip()
        textobject.textLine(line.strip())
    
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# 🧠 Enhanced Main Summary Generation Function
def generate_summary_and_output():
    # Main Header
    st.markdown("""
        <div class='main-header'>
            <h1>🤖 AI News Research Dashboard</h1>
            <p>Intelligent news analysis powered by advanced AI technology</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Stats
    show_dashboard_stats()
    
    # Example Queries Section
    st.markdown("""
        <div class='info-card'>
            <h4 style='color: #667eea; margin-bottom: 1rem;'>🎯 Quick Start Examples</h4>
            <p style='margin-bottom: 1rem; color: #666;'>
                Click any example below to auto-fill your query and get started instantly!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    examples = [
        "Explosive growth in AI technologies like AI video generators and agents",
        " India-Pakistan Tensions",
        " Israel-Iran Conflict Updates",
        " IPL 2025 Match Highlights"
    ]
    
    example_cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(example, use_container_width=True, key=f"example_{i}"):
                st.session_state.query_input = example.split(" ", 1)[1]  # Remove emoji

    # Query Input Section
    st.markdown("""
        <div style='margin-top: 2rem;'>
            <h4 style='text-align:center; color: #667eea; margin-bottom: 1rem;'>
                🔍 Enter Your Research Query
            </h4>
        </div>
    """, unsafe_allow_html=True)
    
    query = st.text_area(
        "", 
        key="query_input", 
        height=100, 
        label_visibility="collapsed",
        placeholder="Type your news research query here... (e.g., 'Latest developments in AI technology')"
    )

    # Action Buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        gen_btn = st.button("⚡ Generate AI Summary", use_container_width=True)
    with col2:
        reset_btn = st.button("🔄 Reset Dashboard", use_container_width=True)
    with col3:
        if st.button("📊 Refresh Stats", use_container_width=True):
            st.rerun()

    if reset_btn:
        reset_all()

    if gen_btn:
        if query:
            # Update query counter
            st.session_state.total_queries += 1
            
            # Show loading animation
            with st.spinner('🔄 AI is analyzing news articles...'):
                response, articles = get_summary(query)
                
            # Process response
            bullet_lines = [f"• {line.strip()}" for line in response.split("•") if line.strip()]
            header_line = articles[0].get("title", "Top News") if articles else (bullet_lines[0][1:].strip() if bullet_lines else "AI News Summary")
            formatted_summary = "\n".join(bullet_lines[1:]) if len(bullet_lines) > 1 else response
            
            # Update summary counter
            st.session_state.total_summaries += 1
            st.session_state.total_articles += len(articles) if articles else 0

            # Display Header
            st.markdown(f"""
                <div class='summary-card'>
                    <h3 style='margin: 0; color: #333; text-align: center;'>
                        📰 {header_line}
                    </h3>
                </div>
            """, unsafe_allow_html=True)

            # Display AI Summary
            st.markdown("""
                <div class='info-card'>
                    <h3 style='color: #667eea; margin-bottom: 1rem; text-align: center;'>
                        🧠 AI-Generated News Summary
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%); 
                            padding: 1.5rem; border-radius: 12px; border-left: 4px solid #2196F3;'>
                    <ul style='padding-left: 1.5rem; margin: 0; line-height: 1.8;'>
                        {''.join([f'<li style="margin-bottom: 0.8rem; color: #333;">{line[1:].strip()}</li>' 
                                for line in formatted_summary.splitlines() if line.strip() and line.startswith('•')])}
                    </ul>
                </div>
            """, unsafe_allow_html=True)

            # Display Articles
            articles_text = ""
            if articles:
                st.markdown("""
                    <div style='margin-top: 2rem;'>
                        <h3 style='color: #667eea; margin-bottom: 1rem; text-align: center;'>
                            📰 Source Articles Analyzed
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
                
                top_articles = articles[:3]
                for i, article in enumerate(top_articles, 1):
                    title = article.get("title", "No title available")
                    source = article.get("source", {}).get("name", "Unknown Source")
                    date = article.get("publishedAt", "").split("T")[0] if article.get("publishedAt") else "Unknown Date"
                    url = article.get("url", "#")
                    
                    st.markdown(f"""
                        <div class='article-card'>
                            <h4 style='color: #333; margin-bottom: 0.8rem;'>
                                📄 Article {i}: {title}
                            </h4>
                            <div style='display: flex; justify-content: space-between; align-items: center; 
                                       flex-wrap: wrap; gap: 1rem;'>
                                <div>
                                    <span style='background: #e8f5e8; padding: 0.3rem 0.8rem; 
                                               border-radius: 15px; font-size: 0.8rem; color: #2e7d32;'>
                                        📅 {date}
                                    </span>
                                    <span style='background: #e3f2fd; padding: 0.3rem 0.8rem; 
                                               border-radius: 15px; font-size: 0.8rem; color: #1976d2; margin-left: 0.5rem;'>
                                        🏷️ {source}
                                    </span>
                                </div>
                                <a href='{url}' target='_blank' style='text-decoration: none; 
                                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                   color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem;'>
                                    🔗 Read Full Article
                                </a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    articles_text += f"Article {i}: {title}\nDate: {date} | Source: {source}\nURL: {url}\n\n"

                # Success message
                st.markdown(f"""
                    <div class='success-card'>
                        <span style='color: #2e7d32; font-weight: 600;'>
                            ✅ Successfully analyzed {len(top_articles)} articles and generated comprehensive summary!
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No articles found for this query. Please try a different search term.")

            # Save to history
            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((query, formatted_summary))

            # Prepare download content
            combined_output = f"""AI News Research Summary
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Query: {query}

Top News Header: {header_line}

🧠 AI-Generated News Summary:
{formatted_summary.strip()}

📰 Source Articles Analyzed:
{articles_text.strip()}

---
Generated by AI News Research Dashboard
"""

            # Download Buttons
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                st.download_button(
                    "📥 Download as TXT", 
                    data=combined_output, 
                    file_name=f"news_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 
                    mime="text/plain", 
                    use_container_width=True
                )

            pdf_output = create_pdf(combined_output)
            with col_download2:
                st.download_button(
                    "📄 Download as PDF", 
                    data=pdf_output, 
                    file_name=f"news_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", 
                    mime="application/pdf", 
                    use_container_width=True
                )
        else:
            st.error("⚠️ Please enter a research query to generate summary.")

# 🏃‍♂️ Sidebar Navigation
def show_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 1rem; color: white;'>
                <h2>🎛️ Dashboard</h2>
                <p>Control Panel</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; 
                       border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;'>
                <h4>👤 Welcome, Sukriti!</h4>
                <p style='margin: 0; opacity: 0.8;'>Premium User</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        st.metric("🔍 Queries Today", st.session_state.total_queries)
        st.metric("📄 Summaries", st.session_state.total_summaries)
        st.metric("📰 Articles Analyzed", st.session_state.total_articles)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# 🚀 Main App Execution
def main():
    handle_authentication()
    show_sidebar()
    generate_summary_and_output()
    show_history()

if __name__ == "__main__":
    main()