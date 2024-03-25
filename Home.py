
import streamlit as st

def intro():
    import streamlit as st

    # st.write("How India uses PhonePe? 👋")

    st.markdown("<h1 style='text-align: center; color: red;'> How India uses PhonePe? </h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: black;'>Visualizing data through maps </h4>", unsafe_allow_html=True)    
    # st.sidebar.success("Click any page below")

    st.markdown(
        """
        ### Aim:
        - This project is aimed at visualizing the phonepe usage data across india.

        ### Data Source:
        -  **👈 The data is collected from github - [PhonePe Pulse](https://github.com/PhonePe/pulse)

        ### Data caterorization:
        - Insurance
            * count -> Number of phonepe user insuranced.
            * amount -> Total amount insuranced.
        - Transaction
            * count -> Number of transaction
            * amount -> Total amount transacted. 




        ### App categorization:

        - Data extraction (Github)
        - Data processing [Pandas)
        - Data Migration  (MySQL)
        - Data Visualization (Plotly)
        
        ### Feel free to explore and give a feedback! 
    """
    )


intro()

