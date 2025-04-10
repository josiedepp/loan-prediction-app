# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import pickle  # to load a saved model
import base64  # to open .gif files in streamlit app (optional)

# Caching to improve performance
@st.cache(suppress_st_warning=True)
def get_fvalue(val):
    feature_dict = {"No": 1, "Yes": 2}
    for key, value in feature_dict.items():
        if val == key:
            return value

def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value

# Sidebar page selector
app_mode = st.sidebar.selectbox('Select Page', ['Home', 'Prediction'])

if app_mode == 'Home':
    st.title('LOAN PREDICTION :)')

    # Load and display image
    st.image('loan_image.jpg')  # Make sure this image is in the same folder as your .py file

    st.markdown('### Dataset :')
    
    # Load the dataset
    data = pd.read_csv('test.csv')  # Replace with 'loan_dataset.csv' if that's your actual file
    st.write(data.head())  # Show top rows of the data

    # Plot bar chart
    st.markdown('### Applicant Income VS Loan Amount')
    st.bar_chart(data[['ApplicantIncome', 'LoanAmount']].head(20))

elif app_mode == 'Prediction':
    st.subheader("Sir/Mme, YOU need to fill all necessary information in order to get a reply to your loan request!")

    st.sidebar.header("Informations about the client :")

    # Dictionaries to map input values
    gender_dict = {"Male": 1, "Female": 2}
    feature_dict = {"No": 1, "Yes": 2}
    edu = {"Graduate": 1, "Not Graduate": 2}
    prop = {"Rural": 1, "Urban": 2, "Semiurban": 3}

    # Sidebar inputs
    gender_dict = {"Male":1,"Female":2}
    feature_dict = {"No":1,"Yes":2}
    edu={'Graduate':1,'Not Graduate':2}
    prop={'Rural':1,'Urban':2,'Semiurban':3}
    ApplicantIncome=st.sidebar.slider('ApplicantIncome',0,10000,0,)
    CoapplicantIncome=st.sidebar.slider('CoapplicantIncome',0,10000,0,)
    LoanAmount=st.sidebar.slider('LoanAmount in K$',9.0,700.0,200.0)
    Loan_Amount_Term = st.sidebar.selectbox('Loan Amount Term', 
        (12.0, 36.0, 60.0, 84.0, 120.0, 180.0, 240.0, 300.0, 360.0))
    Credit_History = st.sidebar.radio('Credit_History', (0.0, 1.0))
    Gender=st.sidebar.radio('Gender',tuple(gender_dict.keys()))
    Married=st.sidebar.radio('Married',tuple(feature_dict.keys()))
    Self_Employed=st.sidebar.radio('Self Employed',tuple(feature_dict.keys()))
    Dependents=st.sidebar.radio('Dependents',options=['0','1' , '2' , '3+'])
    Education=st.sidebar.radio('Education',tuple(edu.keys()))
    Property_Area = st.sidebar.radio('Property Area', tuple(prop.keys()))

    # Convert Dependents into dummy variables
    class_0, class_1, class_2, class_3 = 0, 0, 0, 0
    if Dependents == '0':
        class_0 = 1
    elif Dependents == '1':
        class_1 = 1
    elif Dependents == '2':
        class_2 = 1
    elif Dependents == '3+':
        class_3 = 1

    # Convert Property_Area into dummy variables
    Rural, Urban, Semiurban = 0.0, 0.0, 0.0
    if Property_Area == 'Urban':
        Urban = 1.0
    elif Property_Area == 'Semiurban':
        Semiurban = 1.0
    else:
        Rural = 1.0

    data1={
    'Gender':Gender,
    'Married':Married,
    'Dependents':[class_0,class_1,class_2,class_3],
    'Education':Education,
    'ApplicantIncome':ApplicantIncome,
    'CoapplicantIncome':CoapplicantIncome,
    'Self Employed':Self_Employed,
    'LoanAmount':LoanAmount,
    'Loan_Amount_Term':Loan_Amount_Term,
    'Credit_History':Credit_History,
    'Property_Area':[Rural,Urban,Semiurban],
    }

    feature_list=[ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,get_value(Gender,gender_dict),get_fvalue(Married),data1['Dependents'][0],data1['Dependents'][1],data1['Dependents'][2],data1['Dependents'][3],get_value(Education,edu),get_fvalue(Self_Employed),data1['Property_Area'][0],data1['Property_Area'][1],data1['Property_Area'][2]]

    single_sample = np.array(feature_list).reshape(1,-1)

    if st.button("Predict"):
    # Load GIFs
    file_ = open("6m-rain.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    file = open("green-cola-no.gif", "rb")
    contents = file.read()
    data_url_no = base64.b64encode(contents).decode("utf-8")
    file.close()

    # Load model and predict
    loaded_model = pickle.load(open('RF.sav', 'rb'))
    prediction = loaded_model.predict(single_sample)

    # Show results
    if prediction[0] == 0:
        st.error("According to our Calculations, you will not get the loan from Bank")
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url_no}" alt="no gif">',
            unsafe_allow_html=True
        )
    elif prediction[0] == 1:
        st.success("Congratulations!! You will get the loan from Bank")
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="yes gif">',
            unsafe_allow_html=True
        )


