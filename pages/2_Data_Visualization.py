import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
import mysql.connector
import numpy as np
from plotly.subplots import make_subplots


@st.cache_data
def open_header():

    # Animated text content with HTML and CSS
    animated_text = """
    <div style="font-size: 64px; color: #00ff00; text-align: center;">
      Data Visualization
    </div>
    """
    
    # Display animated text
    alert = st.markdown(animated_text, unsafe_allow_html=True)
    
    # alert1 = st.markdown("""
    # #### Here the dropdown menus are very similar to the data processing stage!

    # - year -> Shows data in that particular year.
    # - quarter -> shows data for that particular quarter.
    # - monetary_type - > Shows data for that particular financial/payment instruments.
    # - data_type - > map, user, aggregated.

    # -- Note: Currently on country data is shown. Districts wise data is yet to be available.
    # """)
    # time.sleep(5)
    # alert1.empty()



def create_map(col1, col2, df):
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations=col1,
        color=col2,
        color_continuous_scale='Greens',

    )    
    
    # fig.add_trace(go.Scattergeo(
    #     mode='text',
    #     #text=df['ST_NM'].str.title(),
    #     text=['{}<br>{}'.format(k,v) for k,v in zip(df['ST_NM'].str.title(), df['value'])],
    #     textfont={'color': 'Green'},
    #     name='',
    # ))
    

    
    fig.update_geos(fitbounds="locations", visible=False)
    # Adjust the layout to increase the width
    fig.update_layout(
        width=1024,  # Adjust this value to increase the width as needed
        margin=dict(l=0, r=0, t=30, b=0),  # Optionally adjust the margins
        coloraxis_colorbar=dict(x=0.20, y=0.5)  # Adjust the position of the color bar
    )    
    return fig

# def create_map(col1, col2, df):
# # Assuming you have already created df, col1, col2

#     # Create choropleth figure
#     fig = go.Figure(go.Choropleth(
#         geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#         featureidkey='properties.ST_NM',
#         locations=df[col1],
#         z=df[col2],
#         colorscale='Blues',
#         colorbar=dict(title='Percentage'),
#         hoverinfo='location+z'
#     ))
    
#     # Update hover template to display percentages with two decimal places
#     fig.update_traces(hovertemplate='%{location}<br>Percentage: %{z:.2f}%<extra></extra>')
    
#     # Update layout to fit bounds and adjust width
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(
#         title='Choropleth Map',
#         width=1024,
#         margin=dict(l=0, r=0, t=30, b=0)
#     )
    
#     # Display the figure
#     return fig


def get_table_names_no_cache():
    try:
        database_name = 'phonepe_pulse'
        
        cols = st.columns(3)
        localhost_placeholder = cols[0].empty()
        root_placeholder = cols[1].empty()
        passwd_placeholder = cols[2].empty()
        
        #localhost = localhost_placeholder.text_input("hostname", value='localhost', key='localhost1')  
        #root = root_placeholder.text_input("username", value='root', key='roots')
        #passwd = passwd_placeholder.text_input("Password", value='Vikas@123', key='pass')  
        
        localhost = st.session_state.localhost
        root = st.session_state.root
        passwd = st.session_state.passwd
        



        
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
        #st.write(tables)

        # # Execute SQL query to select all data from the table
        # query = f"SELECT * FROM {table_name}"
        # df = pd.read_sql_query(query, conn)


        # Close cursor and connection
        cursor.close()
        conn.close()
        # Empty the placeholders after 5 seconds
        localhost_placeholder.empty()
        root_placeholder.empty()
        passwd_placeholder.empty()
        return tables

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None, None


#@st.cache_data
def get_table_names():
    try:
        database_name = 'phonepe_pulse'
        
        cols = st.columns(3)
        
        if 'localhost' not in st.session_state:
            st.session_state.localhost = 'localhost'
        if 'root' not in st.session_state:
            st.session_state.root = 'root'
        if 'passwd' not in st.session_state:
            st.session_state.passwd = 'Vikas@123'

        
        st.session_state.localhost = cols[0].text_input("hostname", value='localhost', key='localhostss')  
        st.session_state.root = cols[1].text_input("username", value='root', key='roots')
        st.session_state.passwd  = cols[2].text_input("Password", value='Vikas@123', key='pass')  

        
        localhost = st.session_state.localhost
        root = st.session_state.root
        passwd = st.session_state.passwd               
        st.write(localhost)
 



        
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
        #st.write(tables)

        # # Execute SQL query to select all data from the table
        # query = f"SELECT * FROM {table_name}"
        # df = pd.read_sql_query(query, conn)


        # Close cursor and connection
        cursor.close()
        conn.close()
        # Empty the placeholders after 5 seconds
        localhost_placeholder.empty()
        root_placeholder.empty()
        passwd_placeholder.empty()
        return tables

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None, None



def copy_mysql_data_to_df_no_cache(table_names):
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

        localhost = st.session_state.localhost
        root = st.session_state.root
        passwd = st.session_state.passwd
        
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
        warn = st.warning("Fetching directly not cached data!")
        

        #warn.empty()
        data_frames = {}  # Initialize an empty dictionary
        other_data_frames = {}
        for table_name in table_names:
            # Execute SQL query to select all data from the table
            query = f"SELECT * FROM {database_name}.{table_name}"
            df = pd.read_sql_query(query, conn)
            #st.dataframe(df)
            col1 = matches_column(df, 'bihar')
            #st.write(col1)
            if col1 is not None:
                df['States'] = [state.title() for state in df[col1].tolist()] 
                df.drop(columns=[col1], inplace=True)
                #st.dataframe(df)
                data_frames[table_name] = df.drop_duplicates()  # As 
            else:
                other_data_frames[table_name] = df
            #st.write("vik", table_name)
        # Close connection
        conn.close()

        return data_frames, other_data_frames

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None, None


@st.cache_data
def copy_mysql_data_to_df(table_names):
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

        localhost = st.session_state.localhost
        root = st.session_state.root
        passwd = st.session_state.passwd
        
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
        warn = st.warning("Fetching directly not cached data!")
        

        #warn.empty()
        data_frames = {}  # Initialize an empty dictionary
        other_data_frames = {}
        for table_name in table_names:
            # Execute SQL query to select all data from the table
            query = f"SELECT * FROM {database_name}.{table_name}"
            df = pd.read_sql_query(query, conn)
            #st.dataframe(df)
            col1 = matches_column(df, 'bihar')
            #st.write(col1)
            if col1 is not None:
                df['States'] = [state.title() for state in df[col1].tolist()] 
                df.drop(columns=[col1], inplace=True)
                #st.dataframe(df)
                data_frames[table_name] = df.drop_duplicates()  # As 
            else:
                other_data_frames[table_name] = df
            #st.write("vik", table_name)
        # Close connection
        conn.close()

        return data_frames, other_data_frames

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None, None



@st.cache_data
def filter_dat(table_name, year, quarter):
    df = st.session_state.data_frames_dict[table_name]
    df = df[(df['year']==str(year)) & (df['quarter']==quarter)]    
    return df
#####################################################################################
        
def create_sliders(table_names):
    st.title('Data spread across India (Geomaps)')
    cols = st.columns(5)
    # Slider for list of strings
    #selected_option_index = cols[0].slider("Monetary instrument type", 0, len(table_names)-1, key='table_names')
    #st.write(table_names[selected_option_index])

    table_name = cols[0].selectbox(
       "Select a table",
        table_names,
        index= 2,
       placeholder="Select",
    )   
    
    # Slider for quarter (range from 1 to 4)
    quarter = cols[1].slider("Select a quarter", min_value=1, max_value=4, key='quarter')


    # Slider for year (range from 2018 to 2023)
    year = cols[2].slider("Select a year", min_value=2018, max_value=2023, key='year')
    
    
    #df = st.session_state.data_frames_dict[table_name]
    df = filter_dat(table_name, year, quarter)
    #df.shape
    
    #st.dataframe(df)
    
    col2 = cols[3].selectbox(
       "Select Y-variable:",
       df.columns.tolist(),
        index = len(df.columns.tolist())-2,
       placeholder="Select",
    )     
    # Return selected values
    return df, 'States', col2



def display_data(df):
    st.dataframe(df, width=1024*2, height=768)


def matches_column(df, element):
    for column in df.columns:
        if element in df[column].tolist():
            return column
            

# Define update function for animation
def update_trace(frame):
    new_x = x[:frame]
    new_y = y[:frame]
    fig.data[0].x = new_x
    fig.data[0].y = new_y


def state_evolution_year(table_names):

    cols = st.columns(5)
    # Generate x values from 0 to 2*pi
    table_name = cols[0].selectbox(
       "Select a table",
        table_names,
        index= 1,
       placeholder="Select",
        key = 'table box'
    )   


    
    quarter = cols[2].slider("Select a quarter", min_value=1, max_value=4, key='quarter1')

    df = st.session_state.data_frames_dict[table_name]


    # table_name = cols[0].selectbox(
    #    "Select a State",
    #     ['All'] + df['States'].tolist(),
    #     index= 0,
    #     placeholder="Select",
    #     key = 'table box'
    # ) 


    # Display the checkbox with multiple selections allowed
    selected_options = st.multiselect('Select States:', ['All']+list(set(df['States'].tolist())), default=['All'])


    
    
    df = df[(df['quarter'] == quarter)]

    if selected_options != ['All']:
        filtered_df = df[df['States'].isin(selected_options)]#.drop_duplicates()
    else:
        filtered_df = df#.drop_duplicates()

    #st.dataframe(filtered_df)
    if not filtered_df.empty:
        col2 = cols[4].selectbox(
           "Select Y-variable:",
           df.columns.tolist(),
            index = len(df.columns.tolist())-2,
            placeholder="Select",
            key = 'y-variable box'
        )  
        
        
    
        # Create DataFrame
        fig = px.line(filtered_df, x='year', y=col2, color='States', title=f'{col2} over Years for Indian States')
        # Display selected options
        #st.write('Selected options:', selected_options)
        return fig

    else:
        return go.Figure()




def generate_heatmap(table_names, colx, coly):
    st.title("Transaction Volumes distribution")


    cols = st.columns(5)
    # Generate x values from 0 to 2*pi
    table_name = cols[0].selectbox(
       "Select a table",
        table_names,
        index= 0,
        placeholder="Select",
        key = 'table box1'
    )   

    #year = cols[1].slider("Select a year", min_value=2018, max_value=2023, key='year1')
    
    if table_name == 'aggregated_transaction':

        
        quarter = cols[2].slider("Select a quarter", min_value=1, max_value=4, key='quarter2')
    
        df = st.session_state.odata_frames_dict[table_name]
        # st.dataframe(df)    
        df = df[(df['quarter'] == quarter)]
    
        #st.dataframe(df)
        if not df.empty:
            col2 = cols[3].selectbox(
                "Select Y-variable:",
                df.columns.tolist(),
                index = len(df.columns.tolist())-2,
                placeholder="Select",
                key = 'y-variable box1'
            )  
            
            
            # st.dataframe(df)
            # #r_data = df.pivot(index=colx, columns=coly, values=col2)
            # # Generate heatmap using Plotly Express
            # fig = px.imshow(df.pivot(index=coly, columns=colx, values=col2),
            #     labels=dict(x=colx, y=coly, color=col2),  # Set axis labels
            #     x=df[colx].unique(),  # Unique years
            #     y=df[coly].unique(),  # Unique categories
            #     color_continuous_scale='Viridis_r',
            #     origin='lower')  # Set color scale

            # data = {
            #     'year': [2018, 2018, 2018, 2019, 2019, 2019],
            #     'category': ['A', 'B', 'C', 'A', 'B', 'C'],
            #     'count': [100, 200, 300, 400, 500, 600]
            # }
            
            # # Create DataFrame
            # df = pd.DataFrame(data)
            
            # Pivot the DataFrame to get the appropriate structure for the heatmap
            pivot_df = df.pivot(index=coly, columns=colx, values=col2)

            # Plot the heatmap using plotly express
            fig = px.imshow(pivot_df,
                            labels=dict(x=colx, y=coly, color=col2),
                            x=pivot_df.columns,
                            y=pivot_df.index,
                            color_continuous_scale='Viridis')

            
            # Set title
            fig.update_layout(title=f'Transaction Volumes Across Time Periods and Categories ({col2})')
        
            # Display the heatmap
            st.plotly_chart(fig)
        else:
            st.warning("Empty dataframe. Check your db or server.")
            st.plotly_chart(go.Figure())        

    else:
        st.warning("You have selected wrong database. This viz is available only for aggregated transaction DB.")
        st.plotly_chart(go.Figure())

#################################################################################################################


def main():
    open_header()
    # Centering CSS
    centered_style = "<style> .centered { display: flex; justify-content: center; } </style>"
    
    # Beautified button with centered styling
    button_html = """
        <div class="centered">
            <button style="background-color: #4CAF50; color: red; padding: 10px 24px; cursor: pointer; border: none; border-radius: 4px;">Update Data from MySQL</button>
        </div>
    """
    
    # Render the button
    st.markdown(centered_style, unsafe_allow_html=True)
    if st.button('Update Data from MySQL'):
        # if st.button('Click to dynamically update'):
        table_names = get_table_names_no_cache()
        st.session_state.data_frames_dict, st.session_state.odata_frames_dict = copy_mysql_data_to_df_no_cache(table_names)        
    
    if 'data_frames_dict' not in st.session_state:
        st.session_state.data_frames_dict = None

    if 'odata_frames_dict' not in st.session_state:
        st.session_state.odata_frames_dict = None        



    # if st.button('Click to dynamically update'):
    table_names = get_table_names()
    #st.write(table_names)
    if st.session_state.data_frames_dict is None:
        st.session_state.data_frames_dict, st.session_state.odata_frames_dict = copy_mysql_data_to_df(table_names)
        #st.write("Again doing!")
    #st.write(st.session_state.data_frames_dict)
    st.write(table_names)
    if table_names:        
        df, col1, col2 = create_sliders(table_names)
    
        cols = st.columns(3)
        if not df.empty:
    
            #st.write(df[col2])
    
            fig = create_map(col1, col2, df)
            st.plotly_chart(fig)    
        else:
            st.warning("Empty dataframe encountered!")
            fig = create_map(col1, col2, df)
            st.plotly_chart(fig)  
    
    
        st.title('Variation over the years')
    
        # Add a sidebar
        st.sidebar.markdown('### Animation Controls')
        frame = st.sidebar.slider('Frame', min_value=0, max_value=9)
    
        # Display the animated plot
        st.plotly_chart(state_evolution_year(table_names), use_container_width=True)
    
    
        generate_heatmap(table_names, 'year', 'Name')
        col = st.columns(3)
    else:
        st.warning("Tables are empty or check your database details and the connection! ")






if __name__ == "__main__":
    main()
