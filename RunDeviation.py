#%%
# run_model_analysis.py
import os
import time
import Deviation1CManager  # Make sure this file is named exactly "model_analysis.py" and in the same folder

def run():
    #Reading Original File
    # compiledPiFileOrig = os.path.getmtime(r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv") #ORIGINAL PATH
    compiledPiFileOrig = os.path.getmtime(r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv") # DESKTOP FALSE TESTING
    while True:
        #Reading Original File
        # compiledPiFileCurrent = os.path.getmtime(r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv") # ORIGINAL PATH
        compiledPiFileCurrent = os.path.getmtime(r"C:\Users\ai.pc\OneDrive\Desktop\CompiledPIMachine.csv") # DESKTOP FALSE TESTING

        if compiledPiFileCurrent != compiledPiFileOrig:
            print("CHANGES DETECTED")

            #Run Program
            print("🚀 Running model analysis...")
            Deviation1CManager.startProgram()
            print("✅ Finished!")

            compiledPiFileOrig = compiledPiFileCurrent

        print("WAITING FOR CHANGES IN CSV FILE")
        time.sleep(1)

run() # THIS WILL RUN AND WAIT FOR FILE CHANGES
# Deviation1CManager.startProgram() # IT WILL RUN AND DO NOT WAIT FOR FILE CHANGES


# %%
