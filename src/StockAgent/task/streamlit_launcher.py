import streamlit.web.bootstrap

SCRIPT_PATH = 'streamlit_preparing.py'  # The file with your dashboard code
args = []
flag_options = {'browser.gatherUsageStats': False}

streamlit.web.bootstrap.run(SCRIPT_PATH, '', args, flag_options)