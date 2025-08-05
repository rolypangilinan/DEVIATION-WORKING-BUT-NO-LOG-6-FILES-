#%%

import pandas as pd
import time
import os
from datetime import datetime

# Tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import VariableManager as varMan

def ReadFiles():
    global df

    pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    # --- Load data ---
    # file_path = r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv" #ORIGINAL PATH
    file_path = r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv"   # DESKTOP FALSE TESTING

    df = pd.read_csv(file_path, encoding='latin1')
    df = df[(~df["MODEL CODE"].isin(['60CAT0203M']))]
    df = df[(~df["MODEL CODE"].isin(["60CAT0202P"]))]
    df = df[(~df["MODEL CODE"].isin(["60CAT0203P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FC00000P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FC00902P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FC00903P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FC00905P"]))]
    df = df[(~df["MODEL CODE"].isin(["60FCXP001P"]))]
    df = df[(~df["MODEL CODE"].isin(["30FCXP001P"]))]
    df = df[(~df["PASS/NG"].isin([0]))]

    # NO NEED TO EDIT (CONSTANT)
    # --- CLEANING before loop ---
    df['S/N'] = df['S/N'].astype(str)
    df['MODEL CODE'] = df['MODEL CODE'].astype(str)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE'])
    df = df[df['S/N'].str.len() >= 8]
    df = df[~df['MODEL CODE'].str.contains('M')]
    today = pd.Timestamp.now().normalize()
    group_counts = df.groupby(['MODEL CODE', 'DATE']).size().reset_index(name='COUNT')
    valid_groups = group_counts[(group_counts['COUNT'] >= 10) | (group_counts['DATE'] == today)][['MODEL CODE', 'DATE']]
    df = df.merge(valid_groups, on=['MODEL CODE', 'DATE'], how='inner')

def EmptyColumnCreator():
    global compiledFrame

    # --- Blank frame ---
    emptyColumn = [
        "DATE", 
        "TIME", 
        "MODEL CODE", 
        "S/N", 
        "PASS/NG",
        "VOLTAGE MAX (V)", 
        "V_MAX PASS", 
        "AVE V_MAX PASS",                   
        "DEV V_MAX PASS",
        "WATTAGE MAX (W)",
        "WATTAGE MAX PASS",
        "AVE WATTAGE MAX (W)",                  
        "DEV WATTAGE MAX (W)",
        "CLOSED PRESSURE_MAX (kPa)",
        "CLOSED PRESSURE_MAX PASS",
        "AVE CLOSED PRESSURE_MAX (kPa)",        
        "DEV CLOSED PRESSURE_MAX (kPa)", 
        "VOLTAGE Middle (V)",
        "VOLTAGE Middle PASS",                  
        "AVE VOLTAGE Middle (V)",
        "DEV VOLTAGE Middle (V)",
        "WATTAGE Middle (W)",
        "WATTAGE Middle (W) PASS",              
        "AVE WATTAGE Middle (W)",
        "DEV WATTAGE Middle (W)",
        "AMPERAGE Middle (A)",
        "AMPERAGE Middle (A) PASS",             
        "AVE AMPERAGE Middle (A)",
        "DEV AMPERAGE Middle (A)",
        "CLOSED PRESSURE Middle (kPa)",
        "CLOSED PRESSURE Middle (kPa) PASS",    
        "AVE CLOSED PRESSURE Middle (kPa)",
        "DEV CLOSED PRESSURE Middle (kPa)",
        "VOLTAGE MIN (V)",
        "VOLTAGE MIN (V) PASS",                 
        "AVE VOLTAGE MIN (V)",
        "DEV VOLTAGE MIN (V)",
        "WATTAGE MIN (W)",
        "WATTAGE MIN (W) PASS",                 
        "AVE WATTAGE MIN (W)",
        "DEV WATTAGE MIN (W)",
        "CLOSED PRESSURE MIN (kPa)",
        "CLOSED PRESSURE MIN (kPa) PASS",       
        "AVE CLOSED PRESSURE MIN (kPa)",
        "DEV CLOSED PRESSURE MIN (kPa)"
    ]
    compiledFrame = pd.DataFrame(columns=emptyColumn)

def PopulateContent():
    global model_summary
    global compiledFrame

    dataList = []

    # --- Custom loop FIRST (to populate compiledFrame) ---
    for a in range(len(df)):
        # print(f"ROW: {a}")
        tempdf = df.iloc[[a]]
        model_code = tempdf["MODEL CODE"].values[0]

        dataFrame = {
            "DATE": tempdf["DATE"].values[0],
            "TIME": tempdf["TIME"].values[0],
            "MODEL CODE": model_code,
            "S/N": tempdf["S/N"].values[0],
            "PASS/NG": tempdf["PASS/NG"].values[0],
            "VOLTAGE MAX (V)": tempdf["VOLTAGE MAX (V)"].values[0],
            "WATTAGE MAX (W)": tempdf["WATTAGE MAX (W)"].values[0],
            "CLOSED PRESSURE_MAX (kPa)": tempdf["CLOSED PRESSURE_MAX (kPa)"].values[0],
            "VOLTAGE Middle (V)": tempdf["VOLTAGE Middle (V)"].values[0],
            "WATTAGE Middle (W)": tempdf["WATTAGE Middle (W)"].values[0],
            "AMPERAGE Middle (A)": tempdf["AMPERAGE Middle (A)"].values[0],
            "CLOSED PRESSURE Middle (kPa)": tempdf["CLOSED PRESSURE Middle (kPa)"].values[0],
            "VOLTAGE MIN (V)": tempdf["VOLTAGE MIN (V)"].values[0],
            "WATTAGE MIN (W)": tempdf["WATTAGE MIN (W)"].values[0],
            "CLOSED PRESSURE MIN (kPa)": tempdf["CLOSED PRESSURE MIN (kPa)"].values[0]
        }

        if tempdf["PASS/NG"].values[0] == 1:
            dataFrame["V_MAX PASS"] = tempdf["VOLTAGE MAX (V)"].values[0]
            dataFrame["WATTAGE MAX PASS"] = tempdf["WATTAGE MAX (W)"].values[0]
            dataFrame["CLOSED PRESSURE_MAX PASS"] = tempdf["CLOSED PRESSURE_MAX (kPa)"].values[0]
            dataFrame["VOLTAGE Middle PASS"] = tempdf["VOLTAGE Middle (V)"].values[0]
            dataFrame["WATTAGE Middle (W) PASS"] = tempdf["WATTAGE Middle (W)"].values[0]
            dataFrame["AMPERAGE Middle (A) PASS"] = tempdf["AMPERAGE Middle (A)"].values[0]
            dataFrame["CLOSED PRESSURE Middle (kPa) PASS"] = tempdf["CLOSED PRESSURE Middle (kPa)"].values[0]
            dataFrame["VOLTAGE MIN (V) PASS"] = tempdf["VOLTAGE MIN (V)"].values[0]
            dataFrame["WATTAGE MIN (W) PASS"] = tempdf["WATTAGE MIN (W)"].values[0]
            dataFrame["CLOSED PRESSURE MIN (kPa) PASS"] = tempdf["CLOSED PRESSURE MIN (kPa)"].values[0]

        dataList.append(dataFrame)

    dataFrame = pd.DataFrame(dataList)
    compiledFrame = pd.concat([compiledFrame, dataFrame], ignore_index=True)

    # --- COMPUTE model_summary AFTER compiledFrame exists --- (REVISED)
    today = pd.to_datetime(datetime.now().date())
    results = []

    for model, group in compiledFrame.groupby('MODEL CODE'):
        past_data = group[group['DATE'].dt.date < today.date()]
        if past_data.empty:
            print(f" Skipping {model}: No past data")
            continue

        past_data = past_data.sort_values('DATE', ascending=False)
        accumulated_rows = pd.DataFrame()
        count = 0

        for date in past_data['DATE'].dt.date.unique():
            daily_rows = past_data[past_data['DATE'].dt.date == date]
            valid_rows = daily_rows[daily_rows["PASS/NG"] == 1]
            accumulated_rows = pd.concat([accumulated_rows, valid_rows])
            count += len(valid_rows)
            if count >= 200:
                latest_valid_date = date
                break

        if count < 200:
            print(f" Skipping {model}: Not enough valid PASS/NG rows")
            continue

        pass_avg = accumulated_rows["V_MAX PASS"].mean()
        wattage_avg = accumulated_rows["WATTAGE MAX PASS"].mean()
        closedPressure_avg = accumulated_rows["CLOSED PRESSURE_MAX PASS"].mean()
        voltageMiddle_avg = accumulated_rows["VOLTAGE Middle PASS"].mean()
        wattageMiddle_avg = accumulated_rows["WATTAGE Middle (W) PASS"].mean()
        amperageMiddle_avg = accumulated_rows["AMPERAGE Middle (A) PASS"].mean()
        closePressureMiddle_avg = accumulated_rows["CLOSED PRESSURE Middle (kPa) PASS"].mean()
        voltageMin_avg = accumulated_rows["VOLTAGE MIN (V) PASS"].mean()
        wattageMin_avg = accumulated_rows["WATTAGE MIN (W) PASS"].mean()
        closePressureMin_avg = accumulated_rows["CLOSED PRESSURE MIN (kPa) PASS"].mean()

        results.append({
            'MODEL CODE': model,
            'LATEST DATE': latest_valid_date,
            'V-MAX PASS AVG': pass_avg,
            'WATTAGE MAX AVG': wattage_avg,
            'CLOSED PRESSURE_MAX AVG': closedPressure_avg,
            'VOLTAGE Middle AVG': voltageMiddle_avg,
            'WATTAGE Middle AVG': wattageMiddle_avg,
            'AMPERAGE Middle AVG': amperageMiddle_avg,
            'CLOSED PRESSURE Middle AVG': closePressureMiddle_avg,
            'VOLTAGE MIN (V) AVG': voltageMin_avg,
            'WATTAGE MIN AVG': wattageMin_avg,
            'CLOSED PRESSURE MIN AVG': closePressureMin_avg
        })

    model_summary = pd.DataFrame(results)
    pass_avg_map = model_summary.set_index("MODEL CODE")["V-MAX PASS AVG"].to_dict()
    wattage_avg_map = model_summary.set_index("MODEL CODE")["WATTAGE MAX AVG"].to_dict()
    closedPressure_avg_map = model_summary.set_index("MODEL CODE")['CLOSED PRESSURE_MAX AVG'].to_dict()
    voltageMiddle_avg_map = model_summary.set_index("MODEL CODE")["VOLTAGE Middle AVG"].to_dict()
    wattageMiddle_avg = model_summary.set_index("MODEL CODE")["WATTAGE Middle AVG"].to_dict()
    amperageMiddle_avg = model_summary.set_index("MODEL CODE")["AMPERAGE Middle AVG"].to_dict()
    closePressureMiddle_avg = model_summary.set_index("MODEL CODE")["CLOSED PRESSURE Middle AVG"].to_dict()
    voltageMin_avg = model_summary.set_index("MODEL CODE")["VOLTAGE MIN (V) AVG"].to_dict()
    wattageMin_avg = model_summary.set_index("MODEL CODE")["WATTAGE MIN AVG"].to_dict()
    closePressureMin_avg = model_summary.set_index("MODEL CODE")["CLOSED PRESSURE MIN AVG"].to_dict()

    # --- Inject AVERAGE DISPLAY ---
    compiledFrame["AVE V_MAX PASS"] = compiledFrame["MODEL CODE"].map(pass_avg_map)
    compiledFrame["AVE WATTAGE MAX (W)"] = compiledFrame["MODEL CODE"].map(wattage_avg_map)
    compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"] = compiledFrame["MODEL CODE"].map(closedPressure_avg_map)
    compiledFrame["AVE VOLTAGE Middle (V)"] = compiledFrame["MODEL CODE"].map(voltageMiddle_avg_map)
    compiledFrame["AVE WATTAGE Middle (W)"] = compiledFrame["MODEL CODE"].map(wattageMiddle_avg)
    compiledFrame["AVE AMPERAGE Middle (A)"] = compiledFrame["MODEL CODE"].map(amperageMiddle_avg)
    compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"] = compiledFrame["MODEL CODE"].map(closePressureMiddle_avg)
    compiledFrame["AVE VOLTAGE MIN (V)"] = compiledFrame["MODEL CODE"].map(voltageMin_avg)
    compiledFrame["AVE WATTAGE MIN (W)"] = compiledFrame["MODEL CODE"].map(wattageMin_avg)
    compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"] = compiledFrame["MODEL CODE"].map(closePressureMin_avg)

    # --- Compute DEV DISPLAY ---
    compiledFrame["DEV V_MAX PASS"] = (compiledFrame["AVE V_MAX PASS"] - compiledFrame["V_MAX PASS"]) / compiledFrame["AVE V_MAX PASS"]
    compiledFrame["DEV WATTAGE MAX (W)"] = (compiledFrame["AVE WATTAGE MAX (W)"] - compiledFrame["WATTAGE MAX PASS"]) / compiledFrame["AVE WATTAGE MAX (W)"]
    compiledFrame["DEV CLOSED PRESSURE_MAX (kPa)"] = (compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"] - compiledFrame["CLOSED PRESSURE_MAX PASS"]) / compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"].astype(float)
    compiledFrame["DEV VOLTAGE Middle (V)"] = (compiledFrame["AVE VOLTAGE Middle (V)"] - compiledFrame["VOLTAGE Middle PASS"]) / compiledFrame["AVE VOLTAGE Middle (V)"]
    compiledFrame["DEV WATTAGE Middle (W)"] = (compiledFrame["AVE WATTAGE Middle (W)"] - compiledFrame["WATTAGE Middle (W) PASS"]) / compiledFrame["AVE WATTAGE Middle (W)"]
    compiledFrame["DEV AMPERAGE Middle (A)"] = (compiledFrame["AVE AMPERAGE Middle (A)"] - compiledFrame["AMPERAGE Middle (A) PASS"]) / compiledFrame["AVE AMPERAGE Middle (A)"]
    compiledFrame["DEV CLOSED PRESSURE Middle (kPa)"] = (compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"] - compiledFrame["CLOSED PRESSURE Middle (kPa) PASS"]) / compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"]
    compiledFrame["DEV VOLTAGE MIN (V)"] = (compiledFrame["AVE VOLTAGE MIN (V)"] - compiledFrame["VOLTAGE MIN (V) PASS"]) / compiledFrame["AVE VOLTAGE MIN (V)"]
    compiledFrame["DEV WATTAGE MIN (W)"] = (compiledFrame["AVE WATTAGE MIN (W)"] - compiledFrame["WATTAGE MIN (W) PASS"]) / compiledFrame["AVE WATTAGE MIN (W)"]
    compiledFrame["DEV CLOSED PRESSURE MIN (kPa)"] = (compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"] - compiledFrame["CLOSED PRESSURE MIN (kPa) PASS"]) / compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"]

    # --- Display results ---
    # print(" Final cleaned compiledFrame with averages:\n")
    # print(compiledFrame)
    # print("\n Summary model_summary:\n")
    # print(model_summary)






def DeviationChecker():
    
    print(f"DEV V_MAX PASS VALUES: {compiledFrame["DEV V_MAX PASS"].tail(1).values[0]}")
    if compiledFrame["DEV V_MAX PASS"].tail(1).values[0] > 0.03 \
    or compiledFrame["DEV V_MAX PASS"].tail(1).values[0] < -0.03:
        print("DEV V_MAX PASS DEVIATION DETECTED")
        varMan.isDeviationDetected = True

        varMan.deviation_time_text.configure(state ='normal')
        # Inserting Text which is read only
        varMan.deviation_time_text.insert(tk.INSERT, f"sleigfhuifhduf\n")
        varMan.deviation_time_text.configure(state ='disabled')

    else:
        print("DEV V_MAX PASS DEVIATION GOOD")

    print(f"DEV WATTAGE MAX (W) VALUES: {compiledFrame["DEV WATTAGE MAX (W)"].tail(1).values[0]}")
    if compiledFrame["DEV WATTAGE MAX (W)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV WATTAGE MAX (W)"].tail(1).values[0] < -0.03:
        print("DEV WATTAGE MAX (W) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV WATTAGE MAX (W) DEVIATION GOOD")

    print(f"DEV CLOSED PRESSURE_MAX (kPa) VALUES: {compiledFrame["DEV CLOSED PRESSURE_MAX (kPa)"].tail(1).values[0]}")
    if compiledFrame["DEV CLOSED PRESSURE_MAX (kPa)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV CLOSED PRESSURE_MAX (kPa)"].tail(1).values[0] < -0.03:
        print("DEV CLOSED PRESSURE_MAX (kPa) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV CLOSED PRESSURE_MAX (kPa) DEVIATION GOOD")

    print(f"DEV VOLTAGE Middle (V) VALUES: {compiledFrame["DEV VOLTAGE Middle (V)"].tail(1).values[0]}")
    if compiledFrame["DEV VOLTAGE Middle (V)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV VOLTAGE Middle (V)"].tail(1).values[0] < -0.03:
        print("DEV VOLTAGE Middle (V) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV VOLTAGE Middle (V) DEVIATION GOOD")

    print(f"DEV WATTAGE Middle (W) VALUES: {compiledFrame["DEV WATTAGE Middle (W)"].tail(1).values[0]}")
    if compiledFrame["DEV WATTAGE Middle (W)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV WATTAGE Middle (W)"].tail(1).values[0] < -0.03:
        print("DEV WATTAGE Middle (W) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV WATTAGE Middle (W) DEVIATION GOOD")

    print(f"DEV AMPERAGE Middle (A) VALUES: {compiledFrame["DEV AMPERAGE Middle (A)"].tail(1).values[0]}")
    if compiledFrame["DEV AMPERAGE Middle (A)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV AMPERAGE Middle (A)"].tail(1).values[0] < -0.03:
        print("DEV AMPERAGE Middle (A) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV AMPERAGE Middle (A) DEVIATION GOOD")

    print(f"DEV CLOSED PRESSURE Middle (kPa) VALUES: {compiledFrame["DEV CLOSED PRESSURE Middle (kPa)"].tail(1).values[0]}")
    if compiledFrame["DEV CLOSED PRESSURE Middle (kPa)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV CLOSED PRESSURE Middle (kPa)"].tail(1).values[0] < -0.03:
        print("DEV CLOSED PRESSURE Middle (kPa) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV CLOSED PRESSURE Middle (kPa) DEVIATION GOOD")

    print(f"DEV VOLTAGE MIN (V) VALUES: {compiledFrame["DEV VOLTAGE MIN (V)"].tail(1).values[0]}")
    if compiledFrame["DEV VOLTAGE MIN (V)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV VOLTAGE MIN (V)"].tail(1).values[0] < -0.03:
        print("DEV VOLTAGE MIN (V) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV VOLTAGE MIN (V) DEVIATION GOOD")

    print(f"DEV WATTAGE MIN (W) VALUES: {compiledFrame["DEV WATTAGE MIN (W)"].tail(1).values[0]}")
    if compiledFrame["DEV WATTAGE MIN (W)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV WATTAGE MIN (W)"].tail(1).values[0] < -0.03:
        print("DEV WATTAGE MIN (W) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV WATTAGE MIN (W) DEVIATION GOOD")

    print(f"DEV CLOSED PRESSURE MIN (kPa) VALUES: {compiledFrame["DEV CLOSED PRESSURE MIN (kPa)"].tail(1).values[0]}")
    if compiledFrame["DEV CLOSED PRESSURE MIN (kPa)"].tail(1).values[0] > 0.03 \
        or compiledFrame["DEV CLOSED PRESSURE MIN (kPa)"].tail(1).values[0] < -0.03:
        print("DEV CLOSED PRESSURE MIN (kPa) DEVIATION DETECTED")
        varMan.isDeviationDetected = True
    else:
        print("DEV CLOSED PRESSURE MIN (kPa) DEVIATION GOOD")

    #--------------------------------------------------------
# def DeviationChecker():
#     global isDeviationDetected
#     isDeviationDetected = False  # Start with default as False

#     # Print current date and time
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print(f"🔍 Inspection Timestamp: {current_time}\n")

#     inspection_columns = [
#         "DEV V_MAX PASS",
#         "DEV WATTAGE MAX (W)",
#         "DEV CLOSED PRESSURE_MAX (kPa)",
#         "DEV VOLTAGE Middle (V)",
#         "DEV WATTAGE Middle (W)",
#         "DEV AMPERAGE Middle (A)",
#         "DEV CLOSED PRESSURE Middle (kPa)",
#         "DEV VOLTAGE MIN (V)",
#         "DEV WATTAGE MIN (W)",
#         "DEV CLOSED PRESSURE MIN (kPa)"
#     ]

#     threshold = 0.03  # Deviation threshold

#     for column in inspection_columns:
#         deviation_value = compiledFrame[column].values[0]
#         print(f"{column} Deviation Value: {deviation_value}")

#         if deviation_value > threshold or deviation_value < -threshold:
#             print(f"{column} DEVIATION DETECTED")
#             varMan.isDeviationDetected = True
#         else:
#             print(f"{column} DEVIATION GOOD")
        
#     print(f"\n📌 Overall Deviation Detected: {isDeviationDetected}")





    if varMan.isDeviationDetected:
        print("⚠️ DEVIATION DETECTED")
        
        varMan.deviation_err_msg_text =  "⚠️ DEVIATION DETECTED"
        varMan.deviation_err_msg.config(text=varMan.deviation_err_msg_text)
        varMan.deviation_stop_btn.config(bg="red")
    else:
        print("✅ NO DEVIATION DETECTED")


def startProgram():
    ReadFiles()
    EmptyColumnCreator()
    PopulateContent()
    DeviationChecker()

def run():
    #Reading Original File
    # compiledPiFileOrig = os.path.getmtime(r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv")
    compiledPiFileOrig = os.path.getmtime(r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv") # DESKTOP FALSE TESTING

    while True:
        if not varMan.isDeviationDetected:
            #Reading Original File
            # compiledPiFileCurrent = os.path.getmtime(r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv")
            compiledPiFileCurrent = os.path.getmtime(r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv") # DESKTOP FALSE TESTING

            if compiledPiFileCurrent != compiledPiFileOrig:
                print("CHANGES DETECTED")

                #Run Program
                # print("🚀 Running model analysis...")
                startProgram()
                # print("✅ Finished!")

                compiledPiFileOrig = compiledPiFileCurrent

            if varMan.deviation_err_msg_text == "Loading...":
                varMan.deviation_err_msg_text = "Loading"
                varMan.deviation_err_msg.config(text=varMan.deviation_err_msg_text)

            else:
                varMan.deviation_err_msg_text += "."
                varMan.deviation_err_msg.config(text=varMan.deviation_err_msg_text)

            print("WAITING FOR CHANGES IN CSV FILE")
            time.sleep(1)


# %%
