import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Define the file path
FILE_PATH = "clothes_data.csv"

# Load data
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=[
            "Name", "Date", "Time", "Shirts", "Pants", "T-shirts", 
            "Sarees", "Dresses", "Dry_clean_shirts", "Others", "Total_Clothes", "Payment_Status"
        ])

# Save data
def save_data(data):
    data.to_csv(FILE_PATH, index=False)

# Main application
st.title("Clothes Ironing Tracker")

# Navigation menu
menu = st.sidebar.radio("Menu", ["Home", "Update Data"])

# Load current data
data = load_data()

if menu == "Home":
    st.header("Add New Entry")
    with st.form("new_entry"):
        name = st.text_input("Cloths given by:")
        date = st.date_input("Date", datetime.now())
        time = st.time_input("Time")  # Manual time input widget, no default time set
        shirts = st.number_input("Number of shirts given", min_value=0, value=0, step=1)
        pants = st.number_input("Number of pants given", min_value=0, value=0, step=1)
        tshirts = st.number_input("Number of t-shirts given", min_value=0, value=0, step=1)
        sarees = st.number_input("Number of sarees given", min_value=0, value=0, step=1)
        dresses = st.number_input("Number of dresses given", min_value=0, value=0, step=1)
        dry_clean_shirts = st.number_input("Number of shirts/blazers given for dry cleaning", min_value=0, value=0, step=1)
        others = st.number_input("Number of other items given", min_value=0, value=0, step=1)
        total_clothes = shirts + pants + tshirts + sarees + dresses + dry_clean_shirts + others
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            new_entry = {
                "Name": name,
                "Date": date.strftime("%Y-%m-%d"),
                "Time": time.strftime("%I:%M %p"),  # Format the entered time as HH:MM AM/PM
                "Shirts": shirts,
                "Pants": pants,
                "T-shirts": tshirts,
                "Sarees": sarees,
                "Dresses": dresses,
                "Dry_clean_shirts": dry_clean_shirts,
                "Others": others,
                "Total_Clothes": total_clothes,
                "Payment_Status": "Pending"
            }
            data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
            save_data(data)
            st.success("Entry added successfully!")
            st.experimental_rerun()  # Refresh the app to show updated data

    st.header("Manage Data")
    st.dataframe(data)

    # Delete existing data
    delete_index = st.multiselect("Select rows to delete:", data.index)
    if st.button("Delete Selected Rows"):
        if delete_index:
            data = data.drop(delete_index).reset_index(drop=True)
            save_data(data)
            st.success("Selected rows deleted successfully!")
            st.experimental_rerun()  # Refresh the app to show updated data
        else:
            st.warning("No rows selected for deletion.")

    st.download_button("Download Data as Excel", data.to_csv(index=False), "clothes_data.csv", "text/csv")

elif menu == "Update Data":
    st.header("Update Existing Data")
    if data.empty:
        st.info("No data available to update.")
    else:
        with st.form("update_form"):
            selected_date = st.date_input("Select Date to Update", datetime.now())
            filtered_data = data[data["Date"] == selected_date.strftime("%Y-%m-%d")]
            
            if not filtered_data.empty:
                st.write("Records for the selected date:")
                st.dataframe(filtered_data)
                
                updated_status = st.text_input("Update Payment Status (e.g., Paid/Not Paid):")
                submitted = st.form_submit_button("Update")
                if submitted:
                    data.loc[data["Date"] == selected_date.strftime("%Y-%m-%d"), "Payment_Status"] = updated_status
                    save_data(data)
                    st.success("Data updated successfully!")
                    st.experimental_rerun()  # Refresh the app to show updated data
            else:
                st.warning("No records found for the selected date.")
