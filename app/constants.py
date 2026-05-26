from datetime import date

GENDER_OPTIONS = ("Male", "Female")
AGE_LIMIT = [0, 80]
STREAMLIT = "https://docs.streamlit.io/"
YEAR_LIST = [year for year in range(2000, date.today().year + 5)][::-1]
FILTER_BY_OPTIONS = ("Production Year", "Profit", "Yield", ) 
