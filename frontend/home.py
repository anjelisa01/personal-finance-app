import streamlit as st
import requests
st.title("Personal Finance APP")

col1, col2 = st.columns(2)
with col1:
    st.text("Track your budgetting the easy way")
    if st.button("Signup to get started"):
        st.switch_page("pages/signup.py")

with col2:
    st.text("Already have an account?")
    if st.button("Sign in to your account"):
        st.switch_page("pages/login.py")




# animal_shelter = ['cat', 'dog', 'rabbit', 'bird']

# animal = st.text_input('Type an animal')

# if st.button('Check availability'):
#     have_it = animal.lower() in animal_shelter
#     'We have that animal!' if have_it else 'We don\'t have that animal.'