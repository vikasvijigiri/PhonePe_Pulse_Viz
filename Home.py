
import streamlit as st

def intro():
    import streamlit as st

    # st.write("How India uses PhonePe? 👋")
    st.set_page_config(layout='wide')
    st.markdown("<h1 style='text-align: center; color: red;'> How India uses PhonePe? </h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: black;'>Visualizing data through maps </h4>", unsafe_allow_html=True)    
    # st.sidebar.success("Click any page below")
    
    st.markdown(
    """
    <style>
        .aim {
            color: #1f77b4;
            font-size: 28px;
            font-weight: bold;
        }
        .data-source {
            color: #1f77b4;
            font-size: 22px;
            font-weight: bold;
        }
        .data-category {
            color: #1f77b4;
            font-size: 22px;
        }
        .data-type {
            color: #ff7f0e;
            font-style: italic;
        }
        .app-category {
            color: #1f77b4;
            font-size: 22px;
        }
        .feedback {
            color: #1f77b4;
            font-size: 28px;
            font-weight: bold;
        }
    </style>

    <div class="aim">
        • Aim:
    </div>
     <ul> 
         This project aims to <span class="data-type">visualize</span> the usage data of PhonePe across India.
     </ul>    

    <div class="data-source">
        • Data Source:
    </div>
     <div style="color: #1f77b4; font-size: 22px;">
        <li> The data is collected from GitHub - <a href="https://github.com/PhonePe/pulse" style="color: #ff7f0e; text-decoration: none;">PhonePe Pulse</a></li>
        
    </div>

    <div class="data-category">
        • Data Categorization:
    </div>
    <ul>
        <li>PhonePe Pulse contains data of payment instruments such as insurance, transactions, and user metrics. For example:
            <ul>
                <li>In the insurance data:
                    <ul>
                        <li>'Count' represents the number of users who have insured with the PhonePe app.</li>
                        <li>'Amount' represents the rupees in which the cash amount was insured with the PhonePe app.</li>
                    </ul>
                </li>
                <li>In the transaction data:
                    <ul>
                        <li>'Count' represents the number of transactions.</li>
                        <li>'Amount' refers to the amount that has been transacted.</li>
                        <li>'Year' indicates the year in which the total transactions were done.</li>
                        <li>'Quarter' indicates which quarter of the year the transactions were done.</li>
                    </ul>
                </li>
                <li>In the user data:
                    <ul>
                        <li>'App Opens' indicates the number of times the PhonePe user has opened the app.</li>
                        <li>'Registered Users' indicates the number of registered users of PhonePe.</li>
                        <li>'Year' indicates the year in which the number of Registered Users and App Opens have been recorded.</li>
                        <li>'Quarter' indicates the quarter of the year.</li>
                    </ul>
                </li>
            </ul>
        </li>
    </ul>

    <div class="app-category">
        • App Categorization:
    </div>
    <ul>
        <li>Data Extraction (GitHub)</li>
        <li>Data Processing (Pandas)</li>
        <li>Data Migration (MySQL)</li>
        <li>Data Visualization (Plotly)
            <ul>
                <li>Charts</li>
                <li>Graphs</li>
                <li>Maps</li>
            </ul>
        </li>
    </ul>

    <div class="feedback">
        • Feel free to explore and provide feedback!
    </div>
    """,
    unsafe_allow_html=True  # Allows HTML tags for custom styling
)


def main():
    intro()    



if __name__ == "__main__":
    main()

