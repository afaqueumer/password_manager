import streamlit as st 
import webbrowser
import sqlite3
from user import User

st.set_page_config(page_title="PMGR", page_icon="🚀" )     
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1532024802178-20dbc87a312a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80");
background-size: 100%;
display: flex;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


conn = sqlite3.connect("pwd.db")
c = conn.cursor()
c.execute("""CREATE TABLE if not exists pwd_mgr (app_name varchar(20) not null,
                        user_name varchar(50) not null,
                        pass_word varchar(50) not null,
                        email_address varchar(100) not null,
                        url varchar(255) not null,
                    primary key(app_name)       
                    );""")


def insert_data(u):
    with conn:
        c.execute("insert into pwd_mgr values (:app, :user, :pass, :email, :url)", {'app': u.app, 'user': u.username, 'pass': u.password, 'email': u.email, 'url': u.url})
        
def get_cred_by_app(app):
    with conn:
        c.execute("select app_name, user_name, pass_word, email_address, url FROM pwd_mgr where app_name = :name;", {'name': app})
        return c.fetchone()
    
def remove_app_cred(app):
    with conn:
        c.execute("DELETE from pwd_mgr WHERE app_name = :name", {'name': app})
        
def update_password(app,new_pass_word):
    with conn:
        c.execute("update pwd_mgr set pass_word = :pass where app_name = :name", {'name': app, 'pass': new_pass_word})


st.title("Password Manager 🔐")
st.markdown('#')

c.execute("select count(*) from pwd_mgr")
db_size = c.fetchone()[0] 

c.execute("select app_name from pwd_mgr")
app_names = c.fetchall()
app_names = [i[0] for i in app_names]

radio_option = st.sidebar.radio("Menu", options=["Home", "Add Account", "Update Password", "Delete Account"])

if radio_option=="Home":    
    st.subheader("Find Credential 🔎")  
    st.markdown("#####")  
    if db_size>0:                   
        option = st.selectbox('Select Application 📱', app_names) # TO be populated from DB
        st.markdown("#####")        
        cred = get_cred_by_app(option)
        with st.container():    
            st.text(f"Username 👤")
            st.code(f"{cred[1]}", language="python")
            st.text_input('Password 🔑', value=cred[2], type="password",)    
            st.markdown("####")
            url = cred[4]   
            if st.button('Launch 🚀', use_container_width=True):
                webbrowser.open_new_tab(url=url)                
        st.markdown('##')    
        with st.expander("Additional Details:"):
            st.text(f"email")
            st.code(f"{cred[3]}", language="python")
            st.text(f"URL")
            st.code(f"{cred[4]}", language="python")
    else:
        st.info('Database is Empty.', icon="ℹ️")

if radio_option=="Add Account": 
    st.subheader("Add New Credential 🗝️")
    st.markdown("####")    
    app_name = st.text_input('Application 📱', 'Twitter')
    user_name = st.text_input('User Name 👤', 'tweety')
    pass_word = st.text_input('Password 🔑', 'pass123', type="password",)
    email = st.text_input('Email 📧', 'tweety@xyz.com')
    url = st.text_input('Website 🔗', 'twitter.com')
    st.markdown("####")
    if st.button('Save ⏬', use_container_width=True):
        try:
            data = User(app_name, user_name, pass_word, email, url)
            insert_data(data)
            st.success(f"{app_name}'s credential is added to the Database!", icon="✅")
        except:
            st.warning('Something went wrong! Try Again.', icon="⚠️")
    st.markdown("####")
    st.info(f"Available Credentials in Database: {db_size}", icon="💾") 
    
if radio_option=="Update Password": 
    st.subheader("Update Password 🔄")
    st.markdown('#####')   
    if db_size>0: 
        up_app = st.selectbox('Select an Account you want to update 👇', app_names) 
        st.markdown('####')
        new_pass_1 = st.text_input('New Password ', 'new123', type="password",)
        new_pass_2 = st.text_input('Confirm New Password', 'new123', type="password",)
        if new_pass_1==new_pass_2:
                          
            if st.button('Update ⚡️', use_container_width=True):
                try:
                    update_password(up_app,new_pass_1)
                    st.success(f"{up_app}'s password is updated!", icon="✅")
                except:
                    st.info(' Database is Empty. Go to Create to add Data ⬅️', icon="ℹ️")    
        else:
            st.warning("Password don't match! Try Again.", icon="⚠️")
    else:
        st.info('Database is Empty.', icon="ℹ️")
   
if radio_option=="Delete Account":
    st.subheader("Delete Credential 🗑️")  
    st.markdown("#####")     
    if db_size>0: 
        agree = st.checkbox('View Full Database')
        if agree:
            c.execute("select app_name, email_address, url from pwd_mgr")
            results = c.fetchall()
            st.table(results)        
        st.markdown('#####')      
        delt = st.selectbox('Select an Account you want to delete 👇', app_names) 
        st.markdown('####')              
        if st.button('Delete ❌', use_container_width=True):
            try:
                remove_app_cred(delt)
                st.success(f"{delt}'s Credential is removed from Database!", icon="✅")
            except:
                st.info(' Database is Empty. Go to Create to add Data ⬅️', icon="ℹ️")             
    else:
        st.info('Database is Empty.', icon="ℹ️")
        