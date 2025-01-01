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
            "Sarees", "Dresses", "Dry_clean_shirts", "Others", "Total_Clothes", 
            "Payment_Status", "Received_By", "Received_Date", 
            "Shirts_Received", "Pants_Received", "T-shirts_Received", 
            "Sarees_Received", "Dresses_Received", "Dry_clean_shirts_Received", 
            "Total_Clothes_Received"
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
                "Payment_Status": "Pending",
                "Received_By": "",
                "Received_Date": "",
                "Shirts_Received": 0,
                "Pants_Received": 0,
                "T-shirts_Received": 0,
                "Sarees_Received": 0,
                "Dresses_Received": 0,
                "Dry_clean_shirts_Received": 0,
                "Total_Clothes_Received": 0
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
        # Form for selecting the date to retrieve data
        with st.form("update_date_form"):
            selected_date = st.date_input("Select Date to Update", datetime.now())
            retrieve_data = st.form_submit_button("Retrieve Data")

        if retrieve_data:
            filtered_data = data[data["Date"] == selected_date.strftime("%Y-%m-%d")].reset_index()
            if not filtered_data.empty:
                st.write("Records for the selected date:")
                st.dataframe(filtered_data)

                # Form to edit and update data row-wise
                with st.form("edit_data_form"):
                    row_to_update = st.selectbox("Select Row to Update", filtered_data.index)
                    updated_name = st.text_input("Name", filtered_data.at[row_to_update, "Name"])
                    updated_payment_status = st.text_input("Payment Status", filtered_data.at[row_to_update, "Payment_Status"])
                    received_by = st.text_input("Name of the person who received the clothes", 
                                                filtered_data.at[row_to_update, "Received_By"])
                    received_date = st.date_input("Date when clothes were received", datetime.now())
                    shirts_received = st.number_input("Number of shirts received", 
                                                       value=filtered_data.at[row_to_update, "Shirts_Received"], step=1)
                    pants_received = st.number_input("Number of pants received", 
                                                      value=filtered_data.at[row_to_update, "Pants_Received"], step=1)
                    tshirts_received = st.number_input("Number of T-shirts received", 
                                                        value=filtered_data.at[row_to_update, "T-shirts_Received"], step=1)
                    sarees_received = st.number_input("Number of sarees received", 
                                                      value=filtered_data.at[row_to_update, "Sarees_Received"], step=1)
                    dresses_received = st.number_input("Number of dresses received", 
                                                       value=filtered_data.at[row_to_update, "Dresses_Received"], step=1)
                    dry_clean_shirts_received = st.number_input("Number of dry-clean shirts received", 
                                                                 value=filtered_data.at[row_to_update, "Dry_clean_shirts_Received"], step=1)

                    total_clothes_received = (shirts_received + pants_received + tshirts_received + sarees_received + 
                                               dresses_received + dry_clean_shirts_received)

                    update_submit = st.form_submit_button("Update Selected Row")

                    if update_submit:
                        row_index = filtered_data.at[row_to_update, "index"]  # Map back to original index
                        data.at[row_index, "Name"] = updated_name
                        data.at[row_index, "Payment_Status"] = updated_payment_status
                        data.at[row_index, "Received_By"] = received_by
                        data.at[row_index, "Received_Date"] = received_date.strftime("%Y-%m-%d")
                        data.at[row_index, "Shirts_Received"] = shirts_received
                        data.at[row_index, "Pants_Received"] = pants_received
                        data.at[row_index, "T-shirts_Received"] = tshirts_received
                        data.at[row_index, "Sarees_Received"] = sarees_received
                        data.at[row_index, "Dresses_Received"] = dresses_received
                        data.at[row_index, "Dry_clean_shirts_Received"] = dry_clean_shirts_received
                        data.at[row_index, "Total_Clothes_Received"] = total_clothes_received
                        save_data(data)
                        st.success("Data updated successfully!")
                        st.experimental_rerun()  # Refresh the app to show updated data
            else:
                st.warning("No records found for the selected date.")
