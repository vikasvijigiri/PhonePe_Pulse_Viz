import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
import mysql.connector


@st.cache_data
def open_header():

    # Animated text content with HTML and CSS
    animated_text = """
    <div style="animation: neon 1.5s ease-in-out infinite alternate; font-size: 36px; color: #00ff00; text-align: center;">
      Data Visualization
    </div>
    
    <style>
    @keyframes neon {
      from {
        text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 30px #00ff00, 0 0 40px #00ff00, 0 0 70px #00ff00, 0 0 80px #00ff00, 0 0 100px #00ff00, 0 0 150px #00ff00;
      }
      to {
        text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00, 0 0 20px #00ff00, 0 0 35px #00ff00, 0 0 40px #00ff00, 0 0 50px #00ff00, 0 0 75px #00ff00;
      }
    }
    </style>
    """
    
    # Display animated text
    alert = st.markdown(animated_text, unsafe_allow_html=True)
    time.sleep(5)
    alert.empty()
    
    alert1 = st.markdown("""
    #### Here the dropdown menus are very similar to the data processing stage!

    - year -> Shows data in that particular year.
    - quarter -> shows data for that particular quarter.
    - monetary_type - > Shows data for that particular financial/payment instruments.
    - data_type - > map, user, aggregated.

    -- Note: Currently on country data is shown. Districts wise data is yet to be available.
    """)
    time.sleep(15)
    alert1.empty()

# Function to create the geo map
def create_map(columns, df):
    col1, col2 = columns
    fig = go.Figure(data=go.Choropleth(
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locationmode='geojson-id',
        locations=df[col1],
        z=df[col2],

    
        autocolorscale=False,
        colorscale='Reds',
        marker_line_color='peachpuff',
    
        colorbar=dict(
            title={'text': col1},
    
            thickness=15,
            len=0.35,
            bgcolor='rgba(255,255,255,0.6)',
    
            tick0=0,
            dtick=20000,
    
            xanchor='left',
            x=0.01,
            yanchor='bottom',
            y=0.05
        )
    ))
    
    fig.update_geos(
        visible=False,
        projection=dict(
            type='conic conformal',
            parallels=[12.472944444, 35.172805555556],
            rotation={'lat': 24, 'lon': 80}
        ),
        lonaxis={'range': [68, 98]},
        lataxis={'range': [6, 38]}
    )
    
    fig.update_layout(
        title=dict(
            text=col2,
            xanchor='center',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b': 10}
        ),
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=550,
        width=550
    )
    
    return fig




def get_table_names():
    try:
        database_name = 'phonepe_pulse'
        
        cols = st.columns(3)
        localhost = cols[0].text_input("hostname", value='localhost')  
        root = cols[1].text_input("username", value='root')
        passwd = cols[2].text_input("Password", value='Vikas@123')  
        
        conn = mysql.connector.connect(
            host=localhost,
            user=root,
            password=passwd,
            database=database_name
        )
        cursor = conn.cursor()

        # Retrieve list of tables in the database
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]


        # # Execute SQL query to select all data from the table
        # query = f"SELECT * FROM {table_name}"
        # df = pd.read_sql_query(query, conn)


        # Close cursor and connection
        cursor.close()
        conn.close()

        return tables

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None, None

        
def create_sliders(table_names):




    # Slider for list of strings
    selected_option_index = st.slider("Monetary instrument type", 0, len(table_names)-1, key='table_names')
    #st.write(table_names[selected_option_index])
    cols = st.columns(5)
    # Slider for quarter (range from 1 to 4)
    quarter = cols[1].slider("Select a quarter", min_value=1, max_value=4, key='quarter')
    
    # Slider for year (range from 2018 to 2023)
    year = cols[3].slider("Select a year", min_value=2018, max_value=2023, key='year')
    
    #st.write("year", year)
    df = copy_mysql_data_to_df(year, quarter, table_names[selected_option_index])
    cols = st.columns(5)
    col2 = cols[2].selectbox(
       "Select Y-variable:",
       df.columns.tolist(),
       placeholder="Select",
    )     
    # Return selected values
    return df, col2

@st.cache_data
def copy_mysql_data_to_df(year, quarter, table_name):
    try:
        container_style = """
            <style>
            .dataframe-container {
                width: 6000px;  /* Adjust the width as needed */
            }
            </style>
        """   
        database_name = 'phonepe_pulse'


        localhost = 'localhost'  
        root = 'root'
        passwd = 'Vikas@123'  
        # if table_name is not None:
        #     if table_name not in table_names:
        #         st.error(f"Table {table_name} doest not exists in {database_name}")
        # else:
        #     st.error(f"Please enter a valid table name!")
            
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=localhost,
            user=root,
            password=passwd,
            database=database_name
        )

        # Execute SQL query to select all data from the table
        query = f"SELECT * FROM {database_name}.{table_name} WHERE year = {str(year)} AND quarter = {quarter}"
        df = pd.read_sql_query(query, conn)
        #st.write(df, query)
        # Close connection
        conn.close()

        return df

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None


def display_data(df):
    st.dataframe(df, width=1024*2, height=768)


def matches_column(df, element):
    for column in df.columns:
        if element in df[column].tolist():
            return column
            
# # Streamlit code
# st.title('Geo Map Example for India')
# st.write('A simple example of creating a geo map for India using Plotly and Streamlit.')

# # Display the map
# st.plotly_chart(create_map(df))
def main():
    open_header()
    button_style = """
            <style>
            .stButton > button {
                color: blue;
                background: white;
                width: 200px;
                height: 50px;
            }
            </style>
            """    
    col = st.columns(5)
    st.markdown(button_style, unsafe_allow_html=True) 
    button = col[2].button("Click to connect to MySQL dynamically", key='upload')    
    if st.session_state.get('button') != True:
        st.session_state['button'] = button

    
    if st.session_state['buttonUpload'] == True:
        while True:
            table_names = get_table_names()
            df, col2 = create_sliders(table_names)
            col1 = matches_column(df, 'bihar')
            df['Statess'] = [state.title() for state in df[col1].tolist()]
            columns = ['Statess', col2]
            #st.write(df[col2])
            fig = create_map(columns, df)
            st.plotly_chart(fig)  
            time.sleep(5)
        
    # if st.button('Click to dynamically update'):
    table_names = get_table_names()
    df, col2 = create_sliders(table_names)
    col1 = matches_column(df, 'bihar')
    df['Statess'] = [state.title() for state in df[col1].tolist()]
    columns = ['Statess', col2]
    #st.write(df[col2])
    fig = create_map(columns, df)
    st.plotly_chart(fig)    
    




if __name__ == "__main__":
    main()
    #display_data(df)













# import streamlit as st
# import plotly.graph_objects as go
# import pandas as pd
# import mysql.connector

# # Function to connect to MySQL database
# def connect_to_mysql(host, user, password, database):
#     return mysql.connector.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database
#     )

# # Function to retrieve table names from the MySQL database
# def get_table_names(host, user, password, database):
#     try:
#         conn = connect_to_mysql(host, user, password, database)
#         cursor = conn.cursor()

#         # Retrieve list of tables in the database
#         cursor.execute("SHOW TABLES")
#         tables = [table[0] for table in cursor.fetchall()]

#         # Close cursor and connection
#         cursor.close()
#         conn.close()

#         return tables

#     except mysql.connector.Error as e:
#         st.error(f"Error: {e}")
#         return None

# # Function to fetch data from MySQL database based on year, quarter, and table name
# def copy_mysql_data_to_df(host, user, password, database, year, quarter, table_name):
#     try:
#         conn = connect_to_mysql(host, user, password, database)

#         # Execute SQL query to select data from the table for the specified year and quarter
#         query = f"SELECT * FROM {table_name} WHERE year = {year} AND quarter = {quarter}"
#         df = pd.read_sql_query(query, conn)

#         # Close connection
#         conn.close()

#         return df

#     except mysql.connector.Error as e:
#         st.error(f"Error: {e}")
#         return None
        
# def matches_column(df, element):
#     for column in df.columns:
#         if element in df[column].tolist():
#             return column

# # Main function
# def main():
#     # Get MySQL connection parameters from user input
#     host = st.text_input("Enter MySQL host", value='localhost')
#     user = st.text_input("Enter MySQL username", value='root')
#     password = st.text_input("Enter MySQL password", value='', type='password')
#     database = st.text_input("Enter MySQL database name", value='phonepe_pulse')

#     # Display table names from the MySQL database
#     table_names = get_table_names(host, user, password, database)
#     if table_names:
#         selected_table_index = st.selectbox("Select a table", options=table_names)

#         # Sliders for year and quarter
#         year = st.slider("Select a year", min_value=2018, max_value=2023, key='year')
#         quarter = st.slider("Select a quarter", min_value=1, max_value=4, key='quarter')

#         # Fetch data from MySQL database based on user selection
#         df = copy_mysql_data_to_df(host, user, password, database, year, quarter, selected_table_index)
#         st.dataframe(df)
#         if df is not None:
#             col1 = matches_column(df, 'bihar')
#             df['Statess'] = [state.title() for state in df[col1].tolist()]
#             columns = ['Statess', col2]
#             fig = create_map(columns, df)
#             st.plotly_chart(fig)

# if __name__ == "__main__":
#     main()


