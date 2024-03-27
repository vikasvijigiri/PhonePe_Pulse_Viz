import git
import os
import tempfile
import pandas as pd
import re
import streamlit as st
import json
import mysql.connector
import time
#from sqlalchemy import create_engine



# ####################################################################################################
#                               PART: DATA PreProcessing
# ####################################################################################################

def open_header():

    st.markdown("<h1 style='text-align: center; color: red;'> Data Extraction </h1>", unsafe_allow_html=True)
    st.markdown("""
    #### Details regarding the variables types are explained below. Choose accordingly: 
    - aggregated -> Total data combined (useful for plotting and analysis)
    - map -> data in JSON format with lattitudes and longitudes (useful for geomaps)
    - year -> Which year data you want to focus on? (useful for comparison)
    - state -> Which state's data are you interested in? (Useful for comparison)
    """)


#######################################################################
def list_files(base_path):
    files = []
    for root, dirs, filenames in os.walk(base_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            abs_file_path = os.path.abspath(file_path)
            files.append(abs_file_path)
    return files



@st.cache_data
def clone_or_use_permanent_folder(repo_url):
    # Create or retrieve a temporary directory for storing the repository
    permanent_folder = os.path.join(tempfile.gettempdir(), "pulse_repo")
    
    # Check if the permanent folder already exists
    if len(os.listdir(permanent_folder)) > 0:
        print("Using existing permanent folder:", permanent_folder)
        return list_files(permanent_folder)
    else:
        if not os.path.exists(permanent_folder) and not os.path.isdir(permanent_folder):
            # Create the permanent folder if it doesn't exist
            os.makedirs(permanent_folder)
        print("Cloning repository into permanent folder:", permanent_folder)
        # Clone the repository into the permanent folder
        git.Repo.clone_from(repo_url, permanent_folder)
        return list_files(permanent_folder)
    
#######################################################################


@st.cache_data
def convert_files_to_JSON(files_list):
    def pattern_exists_simple(pattern, string_list):
        for string in string_list:
            if pattern in string:
                return True
        return False

    
    # loop over files list and collect relevant data from the names of the folder itself.
    quarter = []
    year = []
    states_list = []
    type = []
    count = []
    amount = []



    df2_t_i = pd.DataFrame()
    df2_t_u = pd.DataFrame()    
    
    df2_m_i = pd.DataFrame()
    df2_m_t = pd.DataFrame()
    df2_m_u = pd.DataFrame()

    df2_a_i = pd.DataFrame()
    df2_a_t = pd.DataFrame()
    df2_a_u = pd.DataFrame()    
    for file in files_list:
        file_path = os.path.normpath(file)
        list_file_contents = file_path.split(os.sep)        
        json_exists = pattern_exists_simple('.json', list_file_contents)
        # state_exists = pattern_exists_simple(state_, list_file_contents)
        # aggregated_exists = pattern_exists_simple(usage_capacity_, list_file_contents)
        # insurance_exists = pattern_exists_simple(monetary_type_, list_file_contents)
        # year_exists = pattern_exists_simple(str(year_), list_file_contents) 
        # hover_exists = pattern_exists_simple('hover', list_file_contents)         
        #df = pd.DataFrame()
        df_t_i = pd.DataFrame()
        df_t_u = pd.DataFrame()  

        df_m_i = pd.DataFrame()
        df_m_t = pd.DataFrame()
        df_m_u = pd.DataFrame()
    
        df_a_i = pd.DataFrame()
        df_a_t = pd.DataFrame()
        df_a_u = pd.DataFrame()    
        #########################################################################################################  
        if json_exists:
            if 'top' in list_file_contents and 'india' in list_file_contents:#if usage_capacity_ == 'top' and json_exists:
                states_list.append(str(list_file_contents[-3]))
                json_data = json.load(open(file_path))
                if json_data:
                    if 'state' not in list_file_contents:
                        quarter = int(list_file_contents[-1].split(".")[0])
                        year = str(list_file_contents[-2])  
                        states = str(list_file_contents[-3])
                        
                        #st.write("camee")
                        if ('insurance' in list_file_contents) or ('transaction' in list_file_contents):
                            #st.write("camee")
                            states_data = []
                            for state in json_data['data']['states']:
                                #st.write("camee")
                                states_data.append([quarter, states, year, state['entityName'], state['metric']['type'], state['metric']['count'], state['metric']['amount']])
        
                            
                            df_t_i = pd.DataFrame(states_data, columns=['quarter', 'state', 'year', 'entityName', 'type_', 'count', 'amount'])
                        elif 'user' in list_file_contents:
                            states_data = []
                            for state in json_data['data']['states']:
                                # Extracting data for 'states'
                                states_data.append([quarter, states, year, state['name'], state['registeredUsers']])
                            
                            df_t_u = pd.DataFrame(states_data, columns=['quarter', 'state', 'year', 'Name', 'Registered_Users'])


            elif 'aggregated' in list_file_contents and 'india' in list_file_contents:
                states_list.append(str(list_file_contents[-3]))
                json_data = json.load(open(file_path))
                if json_data:
                    if 'state' not in list_file_contents:
                        quarter = int(list_file_contents[-1].split(".")[0])
                        year = str(list_file_contents[-2])  
                        states = str(list_file_contents[-3])
                        if 'insurance' in list_file_contents:
                            df_data = []
                            if json_data['data']['transactionData']:
                                name = json_data['data']['transactionData'][0]['name']
                                p_type = json_data['data']['transactionData'][0]['paymentInstruments'][0]['type']
                                count = json_data['data']['transactionData'][0]['paymentInstruments'][0]['count']
                                amount = json_data['data']['transactionData'][0]['paymentInstruments'][0]['amount']
                                df_data.append(['insurance', year, quarter, states, name, p_type, count, amount])
                            df_a_i = pd.DataFrame(df_data, 
                                                  columns=['type_', 'year', 'quarter', 'state', 'Name', 'Type_', 'Count', 'Amount'])  
                        if 'transaction' in list_file_contents:
                            df_data = []
                            for transaction in json_data['data']['transactionData']:
                                name = transaction['name']
                                if transaction['paymentInstruments']:
                                    count = transaction['paymentInstruments'][0]['count']
                                    amount = transaction['paymentInstruments'][0]['amount']
                                    df_data.append(['transaction', year, quarter, states, name, count, amount])
                            
                            # Create DataFrame
                            df_a_t = pd.DataFrame(df_data, columns=['type_', 'year', 'quarter', 'state', 'Name', 'Count', 'Amount'])
                        if 'user' in list_file_contents:      
                            df_data = []
                            if json_data['data']['usersByDevice']:
                                for device in json_data['data']['usersByDevice']:
                                    brand = device['brand']
                                    count = device['count']
                                    percentage = device['percentage']
                                    df_data.append(['user', year, quarter, states, brand, count, percentage])                            
                                # Create DataFrame
                            df_a_u = pd.DataFrame(df_data, columns=['type_', 'year', 'quarter', 'state', 'Brand', 'Count', 'Percentage']) 
                
            elif 'map' in list_file_contents and 'india' in list_file_contents:#if usage_capacity_ == 'top' and json_exists:
                states_list.append(str(list_file_contents[-3]))
                json_data = json.load(open(file_path))
                if json_data:
                    if 'state' not in list_file_contents:
                        quarter = int(list_file_contents[-1].split(".")[0])
                        year = str(list_file_contents[-2])  
                        states = str(list_file_contents[-3])
                        if 'insurance' in list_file_contents and 'hover' in list_file_contents:
                            df_data = []
                            for item in json_data['data']['hoverDataList']:
                                name = item['name']
                                if item['metric']:
                                    count = item['metric'][0]['count']
                                    amount = item['metric'][0]['amount']
                                    df_data.append(['insurance', year, quarter, states, name, count, amount])
                                    # Create DataFrame
                            df_m_i = pd.DataFrame(df_data, columns=['type_', 'year', 'quarter', 'state', 'Name', 'Count', 'Amount'])
                        
                        if 'user' in list_file_contents:
                            # Extracting data for DataFrame
                            df_data = []
                            for state, metrics in json_data['data']['hoverData'].items():
                                registered_users = metrics['registeredUsers']
                                app_opens = metrics['appOpens']
                                df_data.append(['user', year, quarter, state, registered_users, app_opens])
                            df_m_u = pd.DataFrame(df_data, columns=['type_', 'year', 'quarter',  'state', 'Registered_Users', 'App_Opens'])

                        if 'transaction' in list_file_contents:                            
   
                            df_data = []
        
                            quarter = int(list_file_contents[-1].split(".")[0])
                            year = str(list_file_contents[-2])
                            states = str(list_file_contents[-3])
                            for item in json_data['data']['hoverDataList']:
                                name = item['name']
                                if item['metric']:
                                    count = item['metric'][0]['count']
                                    amount = item['metric'][0]['amount']
                                    df_data.append(['transaction', year, quarter, states, name, count, amount])
                                
                            df_m_t = pd.DataFrame(df_data, columns=['type_', 'year', 'quarter', 'state', 'Name', 'Count', 'Amount'])

        # ########################################################################
        df2_t_i = pd.concat([df_t_i, df2_t_i], axis=0) 
        df2_t_u = pd.concat([df_t_u, df2_t_u], axis=0) 
        
        df2_m_i = pd.concat([df_m_i, df2_m_i], axis=0)  
        df2_m_t = pd.concat([df_m_t, df2_m_t], axis=0)  
        df2_m_u = pd.concat([df_m_u, df2_m_u], axis=0)  
        
        df2_a_i = pd.concat([df_a_i, df2_a_i], axis=0)  
        df2_a_t = pd.concat([df_a_t, df2_a_t], axis=0)  
        df2_a_u = pd.concat([df_a_u, df2_a_u], axis=0)  
        

    dataframes = {
        ('top', 'insurance'): df2_t_i,
        ('top', 'transaction'): df2_t_i,
        ('top', 'user'): df2_t_u,
        ('aggregated', 'insurance'): df2_a_i,
        ('aggregated', 'transaction'): df2_a_t,
        ('aggregated', 'user'): df2_a_u,
        ('map', 'insurance'): df2_m_i,
        ('map', 'transaction'): df2_m_t,
        ('map', 'user'): df2_m_u
    }    
    return dataframes, states_list

############################################################################################

def options_extraction(files_list):      

    # if 'states_list' not in st.session_state:
    #     st.session_state.states_list = []

    states_list = []
    
    container_style = """
        <style>
        .dataframe-container {
            width: 6000px;  /* Adjust the width as needed */
        }
        </style>
    """
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
    # Render selectboxes for user input
    cols = st.columns(5)
    usage_capacity_ = cols[0].selectbox(
        "Select type?",
        ['aggregated', 'map', 'top'],
        index=1
    )     

    monetary_type_ = cols[1].selectbox(
        "Monetary type?",
        ['insurance', 'transaction', 'user'],
        index=2
    )

    year_ = cols[2].selectbox(
        "year?",
        ['All'] + [str(year) for year in range(2018, 2024)],
        index=0
    )

    state_ = cols[3].selectbox(
        "State/Country?",
        list(set(['india'] + states_list)),
        index=0 
    )
    
    quarter_ = cols[4].selectbox(
        "quarter type?",
        [0] + [1, 2, 3, 4],
        index=0
    )


    button_view_col = st.columns(7)

    ########### button 1
    st.markdown(button_style, unsafe_allow_html=True)  
    button_view = button_view_col[2].button('View', key='view')    
    if st.session_state.get('buttonView') != True:
        st.session_state['buttonView'] = button_view
    
    if st.session_state['buttonView'] == True:
        st.write("Takes some time to run.... only once. Stay Tuned")
        dataframes, states_list = convert_files_to_JSON(files_list)
        selected_df = dataframes.get((usage_capacity_, monetary_type_), None)
        if selected_df is not None:
            if state_ == 'india':
                if year_ == 'All':
                    if quarter_ == 0:
                        df = selected_df
                    else:
                        df = selected_df[(selected_df['quarter'] == quarter_)]
                else:
                    if quarter_ == 0:
                        df = selected_df[(selected_df['year'] == year_)]
                    else:
                        df = selected_df[(selected_df['year'] == year_) & (selected_df['quarter'] == quarter_)]
            else:
                if year_ == 'All':
                    if quarter_ == 0:
                        df = selected_df
                    else:
                        df = selected_df[(selected_df['quarter'] == quarter_) & (selected_df['state'] == state_)]
                else:
                    if quarter_ == 0:
                        df = selected_df[(selected_df['year'] == year_) & (selected_df['state'] == state_)]
                    else:
                        df = selected_df[(selected_df['year'] == year_) & (selected_df['quarter'] == quarter_) & (selected_df['state'] == state_)]
        
        else:
            st.warning("Warning: No matching data found")

        st.session_state.df = df  
        st.markdown(container_style, unsafe_allow_html=True)
        st.dataframe(st.session_state.df, width=1024*2, height=768) 
        #df.to_csv('data.csv', index=False)  # Set index=False to exclude the DataFrame index from the CSV file
    ###########  button 2
    st.markdown(button_style, unsafe_allow_html=True)   
    button_upload = button_view_col[4].button("Upload", key='upload')
 
    if st.session_state.get('buttonUpload') != True:
        st.session_state['buttonUpload'] = button_upload
    
    if st.session_state['buttonUpload'] == True:
        # Ensure df is not None before attempting upload
        if st.session_state.df is not None:
            MySQL_server_details_UI()
        else:
            st.warning("No data available to upload.")
        
############################################################################################    
def MySQL_server_details_UI():

    st.markdown("<h1 style='text-align: center; color: red;'> Data Migration </h1>", unsafe_allow_html=True)
    st.markdown("""
    #### Enter the details below to connect to the MySQL database (local): 
    - hostname -> Name of the host in the MySQL DB.
    - username -> Username used to create a connection in the database (DB). 
    - Password -> Password used to access the a created connection.
    - Table Name -> Enter the desired name you want to ascribe to the table you are gonna create.
    """)
 
    container_style = """
        <style>
        .dataframe-container {
            width: 6000px;  /* Adjust the width as needed */
        }
        </style>
    """   

    cols = st.columns(4)
    localhost = cols[0].text_input("hostname", value='localhost')  
    root = cols[1].text_input("username", value='root')
    passwd = cols[2].text_input("Password", value='Vikas@123')  
    table_name = cols[3].text_input("Table Name", value='table_name')


    #colss = st.columns(7)
    #st.markdown(container_style, unsafe_allow_html=True)
    #st.dataframe(st.session_state.df, width=1024*2, height=768)  

    migrate_to_mysql(localhost, root, passwd, table_name)


def table_exists(cursor, database_name, table_name):
    cursor.execute(f"SHOW TABLES FROM {database_name} LIKE '{table_name}'")
    return cursor.fetchone() is not None
    

def migrate_to_mysql(localhost, root, passwd, table_name):
    container_style = """
        <style>
        .dataframe-container {
            width: 6000px;  /* Adjust the width as needed */
        }
        </style>
    """
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

    database_name = 'phonepe_pulse'

    st.markdown("""
        <style>
        .radio-container {
            width: 400px !important;
        }
        </style>
        """, unsafe_allow_html=True)
    radio_append_cols = st.columns(3)
    #########################################
    add_ = radio_append_cols[1].radio(
        "How would you like to add data?",
        ['append', 'overwrite'],
        index = 0
    )    
 
    #st.write("Almost near button")

    button_view_col = st.columns(7)
    ########### button 1
    st.markdown(button_style, unsafe_allow_html=True)  
    button_view = button_view_col[2].button('Click to Upload', key = 'final upload')    
    if st.session_state.get('buttonFupload') != True:
        st.session_state['buttonFupload'] = button_view
    
    if st.session_state['buttonFupload'] == True: 
        # Connect to MySQL
        # mysql_conn = mysql.connector.connect(
        #     host=localhost,
        #     user=root,
        #     password=passwd,
        #     auth_plugin='mysql_native_password'
        # )
        # mysql_cursor = mysql_conn.cursor()
        # st.write("Connected to MySQL!")

        #mysql_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        # if table_exists(mysql_cursor, database_name, table_name):
        #     alert = st.success(f"Table '{table_name}' exists.")
        #     time.sleep(3) # Wait for 3 seconds
        #     alert.empty() # Clear the alert            
        # else:
        #     alert = st.warning(f"Table '{table_name}' does not exist.")
        #     time.sleep(3) # Wait for 3 seconds
        #     alert.empty() # Clear the alert

        # Create SQLAlchemy engine
        #engine = create_engine(f"mysql+mysqlconnector://{root}:{passwd}@{localhost}/{database_name}")
        
        
        # Use the to_sql method to dump the DataFrame into MySQL
        #st.session_state.df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        
        # Close the SQLAlchemy engine
        #engine.dispose()
        #st.session_state.df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        #create_table_from_df(mysql_conn, mysql_cursor, database_name, table_name, st.session_state.df)
        load_data_to_mysql(localhost, root, passwd, 'phonepe_pulse', st.session_state.df, table_name, add_)
        
        #engine = create_engine(f"mysql+mysqlconnector://{root}:{localhost}@{passwd}/{database_name}")
        
        # Insert DataFrame into SQL table
        #st.session_state.df.to_sql(table_name, con=engine, if_exists='append', index=False)  # Replace 'your_table' with your actual table name
        

        #engine.dispose()
        #mysql_conn.close()        
        st.success('Data appended successfully!')   
        st.session_state['buttonUpload'] = False
        st.session_state['buttonView'] = False
        st.session_state['buttonFupload'] = False




def connect_to_mysql(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

def create_table(conn, df, table_name):

    # cursor = conn.cursor()
    # columns = []

    # for col, dtype in df.dtypes.items():
    #     if pd.api.types.is_string_dtype(dtype):
    #         sql_type = "VARCHAR(255)"
    #     elif pd.api.types.is_integer_dtype(dtype):
    #         sql_type = "BIGINT"
    #     elif pd.api.types.is_float_dtype(dtype):
    #         sql_type = "FLOAT"
    #     elif pd.api.types.is_bool_dtype(dtype):
    #         sql_type = "BOOLEAN"
    #     else:
    #         sql_type = "VARCHAR(255)"

    #     columns.append(f"{col} {sql_type}")

    # columns_str = ", ".join(columns)
    # create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
    # cursor.execute(create_table_query)
    # cursor.close()
    try:
        cursor = conn.cursor()
        columns = []

        # Check if the table exists
        existing_tables_query = f"SHOW TABLES LIKE '{table_name}'"
        cursor.execute(existing_tables_query)
        table_exists = cursor.fetchone() is not None

        if not table_exists:
            for col, dtype in df.dtypes.items():
                if pd.api.types.is_string_dtype(dtype):
                    sql_type = "VARCHAR(255)"
                elif pd.api.types.is_integer_dtype(dtype):
                    sql_type = "BIGINT"
                elif pd.api.types.is_float_dtype(dtype):
                    sql_type = "FLOAT"
                elif pd.api.types.is_bool_dtype(dtype):
                    sql_type = "BOOLEAN"
                else:
                    sql_type = "VARCHAR(255)"

                columns.append(f"{col} {sql_type}")

            columns_str = ", ".join(columns)
            create_table_query = f"CREATE TABLE {table_name} ({columns_str})"
            cursor.execute(create_table_query)
        cursor.close()
    except Exception as e:
        print(f"Error creating table: {str(e)}")


def insert_data(conn, df, table_name, append=False):
    # cursor = conn.cursor()
    # columns = ', '.join(df.columns)
    # placeholders = ', '.join(['%s'] * len(df.columns))
    # query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    # data = [tuple(row) for row in df.values]
    # cursor.executemany(query, data)
    # cursor.close()
    # conn.commit()
    try:
        cursor = conn.cursor()
        
        if append:
            # If append mode is enabled, simply insert data into the table
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            data = [tuple(row) for row in df.values]
            cursor.executemany(query, data)
            conn.commit()
        else:
            # Otherwise, check if the table exists and create it if needed
            existing_tables_query = f"SHOW TABLES LIKE '{table_name}'"
            cursor.execute(existing_tables_query)
            table_exists = cursor.fetchone() is not None

            if not table_exists:
                # If the table does not exist, create it
                columns = []
                for col, dtype in df.dtypes.items():
                    if pd.api.types.is_string_dtype(dtype):
                        sql_type = "VARCHAR(255)"
                    elif pd.api.types.is_integer_dtype(dtype):
                        sql_type = "BIGINT"
                    elif pd.api.types.is_float_dtype(dtype):
                        sql_type = "FLOAT"
                    elif pd.api.types.is_bool_dtype(dtype):
                        sql_type = "BOOLEAN"
                    else:
                        sql_type = "VARCHAR(255)"

                    columns.append(f"{col} {sql_type}")

                columns_str = ", ".join(columns)
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
                cursor.execute(create_table_query)

                # Insert data into the newly created table
                columns = ', '.join(df.columns)
                placeholders = ', '.join(['%s'] * len(df.columns))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                data = [tuple(row) for row in df.values]
                cursor.executemany(query, data)
                conn.commit()

        cursor.close()
    except Exception as e:
        st.write(f"Error inserting into table: {str(e)}")
        st.warning("Try entering a different table name!")




def load_data_to_mysql(host, user, password, database, df, table_name, add):
    conn = connect_to_mysql(host, user, password, database)
    create_table(conn, df, table_name)
    insert_data(conn, df, table_name, add)
    conn.close()




if __name__ == "__main__":
    open_header()
    files_list = clone_or_use_permanent_folder("https://github.com/PhonePe/pulse.git") 
    #dataframe, states_list = convert_files_to_JSON(files_list)
    options_extraction(files_list)    
    





