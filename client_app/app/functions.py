import requests, geocoder, datetime as dt, streamlit as st, altair as alt, shelve, pandas as pd, streamlit_option_menu as om, time, requests
from millify import millify
from datetime import datetime
crop_db = "crop_database"
livestock_db= "livestock_database"
inventory_db = "inventory_database"
# import geocoder
# import datetime as dt
# import streamlit as st
# import altair as alt
# import shelve
# import pandas as pd
# import streamlit_option_menu as om
# import time
# import requests

# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def format_number(number):
    if number == None:
        return None
    return "{:,}".format(number)
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------\
# Crop Class used under Crop.py / tab2
class class_crop:
    def __init__(self, type=None, import_date=None,prod_year=None, export_date=None, yield_amount=None,profit=None, prod_cost=None, export_cost=None):
        self.prod_year = prod_year
        self.type = type
        self.yield_amount = yield_amount
        self.export_cost = export_cost
        self.import_date = import_date
        self.prod_cost = prod_cost
        if export_cost != None:
            self.export = export_date
            self.user = "[User]"
        else:
            self.export = estimated_date(import_date, crop_dict[type])
            self.user  = "[Auto]"
        if export_cost != None and prod_cost != None:
            self.profit = cal_profit(export_cost=export_cost, production_cost=prod_cost)
        else:
            self.profit = profit
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
class class_livestock:
    def __init__(self, type, import_date, amount, prod_year,export_date=None, import_cost=None, export_cost=None,prod_cost=None, profit=None):
        self.prod_year = prod_year
        self.type = type
        self.import_date = import_date
        self.export_date = export_date
        self.livestock_amount = amount
        self.import_cost = import_cost
        self.export_cost = export_cost
        self.prod_cost = prod_cost
        if import_cost != None and export_cost != None:
            self.profit = cal_profit(import_cost=import_cost, export_cost=export_cost, production_cost=prod_cost)
        else:
            self.profit = profit
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
class class_inventory:
    def __init__(self, id, label, quantity, import_date):
        self.id = id
        self.label = label
        self.quantity = quantity
        self.import_date = import_date
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
inventory_dict={
    "Shovel",
    "Fertilizer",
    "Tractors",
    "Seed",
    "Pesticides",
    "Hoes",
    "Watering Cans",
    "Plough",
    "Sprayers",
    "Wheelbarrows",
}
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
livestock_dict = {
    "Goat": 1,
    "Sheep": 1,
    "Cattle": 1,
    "Cow": 1,
    "Chicken": 1,
    "Pig": 1,
    "Beehive": 1,
    "Fish": 1,
}
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
crop_dict = {  # Some pre-defined crops used to show the obtions and contains their average harvest peroid in days
    "Teff": 75,
    "Maize": 90,
    "Inset": 730,
    "Wheat": 91,
    "Sorghum": 110,
    "Corn": 80,
    "Barley": 130,
    "Rice": 150,
}
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
@st.cache_data()  # Store to catch
def get_weather(arg):
    try:
        g = geocoder.ip('me')
        city = g.city
        state = g.state
        country = g.country
        lat, lon = g.latlng
        # url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation"
        print("Your approximate location (latitude, longitude):", g.latlng)

        response = requests.get(url)
        data = response.json()
        weather = data["current_weather"]
        rainfall = sum(data["hourly"]["precipitation"][:12])

        if arg == "temp":
            return f"☀️ {round(weather["temperature"], 2)} °C"
        elif arg == "wind":
            return f"💨 {round(weather["windspeed"],2)} km/h"
        elif arg == "rainfall":
            return f"🌧️ {round(rainfall,2)} mm"
        elif arg == "station":
            return f"🏠 {city}"

        print("Open-Meteo Current Weather:")
        print(data["current_weather"])
        print(response)
        print(response)
        print(f"""
            City: {city}
            State: {state}
            Country: {country}
            Time: {weather['time']}
            Temp: {weather["temperature"]} °C
            Wind Speed: {weather["windspeed"]} km/h
            Rainfall: {rainfall} mm
        """)
        # lit.st.metric("Weather", weather["temperature"], -3)

    except Exception as e:
        print(
            "Error while Searching for weather, Try again when enternet is available !", e)
        return "—"
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
# Caculate Estimated Harvest Day
def estimated_date(current_date, add_days):

    def is_leap_year(year):  # Check for leap year, if found make feb 28 days else feb is 29 days
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    days_in_month = {  # Days for each month
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    day = current_date.day
    month = current_date.month
    year = current_date.year
    leap_year = False
    while add_days > 0:  # Calculate the day, month and year
        leap_year = True
        if month == 2 and is_leap_year(year) and leap_year:
            days_in_month[month] += 1
            leap_year = False
        if day < days_in_month[month]:
            day += 1
        else:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
        add_days -= 1
    # return the estimated date as datetime object
    print(year, month, day)
    date = dt.date(year, month, day)
    return date
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def cal_profit(export_cost, import_cost=None, production_cost=None):  #Profil Calculation
    if import_cost != None:
        return round(export_cost - (import_cost + production_cost),2)
    return round(export_cost - production_cost,2)
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def alter_graph(data_year, data_type, database, height): #
    with shelve.open(database) as db:
        # print(db[data_year][data_type].production_cost, db[data_year][data_type].export_cost, db[data_year][data_type].yield_amount, db[data_year][data_type].profit)
        try:
            df = pd.DataFrame({
                "Metric" : ["Prod","Sold","Yield","Profit" ],
                "Value" : [db[data_year][data_type].production_cost, db[data_year][data_type].export_cost, db[data_year][data_type].yield_amount, db[data_year][data_type].profit],
                "colors" :["#e74c3c","#3498db","#f1c40f", "#2ecc71"]    
        })
        except:
            df = pd.DataFrame({
                "Metric" : ["Purchase", "Prod.","Sold","Profit" ],
                "Value" : [db[data_year][data_type].import_cost, db[data_year][data_type].production_cost, db[data_year][data_type].export_cost, db[data_year][data_type].profit],
                "colors" :["#e74c3c", "#e74c3c","#3498db", "#2ecc71"]    
        })
    chart = alt.Chart(df).mark_bar().encode(

        x=alt.X("Metric:N", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
        y=alt.Y("Value:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
        color = alt.Color("colors:N", scale=None)
    ).properties(
        width=800,
        height=height,
    )
    return chart
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def percent_complete(data):
 
    try:
        start_date = data.import_date
        end_date = data.export_date
        
        print(type(start_date), start_date, end_date, id)
        total_days = (end_date - start_date).days
        current_date = datetime.now().date()
        days_passed = (current_date - start_date).days

        print(total_days, days_passed, current_date, start_date)
        if total_days == 0:
            day = 100
        else:
            day = min((days_passed / total_days) *100,100)

        return f"{int(day)} %"
    except:
        return None
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def render_nav(current_page, width):
    selected = current_page
    pages = {
    "main": "main.py",
    "Crop Data": "pages/Crop.py",
    "Livestock Data": "pages/LiveStock.py",
    "Inventory Data": "pages/Inventory.py",
    "About": "pages/About.py",
    }
    page_list = list(pages.keys())
    if width >= 1000:
        selected = om.option_menu(
                menu_title=None,
                options=page_list, 
                icons=["house", "bar-chart", "bar-chart", "bar-chart" ],
                default_index=page_list.index(current_page),
                orientation="horizontal",
                styles={"nav-link": {"text-align": "center", "margin": "0em", "--hover-color": "#676767"},
                
            }
         )
            
    if selected != current_page:
        st.switch_page(pages[selected])
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
@st.dialog("Add Data", width="medium")
def add_data(database,form_type):
    col1, col2 = st.columns(2)
    option_dict = crop_dict if database == crop_db else livestock_dict if database == livestock_db else inventory_dict
    with st.form(key=f"{form_type} info"):
        st.success("Mandatory Fields")
        if database == inventory_db:
                id = str(st.text_input("ID: ", placeholder="3 digit ID recommended", help="Unique ID for each inventory item"))
                label = st.selectbox(label="Label", options=[key for key in inventory_dict], help="Type of inventory item")
                import_date = st.date_input("Date: ", help="Date when the inventory item was added")
                quantity = st.number_input(label="Quantity", value=1, min_value=1, help="Quantity of the inventory item")
        else:
            with col1:
                st.success("Mandatory Fields")
                type = st.selectbox(label="Type", options=[key for key in option_dict],help="Type of {form_type}")
                if database == livestock_db:
                    amount = st.number_input(label="Amount", value=1, min_value=1, help="Number of livestock imported or bought")
                prod_year = st.text_input(label="Production Year", help="Production year, partial years like 2020/2021 are Allowed", placeholder="Production Year")
                import_date = st.date_input("Planted Date: ", help="Date when the {form_type} was imported")
                
            with col2:
                st.info("Non-Mandatory Fields")
                if database == crop_db:
                    export_date = st.date_input(label="Harvest Date: ",value=None,help="date of export. {If left empty, it will be calculated automatically")
                    yield_amount = st.number_input(label="Yield [kg]", value=None, min_value=0.0,help="Expected or Actual Yield amount in kg, if left empty, it will be set to None")
                    prod_cost = st.number_input(label="Production Cost", value=None, min_value=0.0, help="Cost of producing, e.g. seed price,fertilizer, water, etc.")
                    export_cost = st.number_input(label="Sold Price", value=None, min_value=0.0, help="Expected selling price of the crop")
                elif database == livestock_db:
                    import_cost = st.number_input(label="Purchase Cost", value=None, min_value=0.0, help="Cost of importing or buying the livestock")
                    export_cost = st.number_input(label="Sold Price", value=None, min_value=0.0, help="Sold price of the Livestock")
                    prod_cost = st.number_input(label="Production Cost", value=None, min_value=0.0, help="Cost of producing the crop, e.g. fertilizer, water, etc.")
                    export_date = st.date_input(label="Sold Date: ",value=None,help="estimated selling date, if left empty, it will be filled automatically")
                    
        submit = st.form_submit_button("Submit", type="primary", width='stretch')
        
        if submit: 
            condition = not all([type, import_date, submit, verify_production_year(prod_year)]) if database != inventory_db else not all([id, label, import_date, quantity, submit])
            if condition:  # check if every parameter is filled
                st.warning("Please Fill every Mandatory Fields")
            else:
                if database == crop_db:
                    data = dict(
                        type = type,
                        import_date=import_date, 
                        prod_year=prod_year,
                        export_date=export_date, 
                        yield_amount=yield_amount,
                        prod_cost=prod_cost,
                        export_cost = export_cost
                        )
                    save(database=database,type=type, data=data, prod_year=prod_year)
                elif database == livestock_db:
                    data = dict(
                        type=type,
                        import_date=import_date,
                        prod_year=prod_year,
                        amount=amount,
                        import_cost=import_cost,
                        export_cost=export_cost,
                        prod_cost=prod_cost,
                        export_date=export_date
                        )
                    save(database=database,type=type, data=data, prod_year=prod_year)
                elif database == inventory_db:
                    with shelve.open(database) as db:
                        if id not in db:
                            inventory = class_inventory(
                                id=id,
                                label=label,
                                import_date=import_date,
                                quantity=quantity
                                )
                            db[id] = inventory
                            st.success(f"Data Saved Successfully !", width="stretch")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Inventory ID is Taken")
                            st.warning("Try Using Another ID")

                
                # with shelve.open(database) as db:
                #     year_data = db.get(prod_year, {})
                #     if type in year_data:
                #         st.error(f"Cant Add an Already Existing Crop")
                #         st.warning(f"Please Check your Production Year or try editing")
                #     else:
                #         # year_data = db[production_year] if db[production_year] else db[production_year] = {}  # Get the dict for this year
                #         year_data[type] =  data # Add or update crop type
                #         db[prod_year] = year_data   # Save back to shelve
                #         st.success(f"Data Saved Successfully!", width="stretch")
                #         time.sleep(0.5)
                #         st.rerun()
    # if database == "livestock_database":
    #     with st.form(key="livestock info"):
    #         with col1:
    #             st.success("Mandatory Fields")
    #             livestock_type = st.selectbox(label="Type", options=[key for key in livestock_dict], help="Type of livestock")
    #             prod_year = st.text_input("Production Year")
    #             amount = st.number_input(label="Amount", value=1, min_value=1, help="Number of livestock imported or bought")
    #             date = st.date_input("Purchase Date: ",help="Date when the livestock was imported or bought")
    #         with col2:
    #             st.info("Non Mandatory Fields")
    #             import_cost = st.number_input(label="Purchase Cost", value=None, min_value=0.0, help="Cost of importing or buying the livestock")
    #             prod_cost = st.number_input(label="Production Cost", value=None, min_value=0.0, help="Cost of producing the crop, e.g. fertilizer, water, etc.")
    #             export_date = st.date_input(label="Sold Date: ",value=None,help="estimated selling date, if left empty, it will be filled automatically")
    #             export_cost = st.number_input(label="Sold Price", value=None, min_value=0.0, help="Expected selling price of the crop")
    #         submit = st.form_submit_button("Submit", type="primary", width='stretch')           
    #         if submit:  # Check if ID is taken or not
    #             if all([prod_year, livestock_type, date, amount, submit]) == False:  # check if every parameter is filled
    #                 st.warning("Please Fill every box")
    #             else:
    #                 with shelve.open(database) as db:
    #                     livestock_data = class_livestock(
    #                         type=livestock_type,
    #                         date=date,
    #                         prod_year=prod_year,
    #                         amount=amount,
    #                         import_cost=import_cost,
    #                         export_cost=export_cost,
    #                         prod_cost=prod_year,
    #                         export_date=export_date
    #                         )
    #                     year_data = db.get(prod_year, {})
    #                     if livestock_type in year_data:
    #                         st.error(f"Can't Add an Already Existing Livestock")
    #                         st.warning(f"Please Check your Production Year or try editing")
    #                     else:
    #                         year_data[livestock_type] =  livestock_data
    #                         db[prod_year] = year_data
    #                         st.success(f"Data Saved Successfully! ", width="stretch")
    #                         time.sleep(0.5)
    #                         st.rerun()             
    # if database == "inventory_database":
        # with st.form(key="inventory info"):
        #     st.success("Mandatory Fields 📌")
        #     id = str(st.text_input("ID: ", placeholder="3 digit ID recommended", help="Unique ID for each inventory item"))
        #     label = st.selectbox(label="Label", options=[key for key in inventory_dict], help="Type of inventory item")
        #     date = st.date_input("Date: ", help="Date when the inventory item was added")
        #     quantity = st.number_input(label="Quantity", value=1, min_value=1, help="Quantity of the inventory item")
        #     submit = st.form_submit_button("Submit", type="primary", width='stretch')           
        #     if submit:  # Check if ID is taken or not
        #         if all([id, label, date, quantity, submit]) == False:  # check if every parameter is filled
        #             st.warning("Please Fill every box")
        #         else:
        #             with shelve.open(database) as db:
        #                 if id not in db:
        #                     inventory = class_inventory(
        #                         id=id,
        #                         label=label,
        #                         date=date,
        #                         quantity=quantity
        #                         )
        #                     db[id] = inventory
        #                     st.success(f"Data Saved Successfully !", width="stretch")
        #                     time.sleep(0.5)
        #                     st.rerun()
        #                 else:
        #                     st.error("Inventory ID is Taken")
        #                     st.warning("Try Using Another ID")
     
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def save(database, prod_year, type, data):
    if database == crop_db:
        class_data = class_crop(**data)
    elif database == livestock_db:
        class_data = class_livestock(**data)
    with shelve.open(database) as db:
        prod_year_data = db.get(prod_year, {})
        if type in prod_year_data:
            st.error(f"Warning: Type Already Exists.")
            st.warning(f"Please Check your Production Year or try editing")
        else:
            prod_year_data[type] =  class_data
            db[prod_year] = prod_year_data
            st.success(f"Data Saved Successfully! ", width="stretch")
            time.sleep(0.5)
            st.rerun()

     
        

        
        



def verify_production_year(yr):
    if ("/" not in  yr and len(yr) == 4) or ("/" in yr and len(yr) == 9):
        return True
    else:
        return False
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
@st.dialog("Update / Edit Data")
def edit(database=None, edit_id=None, edit_year=None, edit_type=None):
    if database == "crop_database":
        with st.form(key="crop edit"):
                with shelve.open(database, writeback=True) as db:
                # Collect Crop Informatioln
                    # new_id = str(st.text_input("ID", placeholder="3 digit ID recommended", value=db[edit_id].id))
                    new_type = st.selectbox(label="Type", options=[key for key in crop_dict], index=[key for key in crop_dict].index(db[edit_year][edit_type].type))
                    new_date = st.date_input("Planted Date", value=db[edit_year][edit_type].date)
                    new_production_year = st.text_input("Production year", value=db[edit_year][edit_type].production_year, disabled=True)
                    new_estimated = st.date_input(label="Expected Harvest", value=db[edit_year][edit_type].estimated)
                    new_yield_price = st.number_input(label="Yield[kg]", value=db[edit_year][edit_type].yield_amount)
                    new_production_cost = st.number_input(label = "Production Cost [Birr]", value=db[edit_year][edit_type].production_cost)
                    new_exported_price = st.number_input(label="Sold Price [Birr]", value=db[edit_year][edit_type].export_cost)
                    
                    submit_edit = st.form_submit_button(width="stretch")
                    if submit_edit:
                        if not all([new_production_year, new_type, new_date, submit_edit]):  # check if every parameter is filled
                            st.warning("Please Fill every box")
                        if not (new_type in db[edit_year] and new_type != edit_type):
                            if new_type != edit_type :
                                del db[edit_year][edit_type]
                            new_crop = class_crop(prod_year=new_production_year,type=new_type, date=new_date, yield_amount=new_yield_price, estimated=new_estimated, export_cost=new_exported_price, prod_cost=new_production_cost)
                            db[edit_year][new_type] = new_crop
                            st.success(f"Changes Saved Successfully!", width="stretch")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.warning("Crop Type Already Taken")
    
    elif database == "livestock_database":
        with st.form(key="Livestock edit"):
                with shelve.open(database, writeback=True) as db:
                # Collect Crop Informatioln
                    new_type = st.selectbox(label="Type", options=[key for key in livestock_dict], index=[key for key in livestock_dict].index(db[edit_year][edit_type].type))
                    new_date = st.date_input("Bought  Date", value=db[edit_year][edit_type].date)
                    new_production_year = st.text_input("Production year", value=db[edit_year][edit_type].production_year, disabled=True)
                    new_amount = st.number_input("Amount Bought", min_value=1, value=db[edit_year][edit_type].amount)
                    new_export_date = st.date_input(label="Estimated", value=db[edit_year][edit_type].export_date)
                    new_import_price = st.number_input(label="Bought Price [Birr]", value=db[edit_year][edit_type].import_cost)
                    new_exported_price = st.number_input(label="Sold Price [Birr]", value=db[edit_year][edit_type].export_cost)
                    new_production_cost = st.number_input(label = "Production Cost [Birr]", value=db[edit_year][edit_type].production_cost)
                    submit_edit = st.form_submit_button(width="stretch")
                    if submit_edit:
                        if not all([new_production_year, new_type, new_date, submit_edit]):  # check if every parameter is filled
                            st.warning("Please Fill every box")
                        if not (new_type in db[edit_year] and new_type != edit_type):
                            if new_type != edit_type :
                                del db[edit_year][edit_type]
                            new_livestock = class_livestock(
                            type=new_type,
                            date=new_date,
                            prod_year=new_production_year,
                            amount=new_amount,
                            import_cost=new_import_price,
                            export_date=new_export_date,
                            export_cost=new_exported_price,
                            prod_cost=new_production_cost)
                            db[edit_year][new_type] = new_livestock
                            st.success(f"Changes Saved Successfully", width="stretch")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.warning("ID Already Taken")
    
    elif database == "inventory_database":
        with st.form(key="Inventory edit"):
                with shelve.open(database) as db:
                # Collect Crop Informatioln
                    new_id = str(st.text_input("ID", placeholder="3 digit ID recommended", value=db[edit_id].id))
                    new_label = st.selectbox(label="Label", options=[key for key in inventory_dict], index=[key for key in inventory_dict].index(db[edit_id].label))
                    new_date = st.date_input("Date", value=db[edit_id].date)
                    new_quantity = st.number_input("Quantity", min_value=1, value=db[edit_id].quantity)
                    submit_edit = st.form_submit_button(width="stretch")
                    if submit_edit:
                        if not all([new_id, new_label, new_date, new_quantity, submit_edit]):  # check if every parameter is filled
                            st.warning("Please Fill every box")
                        if not (new_id in db and new_id!= edit_id):
                            if new_id != edit_id:
                                del db[edit_id]
                            new_inventory = class_inventory(
                                id=new_id,
                                label=new_label,
                                date=new_date,
                                quantity=new_quantity)
                            db[new_id] = new_inventory
                            st.success(f"Changes Saved Successfully!", width="stretch")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.warning("ID Already Taken")
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
@st.dialog("Delete Data Permenantly🚨")
def delete(database, del_year, del_type=None):
    with shelve.open(database, writeback=True) as db:
        if database == "inventory_database":
            st.write(f"Are you sure you want to delete data {del_year} of label {db[del_year].label} ? ?")
        else: st.write(f"Are you sure you want to delete data  of type {del_type} ?")
        st.error("This action is irreversible! ⚠️", width="stretch")
        confirm = st.button("Confirm Delete", type="primary", width="stretch", icon=":material/delete:", help="This action is irreversible")
        if confirm:
            if database == "inventory_database": del db[del_year]
            else:
                del db[del_year][del_type]
                if not db[del_year]:
                    del db[del_year]
            st.success("Deleted Successfully", width="stretch")
            time.sleep(1)
            st.rerun()
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
@st.dialog("Welcome to Agro-Board")
def configuration(arg = None):
    with st.container(border=True):
        st.info("Fill out the following to set up your app")
        name = st.text_input("Name", placeholder="Enter your full name", help="This is used to personalize the app")
        kebele = st.selectbox("Qabale",options=["01", "02"], placeholder="Your current Qabale")
        land_area = st.number_input("Argicultural Land Area [Ha]", min_value=0.00, help="Your Average Agricultural Land Area in Hectars", value=0.00)
        if st.button("Get Serial Number /REGISTER/", help="Your special SN that identifies you to higher authorities", width="stretch"):
            if all([name, kebele]):
                SN = requests.get(f"http://127.0.0.1:8000/client/register/{name}")
                if SN:
                    sn = SN.json()
                    st.success(f"Successfully Registered: SN: {sn["SN"]}")
                    with shelve.open("config") as db:
                        db["SN"] = sn["SN"]
                    with shelve.open("config", writeback=True) as db:
                        db["name"] = name
                        db["kebele"] = kebele
                        db["land_area"] = float(land_area)
                    st.success("Saved Successfully", width="stretch")
                    time.sleep(1)
                    st.rerun()
            else:
                st.info("Please Fill Every Parameter")

    return None
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def get_config(arg):
    with shelve.open("config") as config:
        return config[arg]
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
@st.dialog("Upload Data")
def package_data():
    with st.form("Upload Data"):
        st.info("Data to Upload", width="stretch")
        crop_confirm = st.checkbox("Crop Data", value=True)
        livestock_confirm = st.checkbox("LiveStock Data", value=True)
        submit = st.form_submit_button("Send To Server",width="stretch")
    if submit:
        crop_data = {}
        livestock_data = {}
        
        if crop_confirm:
            with shelve.open("crop_database") as db:
                crop_type_dict = {}
                years = [year for year in db]
                ordered_year_list = sort_years(list(set(years)))
                for yr in ordered_year_list:
                    for production_year in db:
                        if production_year != yr:
                            continue
                        year_dict = {}
                        year_dict[yr] = {}
                        for crop_type in db[yr]:
                            crop = db[yr][crop_type]
                            crop_type_dict = {crop_type:{
                                "Planted Date" : crop.date.isoformat() if hasattr(crop.date, "isoformat") else str(crop.date),
                                "Harvested Date": crop.estimated.isoformat() if hasattr(crop.estimated, "isoformat") else str(crop.estimated),
                                "Yield" : crop.yield_amount,
                                "Export Cost": crop.export_cost,
                                "Production Cost": crop.production_cost,
                                "Profit": crop.profit
                                }
                            }
                            year_dict[yr].update(crop_type_dict)
                        crop_data.update(year_dict)
        if livestock_confirm:
            livestock_data = {}
            with shelve.open("livestock_database") as db:
                livestock_type_dict = {}
                years = [year for year in db]
                ordered_year_list = sort_years(list(set(years)))
                for yr in ordered_year_list:
                    for production_year in db:
                        if production_year != yr:
                            continue
                        year_dict = {}
                        year_dict[yr] = {}
                        for livestock_type in db[yr]:
                            livestock = db[yr][livestock_type]
                            livestock_type_dict = {livestock_type:{
                                "Imported Date": livestock.date.isoformat() if hasattr(livestock.date, "isoformat") else str(livestock.date),
                                "Export Date": livestock.date.isoformat() if hasattr(livestock.export_date, "isoformat") else str(livestock.export_date),
                                "Amount": livestock.amount,
                                "Import Cost": livestock.import_cost,
                                "Export Cost": livestock.export_cost,
                                "Production Cost": livestock.production_cost,
                                "Profit": livestock.profit
                                }
                            }
                            year_dict[yr].update(livestock_type_dict)
                        livestock_data.update(year_dict)
            
        # print(crop_data)
        
        payload = {
        "SN" : get_config("SN"),
        "name": get_config("name"),
        "land_area" : 0 if get_config("land_area") == None else get_config("land_area"),
        "kebele": get_config("kebele"),
        "crop_data": crop_data,
        "livestock_data":livestock_data
        }
        try:
            post = requests.post("http://127.0.0.1:8000/client/upload", json=payload)
            if post:
                try:
                    post = post.json()
                    st.success(f"{post['msg']}")
                except:
                    st.error(f"Couldn't Reach Server! Try Again Later")
        except:
            st.error("Something Unexpected Happened! Please Check you internet and try again later")
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def sort_years(year_list) -> list:
    """ 
        takes list of years and sorts them in decending order.
        Parameters:
        year_list: str - non-dublicated  
    """
    def sort_key(year_str):
        year_str = str(year_str)
        parts = year_str.split('/') 
        first = int(parts[0])
        second = int(parts[1]) if len(parts) > 1 else first
        # For single years, second == first, so they come before ranges
        return (first, second)
    year_list = list(set(year_list))
    return sorted(year_list, key=sort_key, reverse=True)
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
@st.dialog("Edit Configuration")
def edit_config():
    with shelve.open("config", writeback=True) as db:
        with st.form("edit Config"):
            st.text_input("Serail Number",placeholder=f"{db["SN"]}",disabled=True)
            st.selectbox("Qabale",options=[get_config('kebele')], placeholder="Your current Qabale", disabled=True, )
            new_name = st.text_input("Name", placeholder="Enter your full name", help="This is used to personalize the app", value=db["name"])            
            new_land_area = st.number_input("Argicultural Land Area [Ha]", min_value=0.00, help="Your Average Agricultural Land Area in Hectars", value= db["land_area"])
            submit = st.form_submit_button("Save Changes",width="stretch")
            if submit:
                db["name"] = new_name
                db["land_area"] = new_land_area
                st.success("Changes Successfully Saved !")
                time.sleep(1)
                st.rerun()
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def check_sn():
    try:
        with shelve.open("config") as db:
            sn = db["SN"]
            return False
    except: return True
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================

def display_graph(database, filter_on=False):
    with shelve.open(database) as db:
        filtered_prod_year_list = filter_by_prod_year(database) if filter_on == True else [prod_years for prod_years in db]
    i = 0
    heights = [220,260, 220, 260]
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    
    with shelve.open(database) as db:
        # filtered_prod_year_list = filter_by_prod_year(database) if filter_on== True else [prod_years for prod_years in db]
        for prod_year in filtered_prod_year_list:
            prod_year_data = db[prod_year]
            for data_type in prod_year_data:
                data = prod_year_data[data_type]
                height = heights[i]
                
                amount = data.yield_amount if database == crop_db else data.amount
                yield_value =  None if amount == None else millify(amount,precision=1)
                with cols[i]:
                    with st.container(border=True):
                        left, right = st.columns(2)
                        with left:
                            st.metric(label=f"{prod_year}", value = f"{data_type}",width="stretch")
                        with right:
                            right_label = "Crop Yiled[KG]" if database == crop_db else "Livestock Amount"
                            st.metric(label=right_label, value = yield_value, width="stretch")
                        st.altair_chart(alter_graph(data_year = prod_year,data_type=data_type, database=database, height=height), use_container_width=True)
                        first_date = data.date
                        last_date = data.estimated if database == crop_db else data.export_date
                        st.button(f"**{data.date} -- {data.estimated if database == crop_db else data.export_date}**", 
                                width="stretch", type="tertiary", 
                                key = f"{prod_year}{data_type}")
                if i >= 3:
                    i = 0
                    heights = heights[::-1]
                else: i += 1



def filter_by_prod_year(database):
    with shelve.open(database) as db:
        years = [key for key in db] # extract all the production years from db
        year_list = sort_years(years) # sort years in decending order
        # collect user selected years into a list, remove dublicates and sort in decending order
        # Only allow user to select existing years
        selected_year_list = st.multiselect("Filter By Year", options=year_list, default=year_list, key=f"{database} filter")
        selected_year_list = sort_years(selected_year_list)
    return selected_year_list
