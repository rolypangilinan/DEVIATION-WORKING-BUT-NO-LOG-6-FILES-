# %%
from imports import *
import JobOrderManager as JOManager
import serial
# import Deviation1CManager
import ExecutableManager
import VariableManager as varMan

# %%
Engine = ""
prog_run = True
is_debug = False

# Process 1
process_1_csv = ""

proc_1_Mtrl_1_code = ""
proc_1_Mtrl_2_code = ""
proc_1_Mtrl_3_code = ""
proc_1_Mtrl_4_code = ""
proc_1_Mtrl_5_code = ""


proc_1_txt = ""
proc_1_stop_btn = ""
proc_1_err_msg = ""
proc_1_err_msg_txt = "Loading"
proc_1_is_wrong_itm = False
is_read_proc1_csv = False
# Add time tolerance error flag
proc_1_time_out_of_tolerance = False


# Process 2
proc_2_csv = ""

proc_2_Mtrl_1_code = ""
proc_2_Mtrl_2_code = ""
proc_2_Mtrl_3_code = ""
proc_2_Mtrl_4_code = ""
proc_2_Mtrl_5_code = ""


proc_2_txt = ""
proc_2_stop_btn = ""
proc_2_err_msg = ""
proc_2_err_msg_txt = "Loading"
proc_2_is_wrong_itm = False
is_read_proc2_csv = False
# Add time tolerance error flag
proc_2_time_out_of_tolerance = False


# Process 3
proc_3_csv = ""

proc_3_Mtrl_1_code = ""
proc_3_Mtrl_2_code = ""
proc_3_Mtrl_3_code = ""
proc_3_Mtrl_4_code = ""
proc_3_Mtrl_5_code = ""


proc_3_txt = ""
proc_3_stop_btn = ""
proc_3_err_msg = ""
proc_3_err_msg_txt = "Loading"
proc_3_is_wrong_itm = False
is_read_proc3_csv = False
# Add time tolerance error flag
proc_3_time_out_of_tolerance = False


# Process 4
proc_4_csv = ""

proc_4_Mtrl_1_code = ""
proc_4_Mtrl_2_code = ""
proc_4_Mtrl_3_code = ""
proc_4_Mtrl_4_code = ""
proc_4_Mtrl_5_code = ""


proc_4_txt = ""
proc_4_stop_btn = ""
proc_4_err_msg = ""
proc_4_err_msg_txt = "Loading"
proc_4_is_wrong_itm = False
is_read_proc4_csv = False
# Add time tolerance error flag
proc_4_time_out_of_tolerance = False


# Process 5
proc_5_csv = ""

proc_5_Mtrl_1_code = ""
proc_5_Mtrl_2_code = ""
proc_5_Mtrl_3_code = ""
proc_5_Mtrl_4_code = ""
proc_5_Mtrl_5_code = ""


proc_5_txt = ""
proc_5_stop_btn = ""
proc_5_err_msg = ""
proc_5_err_msg_txt = "Loading"
proc_5_is_wrong_itm = False
is_read_proc5_csv = False
# Add time tolerance error flag
proc_5_time_out_of_tolerance = False


# Process 6
proc_6_csv = ""

proc_6_Mtrl_1_code = ""
proc_6_Mtrl_2_code = ""
proc_6_Mtrl_3_code = ""
proc_6_Mtrl_4_code = ""
proc_6_Mtrl_5_code = ""


proc_6_txt = ""
proc_6_stop_btn = ""
proc_6_err_msg = ""
proc_6_err_msg_txt = "Loading"
proc_6_is_wrong_itm = False
is_read_proc6_csv = False
# Add time tolerance error flag
proc_6_time_out_of_tolerance = False

is_speaking = False

is_proc_1_by_pass = False
is_proc_2_by_pass = False
is_proc_3_by_pass = False
is_proc_4_by_pass = False
is_proc_5_by_pass = False
is_proc_6_by_pass = False

sound_title = ""

log_count = 0

ser = serial.Serial("COM3", 9600)


# %%
# Utility function to check if actual time is within ±10% of ST (not for Process 6)
def check_time_tolerance(actual_time, st_time):
    """
    Returns (is_within, min_time, max_time):
    - is_within: True if actual_time is within [min_time, max_time], else False
    - min_time: Process ST - 40% of ST
    - max_time: Process ST + 40% of ST
    """
    min_time = st_time - (st_time * 0.40)
    max_time = st_time + (st_time * 0.40)
    is_within = min_time <= actual_time <= max_time
    return is_within, min_time, max_time


# %%
def play_mp3(sound_title):
    os.chdir(r"\\192.168.2.19\ai_team\AI Program\Programs\Individual Program")

    path = rf"Sounds\{sound_title}.mp3"

    pygame.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def stop_mp3():
    pygame.mixer.music.stop()


# %%
def speak_voice(sentence):
    global Engine

    Engine = pyttsx3.init()
    Engine.setProperty("rate", 100)
    Engine.say(sentence)
    Engine.runAndWait()


# %%
def setting_proc_1_dir():
    global is_debug

    if is_debug:
        return rf"\\192.168.2.10\csv\csv\VT1\Debug"
    else:
        return rf"\\192.168.2.10\csv\csv\VT1"


# %%
def setting_proc_2_dir():
    global is_debug

    if is_debug:
        return rf"\\192.168.2.10\csv\csv\VT2\Debug"
    else:
        return rf"\\192.168.2.10\csv\csv\VT2"


# %%
def setting_proc_3_dir():
    global is_debug

    if is_debug:
        return rf"\\192.168.2.10\csv\csv\VT3\Debug"
    else:
        return rf"\\192.168.2.10\csv\csv\VT3"


# %%
def setting_proc_4_dir():
    global is_debug

    if is_debug:
        return rf"\\192.168.2.10\csv\csv\VT4\Debug"
    else:
        return rf"\\192.168.2.10\csv\csv\VT4"


# %%
def setting_proc_5_dir():
    global is_debug

    if is_debug:
        return rf"\\192.168.2.10\csv\csv\VT5\Debug"
    else:
        return rf"\\192.168.2.10\csv\csv\VT5"


# %%
def setting_proc_6_dir():
    global is_debug

    if is_debug:
        return rf"\\192.168.2.10\csv\csv\VT6\Debug"
    else:
        return rf"\\192.168.2.10\csv\csv\VT6"


# %%
def proc_1_start_voice(sound_title):
    global proc_1_is_wrong_itm
    global proc_2_is_wrong_itm
    global proc_3_is_wrong_itm
    global proc_4_is_wrong_itm
    global proc_5_is_wrong_itm
    global proc_6_is_wrong_itm

    global log_count
    global is_speaking

    global is_proc_1_by_pass

    while proc_1_is_wrong_itm:
        if not is_speaking or is_proc_1_by_pass:
            is_speaking = True
            is_proc_1_by_pass = True

            play_mp3(sound_title)
            print(sound_title)

        log_count += 1

        if log_count >= 10:
            os.system("cls")
            log_count = 0
        time.sleep(2)

    is_speaking = False
    is_proc_1_by_pass = False


# %%
def proc_2_start_voice(sound_title):
    global proc_1_is_wrong_itm
    global proc_2_is_wrong_itm
    global proc_3_is_wrong_itm
    global proc_4_is_wrong_itm
    global proc_5_is_wrong_itm
    global proc_6_is_wrong_itm

    global log_count
    global is_speaking

    global is_proc_2_by_pass

    while proc_2_is_wrong_itm:
        if not is_speaking or is_proc_2_by_pass:
            is_speaking = True
            is_proc_2_by_pass = True

            play_mp3(sound_title)
            print(sound_title)

        log_count += 1

        if log_count >= 10:
            os.system("cls")
            log_count = 0
        time.sleep(2)

    is_speaking = False
    is_proc_2_by_pass = False


# %%
def proc_3_start_voice(sound_title):
    global proc_1_is_wrong_itm
    global proc_2_is_wrong_itm
    global proc_3_is_wrong_itm
    global proc_4_is_wrong_itm
    global proc_5_is_wrong_itm
    global proc_6_is_wrong_itm

    global log_count
    global is_speaking

    global is_proc_3_by_pass

    while proc_3_is_wrong_itm:
        if not is_speaking or is_proc_3_by_pass:
            is_speaking = True
            is_proc_3_by_pass = True

            play_mp3(sound_title)
            print(sound_title)

        log_count += 1

        if log_count >= 10:
            os.system("cls")
            log_count = 0
        time.sleep(2)

    is_speaking = False
    is_proc_3_by_pass = False


# %%
def proc_4_start_voice(sound_title):
    global proc_1_is_wrong_itm
    global proc_2_is_wrong_itm
    global proc_3_is_wrong_itm
    global proc_4_is_wrong_itm
    global proc_5_is_wrong_itm
    global proc_6_is_wrong_itm

    global log_count
    global is_speaking

    global is_proc_4_by_pass

    while proc_4_is_wrong_itm:
        if not is_speaking or is_proc_4_by_pass:
            is_speaking = True
            is_proc_4_by_pass = True

            play_mp3(sound_title)
            print(sound_title)

        log_count += 1

        if log_count >= 10:
            os.system("cls")
            log_count = 0
        time.sleep(2)

    is_speaking = False
    is_proc_4_by_pass = False


# %%
def proc_5_start_voice(sound_title):
    global proc_1_is_wrong_itm
    global proc_2_is_wrong_itm
    global proc_3_is_wrong_itm
    global proc_4_is_wrong_itm
    global proc_5_is_wrong_itm
    global proc_6_is_wrong_itm

    global log_count
    global is_speaking

    global is_proc_5_by_pass

    while proc_5_is_wrong_itm:
        if not is_speaking or is_proc_5_by_pass:
            is_speaking = True
            is_proc_5_by_pass = True

            play_mp3(sound_title)
            print(sound_title)

        log_count += 1

        if log_count >= 10:
            os.system("cls")
            log_count = 0
        time.sleep(2)

    is_speaking = False
    is_proc_5_by_pass = False


# %%
def proc_6_start_voice(sound_title):
    global proc_1_is_wrong_itm
    global proc_2_is_wrong_itm
    global proc_3_is_wrong_itm
    global proc_4_is_wrong_itm
    global proc_5_is_wrong_itm
    global proc_6_is_wrong_itm

    global log_count
    global is_speaking

    global is_proc_6_by_pass

    while proc_6_is_wrong_itm:
        if not is_speaking or is_proc_6_by_pass:
            is_speaking = True
            is_proc_6_by_pass = True

            play_mp3(sound_title)
            print(sound_title)

        log_count += 1

        if log_count >= 10:
            os.system("cls")
            log_count = 0
        time.sleep(2)

    is_speaking = False
    is_proc_6_by_pass = False


# %%
def read_proc_1_csv():
    global process_1_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    process_1_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT1\log000_1.csv", encoding="latin1"
    )

    process_1_csv = process_1_csv[
        process_1_csv["Process 1 Regular/Contractual"].str.contains("REG", na=False)
    ]


# %%
def read_proc_2_csv():
    global proc_2_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    proc_2_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT2\log000_2.csv", encoding="latin1"
    )

    proc_2_csv = proc_2_csv[
        proc_2_csv["Process 2 Regular/Contractual"].str.contains("REG", na=False)
    ]


# %%
def read_proc_3_csv():
    global proc_3_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    proc_3_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT3\log000_3.csv", encoding="latin1"
    )

    proc_3_csv = proc_3_csv[
        proc_3_csv["Process 3 Regular/Contractual"].str.contains("REG", na=False)
    ]


# %%
def read_proc_4_csv():
    global proc_4_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    proc_4_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT4\log000_4.csv", encoding="latin1"
    )

    proc_4_csv = proc_4_csv[
        proc_4_csv["Process 4 Regular/Contractual"].str.contains("REG", na=False)
    ]


# %%
def read_proc_5_csv():
    global proc_5_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    proc_5_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT5\log000_5.csv", encoding="latin1"
    )

    proc_5_csv = proc_5_csv[
        proc_5_csv["Process 5 Regular/Contractual"].str.contains("REG", na=False)
    ]


# %%
def read_proc_6_csv():
    global proc_6_csv

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    proc_6_csv = pd.read_csv(
        rf"\\192.168.2.10\csv\csv\VT6\log000_6.csv", encoding="latin1"
    )

    proc_6_csv = proc_6_csv[
        proc_6_csv["Process 6 Regular/Contractual"].str.contains("REG", na=False)
    ]


# %%
def check_proc_1_err_itm():
    global prog_run

    global ser

    # process 1
    global process_1_csv

    global proc_1_Mtrl_1_code
    global proc_1_Mtrl_2_code
    global proc_1_Mtrl_3_code
    global proc_1_Mtrl_4_code
    global proc_1_Mtrl_5_code

    global proc_1_txt
    global proc_1_stop_btn
    global proc_1_err_msg
    global proc_1_err_msg_txt
    global proc_1_is_wrong_itm
    global is_read_proc1_csv

    global log_count

    global sound_title

    is_mtr_read = ""

    org_file = os.path.getmtime(setting_proc_1_dir() + r"\log000_1.csv")

    while prog_run:
        curr_file = os.path.getmtime(setting_proc_1_dir() + r"\log000_1.csv")

        # Reset error detection flag for each iteration
        proc_1_err_mtr_detect = False

        if proc_1_err_msg_txt == "Loading...":
            proc_1_err_msg_txt = "Loading"
            proc_1_err_msg.config(text=proc_1_err_msg_txt)

        else:
            proc_1_err_msg_txt += "."
            proc_1_err_msg.config(text=proc_1_err_msg_txt)

        if curr_file != org_file:
            proc_1_err_mtr_detect = False
            is_read_proc1_csv = False

            print("Changes Detected")

            while not is_read_proc1_csv:
                try:
                    read_proc_1_csv()
                    is_read_proc1_csv = True
                except Exception as e:
                    print(f"Error reading CSV: {e}")

            temp_df_vt_1 = process_1_csv.tail(1)

            while True:
                try:
                    if temp_df_vt_1["Process 1 Repaired Action"].values[0] == "-":
                        print("Reading all data")
                        JOManager.check_job_orders()
                        JOManager.find_materials()
                        is_mtr_read = True
                        break
                    else:
                        print("Reading all data today")
                        JOManager.check_job_orders()
                        JOManager.find_materials()
                        is_mtr_read = True
                        break
                except Exception as e:
                    print(f"Error reading job orders: {e}")
                    is_mtr_read = False
                    break

            # print(f"{temp_df_vt_1["Process 1 Em2p"].values[0]}_______________________________")

            if is_mtr_read:
                # 60CAT0213P,60CAT0212P, 60CAT0202P, 60CAT0203P, 60CAT0902P, 60CAT0903P, 60CAT0905P, 60CAT0000P
                if (
                    temp_df_vt_1["Process 1 Model Code"].values == "60CAT0212P"
                    or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0203P"
                    or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0213P"
                    or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0203P"
                    or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0902P"
                    or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0903P"
                    or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0905P"
                    or temp_df_vt_1["Process 1 Model Code"].values == "60CAT0000P"
                ):
                    # print(f"Model {str(temp_df_vt_1["Process 1 Model Code"].values)}")
                    for a in JOManager.job_order_materials:
                        same_value = 0
                        if temp_df_vt_1["Process 1 Em2p"].values[0] == a:
                            same_value += 1
                            print(same_value)
                            break
                    if same_value == 0:
                        proc_1_err_mtr_detect = True
                        proc_1_is_wrong_itm = True
                        proc_1_err_msg_txt = "Wrong E M Used For 2 P In Process 1"
                        proc_1_err_msg.config(text=proc_1_err_msg_txt)
                        proc_1_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process1WrongEm2P"
                        proc_1_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_value = 0
                        if temp_df_vt_1["Process 1 Em3p"].values[0] == a:
                            same_value += 1
                            print(same_value)
                            break
                    if same_value == 0:
                        proc_1_err_mtr_detect = True
                        proc_1_is_wrong_itm = True
                        proc_1_err_msg_txt = "Wrong E M Used For 3 P In Process 1"
                        proc_1_err_msg.config(text=proc_1_err_msg_txt)
                        proc_1_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process1WrongEm3P"
                        proc_1_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_value = 0
                        if temp_df_vt_1["Process 1 Harness"].values[0] == a:
                            same_value += 1
                            print(same_value)
                            break
                    if same_value == 0:
                        proc_1_err_mtr_detect = True
                        proc_1_is_wrong_itm = True
                        proc_1_err_msg_txt = "Wrong Harness Used In Process 1"
                        proc_1_err_msg.config(text=proc_1_err_msg_txt)
                        proc_1_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process1WrongHarness"
                        proc_1_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_value = 0
                        if temp_df_vt_1["Process 1 Frame"].values[0] == a:
                            same_value += 1
                            print(same_value)
                            break
                    if same_value == 0:
                        proc_1_err_mtr_detect = True
                        proc_1_is_wrong_itm = True
                        proc_1_err_msg_txt = "Wrong Frame Used In Process 1"
                        proc_1_err_msg.config(text=proc_1_err_msg_txt)
                        proc_1_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process1WrongFrame"
                        proc_1_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_value = 0
                        if temp_df_vt_1["Process 1 Bushing"].values[0] == a:
                            same_value += 1
                            print(same_value)
                            break
                    if same_value == 0:
                        proc_1_err_mtr_detect = True
                        proc_1_is_wrong_itm = True
                        proc_1_err_msg_txt = "Wrong Bushing Used In Process 1"
                        proc_1_err_msg.config(text=proc_1_err_msg_txt)
                        proc_1_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process1WrongBushing"
                        proc_1_start_voice(sound_title)

                # Check if no errors were detected (material is correct)
                if not proc_1_err_mtr_detect:
                    # --- TIME TOLERANCE CHECK ---
                    try:
                        actual_time = float(
                            temp_df_vt_1["Process 1 Actual Time"].values[0]
                        )
                        st_time = float(temp_df_vt_1["Process 1 ST"].values[0])
                        print(
                            f"[DEBUG] Process 1: actual_time={actual_time}, st_time={st_time}"
                        )
                        is_within, min_time, max_time = check_time_tolerance(
                            actual_time, st_time
                        )
                        print(
                            f"[DEBUG] Process 1: is_within={is_within}, min_time={min_time}, max_time={max_time}"
                        )
                        if is_within:
                            proc_1_txt.config(text="Process 1", fg="black")
                            proc_1_err_msg.config(
                                text=f"Process 1 Time Within Tolerance (min: {min_time:.2f}, max: {max_time:.2f})",
                                fg="darkgreen",
                            )
                            proc_1_stop_btn.config(bg="orange")
                            proc_1_time_out_of_tolerance = False
                            proc_1_time_text.config(state="normal")
                            proc_1_time_text.delete("1.0", tk.END)
                            proc_1_time_text.insert(
                                tk.END,
                                f"[Within Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                            )
                            proc_1_time_text.config(state="disabled")
                            threading.Thread(
                                target=mtr_correct, args=(proc_1_txt, "Process 1")
                            ).start()
                        else:
                            proc_1_txt.config(text="Process 1", fg="black")
                            proc_1_err_msg.config(text="Loading...", fg="black")
                            proc_1_stop_btn.config(bg="red")
                            proc_1_time_out_of_tolerance = True
                            proc_1_time_text.config(state="normal")
                            proc_1_time_text.delete("1.0", tk.END)
                            proc_1_time_text.insert(
                                tk.END,
                                f"[Time Out of Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                            )
                            proc_1_time_text.config(state="disabled")
                            ser.write(b"H")

                    except Exception as e:
                        print(f"[ERROR] Time tolerance check failed for Process 1: {e}")
                        proc_1_txt.config(text="Process 1", fg="black")
                        proc_1_err_msg.config(text="Process 1", fg="black")
                        proc_1_stop_btn.config(bg="orange")
                        proc_1_time_out_of_tolerance = False
                        threading.Thread(
                            target=mtr_correct, args=(proc_1_txt, "Process 1")
                        ).start()
                else:
                    # No material was read
                    if (
                        temp_df_vt_1["Process 1 Em2p"].values[0] == ""
                        and temp_df_vt_1["Process 1 Em3p"].values[0] == ""
                        and temp_df_vt_1["Process 1 Harness"].values[0] == ""
                        and temp_df_vt_1["Process 1 Frame"].values[0] == ""
                        and temp_df_vt_1["Process 1 Bushing"].values[0] == ""
                    ):
                        threading.Thread(
                            target=no_mtr_read, args=(proc_1_txt, "Process 1")
                        ).start()

            org_file = curr_file

        print("Reading files")
        time.sleep(1)

    if proc_1_time_out_of_tolerance:
        proc_1_txt.config(text="Process 1", fg="black")
        proc_1_err_msg.config(text="Loading...", fg="black")
        proc_1_stop_btn.config(bg="orange")
        proc_1_time_out_of_tolerance = False
        proc_1_time_text.config(state="normal")
        proc_1_time_text.delete("1.0", tk.END)
        proc_1_time_text.config(state="disabled")


# %%
def check_proc_2_err_itm():
    global ser
    global prog_run

    global proc_2_csv

    global proc_2_Mtrl_1_code
    global proc_2_Mtrl_2_code
    global proc_2_Mtrl_3_code
    global proc_2_Mtrl_4_code
    global proc_2_Mtrl_5_code
    global proc_2_Mtrl_6_code

    global proc_2_txt
    global proc_2_stop_btn
    global proc_2_err_msg
    global proc_2_err_msg_txt
    global proc_2_is_wrong_itm
    global is_read_proc2_csv

    global log_count

    global sound_title

    global ser

    is_mtr_read = ""

    org_file = os.path.getmtime(setting_proc_2_dir() + r"\log000_2.csv")
    while prog_run:
        try:
            curr_file = os.path.getmtime(setting_proc_2_dir() + r"\log000_2.csv")
        except:
            print

        if proc_2_err_msg_txt == "Loading...":
            proc_2_err_msg_txt = "Loading"
            proc_2_err_msg.config(text=proc_2_err_msg_txt)
        else:
            proc_2_err_msg_txt += "."
            proc_2_err_msg.config(text=proc_2_err_msg_txt)

        if curr_file != org_file:
            proc_2_err_mtr_detect = False
            is_read_proc2_csv = False

            print("Changes Detected")

            while not is_read_proc2_csv:
                try:
                    read_proc_2_csv()
                    is_read_proc2_csv = True
                except:
                    print

            temp_df_vt_2 = proc_2_csv.tail(1)

            # Forced Reading Of JobOrder
            while True:
                # try:
                if temp_df_vt_2["Process 2 Repaired Action"].values[0] != "-":
                    print("Reading All Data")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    is_mtr_read = True
                    break
                else:
                    print("Reading Data Today")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    is_mtr_read = True
                    break
                # except:
                #     is_mtr_read = False
                #     break
            
            if is_mtr_read:
                # 60CAT0212P, 60CAT0203P, 60CAT0213P, 60CAT0203P,
                if (
                    temp_df_vt_2["Process 2 Model Code"].values == "60CAT0212P"
                    or temp_df_vt_2["Process 2 Model Code"].values == "60CAT0202P"
                    or temp_df_vt_2["Process 2 Model Code"].values == "60CAT0213P"
                    or temp_df_vt_2["Process 2 Model Code"].values == "60CAT0203P"
                ):

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 M4x40 Screw"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong M4X40 Screw Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongM4X40Screw"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Rod Blk"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Rod BLock Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongRodBlock"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Df Blk"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Diaphragm Block Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongDiaphragmBlock"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Df Ring"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Diaphragm Ring Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongDfRing"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Washer"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Washer Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongWasher"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Lock Nut"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Lock Nut In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongLockNut"
                        proc_2_start_voice(sound_title)

                # 60FC00902P, 60FC00903P, 60FC00905P, 60FC00000P
                if (
                    temp_df_vt_2["Process 2 Model Code"].values == "60FC00902P"
                    or temp_df_vt_2["Process 2 Model Code"].values == "60FC00903P"
                    or temp_df_vt_2["Process 2 Model Code"].values == "60FC00905P"
                    or temp_df_vt_2["Process 2 Model Code"].values == "60FC00000P"
                ):
                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 M4x40 Screw"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong M4X40 Screw Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongM4X40Screw"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Rod Blk"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Rod Block Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongRodBlock"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Df Blk"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Diaphragm Block Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongDiaphragmBlock"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Df Ring"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Diaphragm Ring Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongDfRing"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Washer"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Washer Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongWasher"
                        proc_2_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_2["Process 2 Lock Nut"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_2_err_mtr_detect = True
                        proc_2_is_wrong_itm = True
                        proc_2_err_msg_txt = "Wrong Lock Nut Used In Process 2"
                        proc_2_err_msg.config(text=proc_2_err_msg_txt)
                        proc_2_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process2WrongLockNut"
                        proc_2_start_voice(sound_title)

            if not proc_2_err_mtr_detect:
                # --- TIME TOLERANCE CHECK ---
                try:
                    actual_time = float(temp_df_vt_2["Process 2 Actual Time"].values[0])
                    st_time = float(temp_df_vt_2["Process 2 ST"].values[0])
                    print(
                        f"[DEBUG] Process 2: actual_time={actual_time}, st_time={st_time}"
                    )
                    is_within, min_time, max_time = check_time_tolerance(
                        actual_time, st_time
                    )
                    print(
                        f"[DEBUG] Process 2: is_within={is_within}, min_time={min_time}, max_time={max_time}"
                    )
                    if is_within:
                        proc_2_txt.config(text="Process 2", fg="black")
                        proc_2_err_msg.config(
                            text=f"Process 2 Time Within Tolerance (min: {min_time:.2f}, max: {max_time:.2f})",
                            fg="darkgreen",
                        )
                        proc_2_stop_btn.config(bg="orange")
                        proc_2_time_out_of_tolerance = False
                        proc_2_time_text.config(state="normal")
                        proc_2_time_text.delete("1.0", tk.END)
                        proc_2_time_text.insert(
                            tk.END,
                            f"[Within Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                        )
                        proc_2_time_text.config(state="disabled")
                        threading.Thread(
                            target=mtr_correct, args=(proc_2_txt, "Process 2")
                        ).start()
                    else:
                        proc_2_txt.config(text="Process 2", fg="black")
                        proc_2_err_msg.config(text="Loading...", fg="black")
                        proc_2_stop_btn.config(bg="red")
                        proc_2_time_out_of_tolerance = True
                        proc_2_time_text.config(state="normal")
                        proc_2_time_text.delete("1.0", tk.END)
                        proc_2_time_text.insert(
                            tk.END,
                            f"[Time Out of Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                        )
                        proc_2_time_text.config(state="disabled")
                        ser.write(b"H")
                except Exception as e:
                    print(f"[ERROR] Time tolerance check failed for Process 2: {e}")
                    proc_2_txt.config(text="Process 2", fg="black")
                    proc_2_err_msg.config(text="Process 2", fg="black")
                    proc_2_stop_btn.config(bg="orange")
                    proc_2_time_out_of_tolerance = False
                    threading.Thread(
                        target=mtr_correct, args=(proc_2_txt, "Process 2")
                    ).start()
            else:
                if (
                    temp_df_vt_2["Process 2 M4x40 Screw"].values[0] == ""
                    and temp_df_vt_2["Process 2 Rod Blk"].values[0] == ""
                    and temp_df_vt_2["Process 2 Df Blk"].values[0] == ""
                    and temp_df_vt_2["Process 2 Df Ring"].values[0] == ""
                    and temp_df_vt_2["Process 2 Washer"].values[0] == ""
                    and temp_df_vt_2["Process 2 Lock Nut"].values[0] == ""
                ):
                    threading.Thread(
                        target=no_mtr_read, args=(proc_2_txt, "Process 2")
                    ).start()
            org_file = curr_file
        print("Reading Files")

        # #Clearing Cmd Logs When Reaches 10 Lines
        # logCount += 1
        # if logCount >= 10:
        #     os.system('cls')
        #     logCount = 0
        time.sleep(1)

    if proc_2_time_out_of_tolerance:
        proc_2_txt.config(text="Process 2", fg="black")
        proc_2_err_msg.config(text="Loading...", fg="black")
        proc_2_stop_btn.config(bg="orange")
        proc_2_time_out_of_tolerance = False
        proc_2_time_text.config(state="normal")
        proc_2_time_text.delete("1.0", tk.END)
        proc_2_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 2: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


# %%
def check_proc_3_err_itm():
    global prog_run

    global proc_3_csv

    global proc_3_Mtrl_1_code
    global proc_3_Mtrl_2_code
    global proc_3_Mtrl_3_code
    global proc_3_Mtrl_4_code
    global proc_3_Mtrl_5_code
    global proc_3_Mtrl_6_code

    global proc_3_txt
    global proc_3_stop_btn
    global proc_3_err_msg
    global proc_3_err_msg_txt
    global proc_3_is_wrong_itm
    global is_read_proc3_csv

    global log_count

    global sound_title

    global ser

    is_mtr_read = ""

    org_file = os.path.getmtime(setting_proc_3_dir() + r"\log000_3.csv")
    while prog_run:
        try:
            curr_file = os.path.getmtime(setting_proc_3_dir() + r"\log000_3.csv")
        except:
            print

        if proc_3_err_msg_txt == "Loading...":
            proc_3_err_msg_txt = "Loading"
            proc_3_err_msg.config(text=proc_3_err_msg_txt)
        else:
            proc_3_err_msg_txt += "."
            proc_3_err_msg.config(text=proc_3_err_msg_txt)

        if curr_file != org_file:
            proc_3_err_mtr_detect = False
            is_read_proc3_csv = False

            print("Changes Detected")

            while not is_read_proc3_csv:
                try:
                    read_proc_3_csv()
                    is_read_proc3_csv = True
                except:
                    print

            temp_df_vt_3 = proc_3_csv.tail(1)

            # Forced Reading Of JobOrder
            while True:
                # try:
                if temp_df_vt_3["Process 3 Repaired Action"].values[0] != "-":
                    print("Reading All Data")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    is_mtr_read = True
                    break
                else:
                    print("Reading Data Today")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    is_mtr_read = True
                    break
                # except:
                #     is_mtr_read = False
                #     break

            if is_mtr_read:
                # 60CAT0213P, 60CAT0203P
                if (
                    temp_df_vt_3["Process 3 Model Code"].values == "60CAT0213P"
                    or temp_df_vt_3["Process 3 Model Code"].values == "60CAT0203P"
                ):

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Frame Gasket"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Frame Gasket Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongFrameGasket"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Casing Block"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong CSB Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongCSB"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Casing Gasket"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Casing Gasket Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongCasingGasket"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 M4x16 Screw 1"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong M4X16 Screw Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongM4X16Screw"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 M4x16 Screw 2"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong M4x16 Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongM4X16Screw"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Ball Cushion"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Ball Cushion Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongBallCushion"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Partition Board"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Partition Board Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongPartitionBoard"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Built In Tube 1"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Built In Tube Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongBuiltInTube"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Built In Tube 2"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Built In Tube Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongBuiltInTube"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Frame Cover"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Frame Cover Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongFrameCover"
                        proc_3_start_voice(sound_title)

                # 60CAT0212P, 60CAT0202P
                if (
                    temp_df_vt_3["Process 3 Model Code"].values == "60CAT0212P"
                    or temp_df_vt_3["Process 3 Model Code"].values == "60CAT0202P"
                ):

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Frame Gasket"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Frame Gasket Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongFrameGasket"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Casing Block"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong CSB Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongCSB"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Casing Gasket"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Casing Gasket Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongCasingGasket"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 M4x16 Screw 1"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong M4X16 Screw Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        sound_title = "Process3WrongM4X16Screw"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 M4x16 Screw 2"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong M4X16 Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongM4X16Screw"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Ball Cushion"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Ball Cushion Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongBallCushion"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Frame Cover"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Frame Cover Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongFrameCover"
                        proc_3_start_voice(sound_title)

                # 60FC00902P , 60FC00903P, 60FC00905P, 60FC00000P
                if (
                    temp_df_vt_3["Process 3 Model Code"].values == "60FC00902P"
                    or temp_df_vt_3["Process 3 Model Code"].values == "60FC00903P"
                    or temp_df_vt_3["Process 3 Model Code"].values == "60FC00905P"
                    or temp_df_vt_3["Process 3 Model Code"].values == "60FC00000P"
                ):
                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Frame Cover"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Frame Cover Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongFrameCover"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Head Cover"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Head Cover Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongHeadCover"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Casing Packing"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Casing Packing Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongCasingPacking"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 M4x12 Screw"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong M4X12 Screw Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongM4X12Screw"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Csb L"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Casing Left Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongCasingLeft"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Csb R"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Casing Right Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongCasingRight"
                        proc_3_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_3["Process 3 Head Packing"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_3_err_mtr_detect = True
                        proc_3_is_wrong_itm = True
                        proc_3_err_msg_txt = "Wrong Head Packing Used In Process 3"
                        proc_3_err_msg.config(text=proc_3_err_msg_txt)
                        proc_3_stop_btn.config(bg="red")
                        # ser.write(b'H')
                        sound_title = "Process3WrongHeadPacking"
                        proc_3_start_voice(sound_title)

            if not proc_3_err_mtr_detect:
                # --- TIME TOLERANCE CHECK ---
                try:
                    actual_time = float(temp_df_vt_3["Process 3 Actual Time"].values[0])
                    st_time = float(temp_df_vt_3["Process 3 ST"].values[0])
                    print(
                        f"[DEBUG] Process 3: actual_time={actual_time}, st_time={st_time}"
                    )
                    is_within, min_time, max_time = check_time_tolerance(
                        actual_time, st_time
                    )
                    print(
                        f"[DEBUG] Process 3: is_within={is_within}, min_time={min_time}, max_time={max_time}"
                    )
                    if is_within:
                        proc_3_txt.config(text="Process 3", fg="black")
                        proc_3_err_msg.config(
                            text=f"Process 3 Time Within Tolerance (min: {min_time:.2f}, max: {max_time:.2f})",
                            fg="darkgreen",
                        )
                        proc_3_stop_btn.config(bg="orange")
                        proc_3_time_out_of_tolerance = False
                        proc_3_time_text.config(state="normal")
                        proc_3_time_text.delete("1.0", tk.END)
                        proc_3_time_text.insert(
                            tk.END,
                            f"[Within Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                        )
                        proc_3_time_text.config(state="disabled")
                        threading.Thread(
                            target=mtr_correct, args=(proc_3_txt, "Process 3")
                        ).start()
                    else:
                        proc_3_txt.config(text="Process 3", fg="black")
                        proc_3_err_msg.config(text="Loading...", fg="black")
                        proc_3_stop_btn.config(bg="red")
                        proc_3_time_out_of_tolerance = True
                        proc_3_time_text.config(state="normal")
                        proc_3_time_text.delete("1.0", tk.END)
                        proc_3_time_text.insert(
                            tk.END,
                            f"[Time Out of Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                        )
                        proc_3_time_text.config(state="disabled")
                        ser.write(b"H")
                except Exception as e:
                    print(f"[ERROR] Time tolerance check failed for Process 3: {e}")
                    proc_3_txt.config(text="Process 3", fg="black")
                    proc_3_err_msg.config(text="Process 3", fg="black")
                    proc_3_stop_btn.config(bg="orange")
                    proc_3_time_out_of_tolerance = False
                    threading.Thread(
                        target=mtr_correct, args=(proc_3_txt, "Process 3")
                    ).start()
            else:
                if (
                    temp_df_vt_3["Process 3 Frame Gasket"].values[0] == ""
                    and temp_df_vt_3["Process 3 Casing Block"].values[0] == ""
                    and temp_df_vt_3["Process 3 Casing Gasket"].values[0] == ""
                    and temp_df_vt_3["Process 3 M4x16 Screw 1"].values[0] == ""
                    and temp_df_vt_3["Process 3 M4x16 Screw 2"].values[0] == ""
                    and temp_df_vt_3["Process 3 Ball Cushion"].values[0] == ""
                    and temp_df_vt_3["Process 3 Partition Board"].values[0] == ""
                    and temp_df_vt_3["Process 3 Built In Tube 1"].values[0] == ""
                    and temp_df_vt_3["Process 3 Built In Tube 2"].values[0] == ""
                    and temp_df_vt_3["Process 3 Frame Cover"].values[0] == ""
                ):
                    threading.Thread(
                        target=no_mtr_read, args=(proc_3_txt, "Process 3")
                    ).start()
            org_file = curr_file
        print("Reading Files")

        # #Clearing Cmd Logs When Reaches 10 Lines
        # logCount += 1
        # if logCount >= 10:
        #     os.system('cls')
        #     logCount = 0
        time.sleep(1)

    if proc_3_time_out_of_tolerance:
        proc_3_txt.config(text="Process 3", fg="black")
        proc_3_err_msg.config(text="Loading...", fg="black")
        proc_3_stop_btn.config(bg="orange")
        proc_3_time_out_of_tolerance = False
        proc_3_time_text.config(state="normal")
        proc_3_time_text.delete("1.0", tk.END)
        proc_3_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 3: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


# %%
def check_proc_4_err_itm():
    global prog_run

    # PROCESS 4
    global proc_4_csv

    global proc_4_Mtrl_1_code
    global proc_4_Mtrl_2_code
    global proc_4_Mtrl_3_code
    global proc_4_Mtrl_4_code
    global proc_4_Mtrl_5_code
    global proc_4_Mtrl_6_code

    global proc_4_txt
    global proc_4_stop_btn
    global proc_4_err_msg
    global proc_4_err_msg_txt
    global proc_4_is_wrong_itm
    global is_read_proc4_csv

    global log_count

    global sound_title

    global ser

    is_mtr_read = ""

    org_file = os.path.getmtime(setting_proc_4_dir() + r"\log000_4.csv")

    while prog_run:
        try:
            curr_file = os.path.getmtime(setting_proc_4_dir() + r"\log000_4.csv")
        except:
            print

        if proc_4_err_msg_txt == "Loading...":
            proc_4_err_msg_txt = "Loading"
            proc_4_err_msg.config(text=proc_4_err_msg_txt)
        else:
            proc_4_err_msg_txt += "."
            proc_4_err_msg.config(text=proc_4_err_msg_txt)

        if curr_file != org_file:
            proc_4_err_mtr_detect = False
            is_read_proc4_csv = False

            print("Changes Detected")

            while not is_read_proc4_csv:
                try:
                    read_proc_4_csv()
                    is_read_proc4_csv = True
                except Exception as e:
                    print(f"Error reading CSV: {e}")

            temp_df_vt_4 = proc_4_csv.tail(1)

            while True:
                try:
                    if temp_df_vt_4["Process 4 Repaired Action"].values[0] != "-":
                        print("Reading All Data")
                        JOManager.check_job_orders()
                        JOManager.find_materials()
                        is_mtr_read = True
                        break
                    else:
                        print("Reading Data Today")
                        JOManager.check_job_orders()
                        JOManager.find_materials()
                        is_mtr_read = True
                        break
                except Exception as e:
                    print(f"Error reading job orders: {e}")
                    is_mtr_read = False
                    break

            if is_mtr_read:
                # 60CAT0212P, 60CAT0202P
                if (
                    temp_df_vt_4["Process 4 Model Code"].values == "60CAT0212P"
                    or temp_df_vt_4["Process 4 Model Code"].values == "60CAT0202P"
                ):

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Tank"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Tank Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongTank"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Upper Housing"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Upper Housing Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongUpperHousing"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Cord Hook"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Cord Hook Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongCordHook"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 M4x16 Screw"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong M4x16 Screw Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongM4X16Screw"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Tank Gasket"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Tank Gasket Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongTankGasket"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Tank Cover"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Tank Cover Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongTankCover"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Housing Gasket"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Housing Gasket Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongHousingGasket"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 M4x40 Screw"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong M4x40 Screw Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongM4x40Screw"
                        proc_4_start_voice(sound_title)

                # 60CAT0213P, 60CAT0203P
                if (
                    temp_df_vt_4["Process 4 Model Code"].values == "60CAT0213P"
                    or temp_df_vt_4["Process 4 Model Code"].values == "60CAT0203P"
                ):

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Tank"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Tank Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongTank"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Upper Housing"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Upper Housing Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongUpperHousing"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Cord Hook"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Cord Hook Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongCordHook"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 M4x16 Screw"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong M4X16 Screw Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongM4X16Screw"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 PartitionGasket"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Partition Gasket Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongPartitionGasket"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 M4x12 Screw"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong M4x12 Screw Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4Wrongm4x12Screw"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 Housing Gasket"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Housing Gasket Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongHousingGasket"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if temp_df_vt_4["Process 4 M4x40 Screw"].values[0] == a:
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong M4x40 Screw Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongM4x40Screw"
                        proc_4_start_voice(sound_title)

                # \end{code}

                # 60FC00902P, 60FC00903P, 60FC00905P, 60FC00000P
                if (
                    temp_df_vt_4["Process 4 Model Code"].values == "60FC00902P"
                    or temp_df_vt_4["Process 4 Model Code"].values == "60FC00903P"
                    or temp_df_vt_4["Process 4 Model Code"].values == "60FC00905P"
                    or temp_df_vt_4["Process 4 Model Code"].values == "60FC00000P"
                ):
                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if (
                            temp_df_vt_4["Process 4 Material 1 Item Code"].values[0]
                            == a
                        ):
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Muffler Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongMuffler"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if (
                            temp_df_vt_4["Process 4 Material 2 Item Code"].values[0]
                            == a
                        ):
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Muffler Gasket Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongMufflerGasket"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if (
                            temp_df_vt_4["Process 4 Material 3 Item Code"].values[0]
                            == a
                        ):
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong M4X12 Screw Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongM4X12Screw"
                        proc_4_start_voice(sound_title)

                    for a in JOManager.job_order_materials:
                        same_val = 0
                        if (
                            temp_df_vt_4["Process 4 Material 4 Item Code"].values[0]
                            == a
                        ):
                            same_val += 1
                            print(same_val)
                            break
                    if same_val == 0:
                        proc_4_err_mtr_detect = True
                        proc_4_is_wrong_itm = True
                        proc_4_err_msg_txt = "Wrong Rubber Leg Used In Process 4"
                        proc_4_err_msg.config(text=proc_4_err_msg_txt)
                        proc_4_stop_btn.config(bg="red")
                        ##ser.write(b'H')
                        sound_title = "Process4WrongRubberLeg"
                        proc_4_start_voice(sound_title)

            if not proc_4_err_mtr_detect:
                # --- TIME TOLERANCE CHECK ---
                try:
                    actual_time = float(temp_df_vt_4["Process 4 Actual Time"].values[0])
                    st_time = float(temp_df_vt_4["Process 4 ST"].values[0])
                    print(
                        f"[DEBUG] Process 4: actual_time={actual_time}, st_time={st_time}"
                    )
                    is_within, min_time, max_time = check_time_tolerance(
                        actual_time, st_time
                    )
                    print(
                        f"[DEBUG] Process 4: is_within={is_within}, min_time={min_time}, max_time={max_time}"
                    )
                    if is_within:
                        proc_4_txt.config(text="Process 4", fg="black")
                        proc_4_err_msg.config(
                            text=f"Process 4 Time Within Tolerance (min: {min_time:.2f}, max: {max_time:.2f})",
                            fg="darkgreen",
                        )
                        proc_4_stop_btn.config(bg="orange")
                        proc_4_time_out_of_tolerance = False
                        proc_4_time_text.config(state="normal")
                        proc_4_time_text.delete("1.0", tk.END)
                        proc_4_time_text.insert(
                            tk.END,
                            f"[Within Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                        )
                        proc_4_time_text.config(state="disabled")
                        threading.Thread(
                            target=mtr_correct, args=(proc_4_txt, "Process 4")
                        ).start()
                    else:
                        proc_4_txt.config(text="Process 4", fg="black")
                        proc_4_err_msg.config(text="Loading...", fg="black")
                        proc_4_stop_btn.config(bg="red")
                        proc_4_time_out_of_tolerance = True
                        proc_4_time_text.config(state="normal")
                        proc_4_time_text.delete("1.0", tk.END)
                        proc_4_time_text.insert(
                            tk.END,
                            f"[Time Out of Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                        )
                        proc_4_time_text.config(state="disabled")
                        ser.write(b"H")
                except Exception as e:
                    print(f"[ERROR] Time tolerance check failed for Process 4: {e}")
                    proc_4_txt.config(text="Process 4", fg="black")
                    proc_4_err_msg.config(text="Process 4", fg="black")
                    proc_4_stop_btn.config(bg="orange")
                    proc_4_time_out_of_tolerance = False
                    threading.Thread(
                        target=mtr_correct, args=(proc_4_txt, "Process 4")
                    ).start()
            else:
                if (
                    temp_df_vt_4["Process 4 Tank"].values[0] == ""
                    and temp_df_vt_4["Process 4 Upper Housing"].values[0] == ""
                    and temp_df_vt_4["Process 4 Cord Hook"].values[0] == ""
                    and temp_df_vt_4["Process 4 M4x16 Screw"].values[0] == ""
                    and temp_df_vt_4["Process 4 Tank Gasket"].values[0] == ""
                    and temp_df_vt_4["Process 4 Tank Cover"].values[0] == ""
                    and temp_df_vt_4["Process 4 Housing Gasket"].values[0] == ""
                    and temp_df_vt_4["Process 4 M4x40 Screw"].values[0] == ""
                ):
                    threading.Thread(
                        target=no_mtr_read, args=(proc_4_txt, "Process 4")
                    ).start()
            org_file = curr_file
        print("Reading Files")

        # #Clearing Cmd Logs When Reaches 10 Lines
        # logCount += 1
        # if logCount >= 10:
        #     os.system('cls')
        #     logCount = 0
        time.sleep(1)

    if proc_4_time_out_of_tolerance:
        proc_4_txt.config(text="Process 4", fg="black")
        proc_4_err_msg.config(text="Loading...", fg="black")
        proc_4_stop_btn.config(bg="orange")
        proc_4_time_out_of_tolerance = False
        proc_4_time_text.config(state="normal")
        proc_4_time_text.delete("1.0", tk.END)
        proc_4_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 4: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


# %%
def check_proc_5_err_itm():
    global prog_run

    global proc_5_csv

    global proc_5_Mtrl_1_code
    global proc_5_Mtrl_2_code
    global proc_5_Mtrl_3_code
    global proc_5_Mtrl_4_code
    global proc_5_Mtrl_5_code
    global proc_5_Mtrl_6_code

    global proc_5_txt
    global proc_5_stop_btn
    global proc_5_err_msg
    global proc_5_err_msg_txt
    global proc_5_is_wrong_itm
    global is_read_proc5_csv

    global log_count

    global sound_title

    is_mtr_read = ""

    org_file = os.path.getmtime(setting_proc_5_dir() + r"\log000_5.csv")
    while prog_run:
        try:
            curr_file = os.path.getmtime(setting_proc_5_dir() + r"\log000_5.csv")
        except:
            print

        if proc_5_err_msg_txt.startswith("Loading"):
            dots = proc_5_err_msg_txt.count(".")
            if dots >= 3:
                proc_5_err_msg_txt = "Loading"
            else:
                proc_5_err_msg_txt = "Loading" + "." * (dots + 1)
            proc_5_err_msg.config(text=proc_5_err_msg_txt)
        else:
            proc_5_err_msg_txt = "Loading"
            proc_5_err_msg.config(text=proc_5_err_msg_txt)

        if curr_file != org_file:
            proc_5_err_mtr_detect = False
            is_read_proc5_csv = False

            print("Changes Detected")

            while not is_read_proc5_csv:
                try:
                    read_proc_5_csv()
                    is_read_proc5_csv = True
                except:
                    print

            temp_df_vt_5 = proc_5_csv.tail(1)

            while True:
                # try:
                if temp_df_vt_5["Process 5 Repaired Action"].values[0] != "-":
                    print("Reading All Data")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    is_mtr_read = True
                    break
                else:
                    print("Reading Data Today")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    is_mtr_read = True
                    break
                # except:
                #     is_mtr_read = False
                #     break
                
            if is_mtr_read:
                # Check if this is an HPIR job order first
                if JOManager.is_hpir_job_order:
                    # For HPIR job orders, display "Trial Detected" but continue processing
                    proc_5_err_msg_txt = "Trial Detected"
                    proc_5_err_msg.config(text=proc_5_err_msg_txt)
                    proc_5_stop_btn.config(
                        bg="blue"
                    )  # Different color to indicate trial
                    threading.Thread(
                        target=trial_detected, args=(proc_5_txt, "Process 5")
                    ).start()
                else:
                    # Normal processing for non-HPIR job orders
                    # 60CAT0212P, 60CAT0202P, 60CAT0213P, 60CAT0203P
                    if (
                        temp_df_vt_5["Process 5 Model Code"].values == "60CAT0212P"
                        or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0202P"
                        or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0213P"
                        or temp_df_vt_5["Process 5 Model Code"].values == "60CAT0203P"
                    ):

                        for a in JOManager.job_order_materials:
                            same_val = 0
                            if temp_df_vt_5["Process 5 Rating Label"].values[0] == a:
                                same_val += 1
                                print(same_val)
                                break
                        if same_val == 0:
                            proc_5_err_mtr_detect = True
                            proc_5_is_wrong_itm = True
                            proc_5_err_msg_txt = "Wrong Rating Label Used In Process 5"
                            proc_5_err_msg.config(text=proc_5_err_msg_txt)
                            proc_5_stop_btn.config(bg="red")
                            # #ser.write(b'H')
                            sound_title = "Process5WrongRatingLabel"
                            proc_5_start_voice(sound_title)

                    if not proc_5_err_mtr_detect:
                        # --- TIME TOLERANCE CHECK ---
                        try:
                            actual_time = float(
                                temp_df_vt_5["Process 5 Actual Time"].values[0]
                            )
                            st_time = float(temp_df_vt_5["Process 5 ST"].values[0])
                            print(
                                f"[DEBUG] Process 5: actual_time={actual_time}, st_time={st_time}"
                            )
                            is_within, min_time, max_time = check_time_tolerance(
                                actual_time, st_time
                            )
                            print(
                                f"[DEBUG] Process 5: is_within={is_within}, min_time={min_time}, max_time={max_time}"
                            )
                            if is_within:
                                proc_5_txt.config(text="Process 5", fg="black")
                                proc_5_err_msg.config(
                                    text=f"Process 5 Time Within Tolerance (min: {min_time:.2f}, max: {max_time:.2f})",
                                    fg="darkgreen",
                                )
                                proc_5_stop_btn.config(bg="orange")
                                proc_5_time_out_of_tolerance = False
                                proc_5_time_text.config(state="normal")
                                proc_5_time_text.delete("1.0", tk.END)
                                proc_5_time_text.insert(
                                    tk.END,
                                    f"[Within Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                                )
                                proc_5_time_text.config(state="disabled")
                                threading.Thread(
                                    target=mtr_correct, args=(proc_5_txt, "Process 5")
                                ).start()
                            else:
                                proc_5_txt.config(text="Process 5", fg="black")
                                proc_5_err_msg.config(text="Loading...", fg="black")
                                proc_5_stop_btn.config(bg="red")
                                proc_5_time_out_of_tolerance = True
                                proc_5_time_text.config(state="normal")
                                proc_5_time_text.delete("1.0", tk.END)
                                proc_5_time_text.insert(
                                    tk.END,
                                    f"[Time Out of Tolerance] Actual: {actual_time:.2f}, ST: {st_time:.2f}, Min: {min_time:.2f}, Max: {max_time:.2f}\n",
                                )
                                proc_5_time_text.config(state="disabled")
                                ser.write(b"H")
                        except Exception as e:
                            print(
                                f"[ERROR] Time tolerance check failed for Process 5: {e}"
                            )
                            proc_5_txt.config(text="Process 5", fg="black")
                            proc_5_err_msg.config(text="Process 5", fg="black")
                            proc_5_stop_btn.config(bg="orange")
                            proc_5_time_out_of_tolerance = False
                            threading.Thread(
                                target=mtr_correct, args=(proc_5_txt, "Process 5")
                            ).start()
            else:
                if JOManager.is_hpir_job_order:
                    # For HPIR job orders, display "Trial Detected" even when no material is read
                    proc_5_err_msg_txt = "Trial Detected"
                    proc_5_err_msg.config(text=proc_5_err_msg_txt)
                    proc_5_stop_btn.config(bg="blue")
                    threading.Thread(
                        target=trial_detected, args=(proc_5_txt, "Process 5")
                    ).start()
                else:
                    if temp_df_vt_5["Process 5 Rating Label"].values[0] == "":
                        threading.Thread(
                            target=no_mtr_read, args=(proc_5_txt, "Process 5")
                        ).start()
            org_file = curr_file
        print("Reading Files")

        # #Clearing Cmd Logs When Reaches 10 Lines
        # logCount += 1
        # if logCount >= 10:
        #     os.system('cls')
        #     logCount = 0
        time.sleep(1)

    if proc_5_time_out_of_tolerance:
        proc_5_txt.config(text="Process 5", fg="black")
        proc_5_err_msg.config(text="Loading...", fg="black")
        proc_5_stop_btn.config(bg="orange")
        proc_5_time_out_of_tolerance = False
        proc_5_time_text.config(state="normal")
        proc_5_time_text.delete("1.0", tk.END)
        proc_5_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 5: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


# %%
def check_proc_6_err_itm():
    global ser

    global prog_run

    global proc_6_csv

    global proc_6_Mtrl_1_code

    global proc_6_txt
    global proc_6_stop_btn
    global proc_6_err_msg
    global proc_6_err_msg_txt
    global proc_6_is_wrong_itm
    global is_read_proc6_csv

    global log_count

    global sound_title

    is_mtr_read = ""

    org_file = os.path.getmtime(setting_proc_6_dir() + r"\log000_6.csv")
    while prog_run:
        try:
            curr_file = os.path.getmtime(setting_proc_6_dir() + r"\log000_6.csv")
        except:
            print

        if proc_6_err_msg_txt.startswith("Loading"):
            dots = proc_6_err_msg_txt.count(".")
            if dots >= 3:
                proc_6_err_msg_txt = "Loading"
            else:
                proc_6_err_msg_txt = "Loading" + "." * (dots + 1)
            proc_6_err_msg.config(text=proc_6_err_msg_txt)
        else:
            proc_6_err_msg_txt = "Loading"
            proc_6_err_msg.config(text=proc_6_err_msg_txt)

        if curr_file != org_file:
            proc_6_wrong_itm_detect = False
            is_read_proc6_csv = False

            print("[DEBUG] Process 6: Changes Detected")

            while not is_read_proc6_csv:
                try:
                    read_proc_6_csv()
                    is_read_proc6_csv = True
                except:
                    print

            temp_df_vt_6 = proc_6_csv.tail(1)

            while True:
                # try:
                if temp_df_vt_6["Process 6 Repaired Action"].values[0] != "-":
                    print("[DEBUG] Process 6: Reading All Data")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    is_mtr_read = True
                    break
                else:
                    print("[DEBUG] Process 6: Reading Data Today")
                    JOManager.check_job_orders()
                    JOManager.find_materials()
                    is_mtr_read = True
                    break
                # except:
                #     is_mtr_read = False
                #     break

            # #Writing Done In Specific Number In JobOrderSerial CSV
            # JOManager.WriteDoneInJobOrder()

            if is_mtr_read:
                # Check if this is an HPIR job order first
                if JOManager.is_hpir_job_order:
                    # For HPIR job orders, display "Trial Detected" but continue processing
                    proc_6_err_msg_txt = "Trial Detected"
                    proc_6_err_msg.config(text=proc_6_err_msg_txt)
                    proc_6_stop_btn.config(
                        bg="blue"
                    )  # Different color to indicate trial
                    threading.Thread(
                        target=trial_detected, args=(proc_6_txt, "Process 6")
                    ).start()
                else:
                    # Normal processing for non-HPIR job orders
                    # 60CAT0212P, 60CAT0202P, 60CAT0213P, 60CAT0203P
                    if (
                        temp_df_vt_6["Process 6 Model Code"].values == "60CAT0212P"
                        or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0202P"
                        or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0213P"
                        or temp_df_vt_6["Process 6 Model Code"].values == "60CAT0203P"
                        or temp_df_vt_6["Process 6 Model Code"].values == "60FC00902P"
                        or temp_df_vt_6["Process 6 Model Code"].values == "60FC00903P"
                        or temp_df_vt_6["Process 6 Model Code"].values == "60FC00905P"
                        or temp_df_vt_6["Process 6 Model Code"].values == "60FC00000P"
                    ):

                        for a in JOManager.job_order_materials:
                            same_val = 0
                            if temp_df_vt_6["Process 6 Vinyl"].values[0] == a:
                                same_val += 1
                                print(same_val)
                                break
                        if same_val == 0:
                            proc_6_wrong_itm_detect = True
                            proc_6_is_wrong_itm = True
                            proc_6_err_msg_txt = "Wrong Vinyl Used In Process 6"
                            proc_6_err_msg.config(text=proc_6_err_msg_txt)
                            proc_6_stop_btn.config(bg="red")
                            # ser.write(b'H')
                            sound_title = "Process6WrongVinyl"
                            proc_6_start_voice(sound_title)

                    if not proc_6_wrong_itm_detect:
                        if JOManager.is_hpir_job_order:
                            # For HPIR job orders, display "Trial Detected" even when no material is read
                            proc_6_err_msg_txt = "Trial Detected"
                            proc_6_err_msg.config(text=proc_6_err_msg_txt)
                            proc_6_stop_btn.config(bg="blue")
                            threading.Thread(
                                target=trial_detected, args=(proc_6_txt, "Process 6")
                            ).start()
                        else:
                            if temp_df_vt_6["Process 6 Vinyl"].values[0] == "":
                                threading.Thread(
                                    target=no_mtr_read, args=(proc_6_txt, "Process 6")
                                ).start()
            org_file = curr_file
        print("Reading Files")

        # #Clearing Cmd Logs When Reaches 10 Lines
        # logCount += 1
        # if logCount >= 10:
        #     os.system('cls')
        #     logCount = 0
        time.sleep(1)

    if proc_6_time_out_of_tolerance:
        proc_6_txt.config(text="Process 6", fg="black")
        proc_6_err_msg.config(text="Loading...", fg="black")
        proc_6_stop_btn.config(bg="orange")
        proc_6_time_out_of_tolerance = False
        proc_6_time_text.config(state="normal")
        proc_6_time_text.delete("1.0", tk.END)
        proc_6_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 6: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


# %%
def disable_proc_1_wrong_itm():
    global Engine
    global ser
    global proc_1_is_wrong_itm
    global proc_1_err_msg
    global proc_1_err_msg_txt
    global proc_1_stop_btn
    global proc_1_time_out_of_tolerance
    global proc_1_txt

    if proc_1_is_wrong_itm:
        # ser.write(b'L')
        stop_mp3()

    # Reset time tolerance error state and UI
    if proc_1_time_out_of_tolerance:
        proc_1_txt.config(text="Process 1", fg="black")
        proc_1_err_msg.config(text="Loading...", fg="black")
        proc_1_stop_btn.config(bg="orange")
        proc_1_time_out_of_tolerance = False
        proc_1_time_text.config(state="normal")
        proc_1_time_text.delete("1.0", tk.END)
        proc_1_time_text.config(state="disabled")

    proc_1_err_msg_txt = "Loading..."
    proc_1_err_msg.config(text=proc_1_err_msg_txt, fg="black")
    proc_1_txt.config(text="Process 1", fg="black")
    proc_1_stop_btn.config(bg="orange")
    proc_1_is_wrong_itm = False

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 1: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


def disable_proc_2_wrong_itm():
    global Engine
    global ser
    global proc_2_is_wrong_itm
    global proc_2_err_msg
    global proc_2_err_msg_txt
    global proc_2_stop_btn
    global proc_2_time_out_of_tolerance
    global proc_2_txt

    if proc_2_is_wrong_itm:
        # ser.write(b'L')
        stop_mp3()

    proc_2_err_msg_txt = "Loading..."
    proc_2_err_msg.config(text=proc_2_err_msg_txt, fg="black")
    proc_2_txt.config(text="Process 2", fg="black")
    proc_2_stop_btn.config(bg="orange")
    proc_2_is_wrong_itm = False

    # Reset time tolerance error state and UI
    if proc_2_time_out_of_tolerance:
        proc_2_txt.config(text="Process 2", fg="black")
        proc_2_err_msg.config(text="Loading...", fg="black")
        proc_2_stop_btn.config(bg="orange")
        proc_2_time_out_of_tolerance = False
        proc_2_time_text.config(state="normal")
        proc_2_time_text.delete("1.0", tk.END)
        proc_2_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 2: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


def disable_proc_3_wrong_itm():
    global Engine
    global ser
    global proc_3_is_wrong_itm
    global proc_3_err_msg
    global proc_3_err_msg_txt
    global proc_3_stop_btn
    global proc_3_time_out_of_tolerance
    global proc_3_txt

    if proc_3_is_wrong_itm:
        # ser.write(b'L')
        stop_mp3()

    proc_3_err_msg_txt = "Loading..."
    proc_3_err_msg.config(text=proc_3_err_msg_txt, fg="black")
    proc_3_txt.config(text="Process 3", fg="black")
    proc_3_stop_btn.config(bg="orange")
    proc_3_is_wrong_itm = False

    # Reset time tolerance error state and UI
    if proc_3_time_out_of_tolerance:
        proc_3_txt.config(text="Process 3", fg="black")
        proc_3_err_msg.config(text="Loading...", fg="black")
        proc_3_stop_btn.config(bg="orange")
        proc_3_time_out_of_tolerance = False
        proc_3_time_text.config(state="normal")
        proc_3_time_text.delete("1.0", tk.END)
        proc_3_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 3: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


def disable_proc_4_wrong_itm():
    global Engine
    global ser
    global proc_4_is_wrong_itm
    global proc_4_err_msg
    global proc_4_err_msg_txt
    global proc_4_stop_btn
    global proc_4_time_out_of_tolerance
    global proc_4_txt

    if proc_4_is_wrong_itm:
        # ser.write(b'L')
        stop_mp3()

    proc_4_err_msg_txt = "Loading..."
    proc_4_err_msg.config(text=proc_4_err_msg_txt, fg="black")
    proc_4_txt.config(text="Process 4", fg="black")
    proc_4_stop_btn.config(bg="orange")
    proc_4_is_wrong_itm = False

    # Reset time tolerance error state and UI
    if proc_4_time_out_of_tolerance:
        proc_4_txt.config(text="Process 4", fg="black")
        proc_4_err_msg.config(text="Loading...", fg="black")
        proc_4_stop_btn.config(bg="orange")
        proc_4_time_out_of_tolerance = False
        proc_4_time_text.config(state="normal")
        proc_4_time_text.delete("1.0", tk.END)
        proc_4_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 4: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


def disable_proc_5_wrong_itm():
    global Engine
    global proc_5_is_wrong_itm
    global proc_5_err_msg
    global proc_5_err_msg_txt
    global proc_5_stop_btn
    global ser
    global proc_5_time_out_of_tolerance
    global proc_5_txt

    if proc_5_is_wrong_itm:
        # ser.write(b'L')
        stop_mp3()

    proc_5_err_msg_txt = "Loading..."
    proc_5_err_msg.config(text=proc_5_err_msg_txt, fg="black")
    proc_5_txt.config(text="Process 5", fg="black")
    proc_5_stop_btn.config(bg="orange")
    proc_5_is_wrong_itm = False

    # Reset time tolerance error state and UI
    if proc_5_time_out_of_tolerance:
        proc_5_txt.config(text="Process 5", fg="black")
        proc_5_err_msg.config(text="Loading...", fg="black")
        proc_5_stop_btn.config(bg="orange")
        proc_5_time_out_of_tolerance = False
        proc_5_time_text.config(state="normal")
        proc_5_time_text.delete("1.0", tk.END)
        proc_5_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 5: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')


def disable_proc_6_wrong_itm():
    global Engine
    global proc_6_is_wrong_itm
    global proc_6_err_msg
    global proc_6_err_msg_txt
    global proc_6_stop_btn
    global ser
    global proc_6_time_out_of_tolerance
    global proc_6_txt

    if proc_6_is_wrong_itm:
        # ser.write(b'L')
        stop_mp3()

    proc_6_err_msg_txt = "Loading..."
    proc_6_err_msg.config(text=proc_6_err_msg_txt, fg="black")
    proc_6_txt.config(text="Process 6", fg="black")
    proc_6_stop_btn.config(bg="orange")
    proc_6_is_wrong_itm = False

    # Reset time tolerance error state and UI
    if proc_6_time_out_of_tolerance:
        proc_6_txt.config(text="Process 6", fg="black")
        proc_6_err_msg.config(text="Loading...", fg="black")
        proc_6_stop_btn.config(bg="orange")
        proc_6_time_out_of_tolerance = False
        proc_6_time_text.config(state="normal")
        proc_6_time_text.delete("1.0", tk.END)
        proc_6_time_text.config(state="disabled")

    # Immediately reset PLC/ESP8266 to RUN state
    print("[STOP BUTTON] Process 6: Sending b'L' (RUN) after STOP pressed")
    ser.write(b'L')

def disable_deviation():
    varMan.deviation_err_msg_text = "Loading..."
    varMan.deviation_err_msg.config(text=varMan.deviation_err_msg_text, fg="black")

    varMan.deviation_txt.config(text="DeviationChecker", fg="black")

    varMan.deviation_stop_btn.config(bg="orange")
    varMan.isDeviationDetected = False

# %%
def stop_prog():
    global prog_run
    global proc_1_is_wrong_itm
    global proc_2_is_wrong_itm
    global proc_3_is_wrong_itm
    global proc_4_is_wrong_itm
    global proc_5_is_wrong_itm
    global proc_6_is_wrong_itm

    prog_run = False
    proc_1_is_wrong_itm = False
    proc_2_is_wrong_itm = False
    proc_3_is_wrong_itm = False
    proc_4_is_wrong_itm = False
    proc_5_is_wrong_itm = False
    proc_6_is_wrong_itm = False

    root.destroy()


# %%
def mtr_correct(proc_txt, proc_num):
    proc_txt.config(text=f"{proc_num} Correct {chr(0x1F44D)}", fg="darkgreen")
    time.sleep(5)
    proc_txt.config(text=f"{proc_num}", fg="black")


# %%
def no_mtr_read(proc_txt, proc_num):
    global ser

    proc_txt.config(text=f"{proc_num} No Material Detected", fg="darkgreen")

    # ser.write(b'H')

    time.sleep(5)
    proc_txt.config(text=f"{proc_num}", fg="black")


# %%
def trial_detected(proc_txt, proc_num):
    proc_txt.config(text=f"{proc_num} Trial Detected", fg="blue")
    time.sleep(5)
    proc_txt.config(text=f"{proc_num}", fg="black")


# %%
def plcStopper():
    global ser
    global prog_run

    last_state = None
    while prog_run:
        should_stop = (
            proc_1_is_wrong_itm or proc_2_is_wrong_itm or proc_3_is_wrong_itm or
            proc_4_is_wrong_itm or proc_5_is_wrong_itm or proc_6_is_wrong_itm or
            proc_1_time_out_of_tolerance or proc_2_time_out_of_tolerance or
            proc_3_time_out_of_tolerance or proc_4_time_out_of_tolerance or
            proc_5_time_out_of_tolerance or proc_6_time_out_of_tolerance or
            varMan.isDeviationDetected # carl
        )
        if should_stop:
            if last_state != 'H':
                print("[PLC] Sending b'H' (STOP) due to error or time out of tolerance")
                ser.write(b'H')
                last_state = 'H'
        else:
            if last_state != 'L':
                print("[PLC] Sending b'L' (RUN) - all clear")
                ser.write(b'L')
                last_state = 'L'
        time.sleep(0.1)

def InsertInLogWindow(message):
    varMan.deviation_time_text.configure(state ='normal')
    # Inserting Text which is read only
    varMan.deviation_time_text.insert(tk.INSERT, f"{message}\n")
    varMan.deviation_time_text.configure(state ='disabled')




# %%
from ctypes import windll
import tkinter as tk


# Fixing Blur/This line ensures the GUI doesn’t appear blurry on high-DPI displays by enabling DPI awareness.
windll.shcore.SetProcessDpiAwareness(1)


# Creates the main window titled "Wrong Material Detector".
# Sets its size and position.
root = tk.Tk()
root.title("Wrong Material Detector")
root.geometry("1480x700+50+50")
# root.resizable(False, False)


# Distributes space across three columns evenly.
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
# place a label on the root windowf
titleText = tk.Label(root, text="Wrong Material Detector", font=("Arial", 21, "bold"))
titleText.grid(column=0, row=0, pady=(0, 40), columnspan=10)

# PROCESS 1
proc_1_txt = tk.Label(root, text="Process 1", font=("Arial", 12, "bold"))
proc_1_txt.grid(column=0, row=1)
proc_1_stop_btn = tk.Button(
    root,
    text="STOP",
    font=("Arial", 12),
    command=disable_proc_1_wrong_itm,
    width=15,
    height=1,
)
proc_1_stop_btn.grid(column=0, row=2, ipadx=5, ipady=5) # Button to stop process 1
proc_1_stop_btn.config(bg="orange", fg="black") # Button color and text
proc_1_err_msg = tk.Label(root, text=proc_1_err_msg_txt, font=("Arial", 12))
proc_1_err_msg.grid(column=0, row=3)
proc_1_time_text = tk.Text(root, height=3, width=40, font=("Arial", 10))
proc_1_time_text.grid(column=0, row=4)
proc_1_time_text.config(state="disabled")
#----------------------------------------------------------DISPLAY STOP BUTTON
# PROCESS 2
proc_2_txt = tk.Label(root, text="Process 2", font=("Arial", 12, "bold"))
proc_2_txt.grid(column=1, row=1)
proc_2_stop_btn = tk.Button(
    root,
    text="STOP",
    font=("Arial", 12),
    command=disable_proc_2_wrong_itm,
    width=15,
    height=1,
)
proc_2_stop_btn.grid(column=1, row=2, ipadx=5, ipady=5)
proc_2_stop_btn.config(bg="orange", fg="black")
proc_2_err_msg = tk.Label(root, text=proc_2_err_msg_txt, font=("Arial", 12))
proc_2_err_msg.grid(column=1, row=3)
#----------------------------------------------------------
proc_2_time_text = tk.Text(root, height=3, width=40, font=("Arial", 10))
proc_2_time_text.grid(column=1, row=4)
proc_2_time_text.config(state="disabled")

# PROCESS 3
proc_3_txt = tk.Label(root, text="Process 3", font=("Arial", 12, "bold"))
proc_3_txt.grid(column=2, row=1)
proc_3_stop_btn = tk.Button(
    root,
    text="STOP",
    font=("Arial", 12),
    command=disable_proc_3_wrong_itm,
    width=15,
    height=1,
)
proc_3_stop_btn.grid(column=2, row=2, ipadx=5, ipady=5)
proc_3_stop_btn.config(bg="orange", fg="black")
proc_3_err_msg = tk.Label(root, text=proc_3_err_msg_txt, font=("Arial", 12))
proc_3_err_msg.grid(column=2, row=3)
proc_3_time_text = tk.Text(root, height=3, width=40, font=("Arial", 10))
proc_3_time_text.grid(column=2, row=4)
proc_3_time_text.config(state="disabled")

# PROCESS 4
proc_4_txt = tk.Label(root, text="Process 4", font=("Arial", 12, "bold"))
proc_4_txt.grid(column=0, row=5, pady=(40, 0))
proc_4_stop_btn = tk.Button(
    root,
    text="STOP",
    font=("Arial", 12),
    command=disable_proc_4_wrong_itm,
    width=15,
    height=1,
)
proc_4_stop_btn.grid(column=0, row=6, ipadx=5, ipady=5)
proc_4_stop_btn.config(bg="orange", fg="black")
proc_4_err_msg = tk.Label(root, text=proc_4_err_msg_txt, font=("Arial", 12))
proc_4_err_msg.grid(column=0, row=7)
proc_4_time_text = tk.Text(root, height=3, width=40, font=("Arial", 10))
proc_4_time_text.grid(column=0, row=8)
proc_4_time_text.config(state="disabled")

# PROCESS 5
proc_5_txt = tk.Label(root, text="Process 5", font=("Arial", 12, "bold"))
proc_5_txt.grid(column=1, row=5, pady=(40, 0))
proc_5_stop_btn = tk.Button(
    root,
    text="STOP",
    font=("Arial", 12),
    command=disable_proc_5_wrong_itm,
    width=15,
    height=1,
)
proc_5_stop_btn.grid(column=1, row=6, ipadx=5, ipady=5)
proc_5_stop_btn.config(bg="orange", fg="black")
proc_5_err_msg = tk.Label(root, text=proc_5_err_msg_txt, font=("Arial", 12))
proc_5_err_msg.grid(column=1, row=7)
proc_5_time_text = tk.Text(root, height=3, width=40, font=("Arial", 10))
proc_5_time_text.grid(column=1, row=8)
proc_5_time_text.config(state="disabled")

# PROCESS 6
proc_6_txt = tk.Label(root, text="Process 6", font=("Arial", 12, "bold"))
proc_6_txt.grid(column=2, row=5, pady=(40, 0))
proc_6_stop_btn = tk.Button(
    root,
    text="STOP",
    font=("Arial", 12),
    command=disable_proc_6_wrong_itm,
    width=15,
    height=1,
)
proc_6_stop_btn.grid(column=2, row=6, ipadx=5, ipady=5)
proc_6_stop_btn.config(bg="orange", fg="black")
proc_6_err_msg = tk.Label(root, text=proc_6_err_msg_txt, font=("Arial", 12))
proc_6_err_msg.grid(column=2, row=7)
proc_6_time_text = tk.Text(root, height=3, width=40, font=("Arial", 10))
proc_6_time_text.grid(column=2, row=8)
proc_6_time_text.config(state="disabled")

# TEXT (DeviationChecker)
varMan.deviation_txt = tk.Label(root, text="DeviationChecker", font=("Arial", 12, "bold"))
varMan.deviation_txt.grid(column=0, row=9, pady=(40, 0))

# STOP BUTTON
varMan.deviation_stop_btn = tk.Button(
    root,
    text="STOP",
    font=("Arial", 12),
    command=disable_deviation,
    width=15,
    height=1,
)
varMan.deviation_stop_btn.grid(column=0, row=10, ipadx=5, ipady=5)
varMan.deviation_stop_btn.config(bg="orange", fg="black")

# LOADING MESSAGE
varMan.deviation_err_msg = tk.Label(root, text=varMan.deviation_err_msg_text, font=("Arial", 12))
varMan.deviation_err_msg.grid(column=0, row=11)

# LOG BOX
varMan.deviation_time_text = tk.Text(root, height=8, width=70, font=("Arial", 10))
varMan.deviation_time_text.grid(column=0, row=12)
varMan.deviation_time_text.config(state="disabled")


#  !------------------------------------THREADS SECTION------------------------------------!

check_proc_1 = threading.Thread(target=check_proc_1_err_itm)
check_proc_1.start()
check_proc_2 = threading.Thread(target=check_proc_2_err_itm)
check_proc_2.start()
check_proc_3 = threading.Thread(target=check_proc_3_err_itm)
check_proc_3.start()
check_proc_4 = threading.Thread(target=check_proc_4_err_itm)
check_proc_4.start()
check_proc_5 = threading.Thread(target=check_proc_5_err_itm)
check_proc_5.start()
check_proc_6 = threading.Thread(target=check_proc_6_err_itm)
check_proc_6.start()
plc_stopper = threading.Thread(target=plcStopper)
plc_stopper.start()

deviation_Checker = threading.Thread(target=ExecutableManager.run) # carl
deviation_Checker.start()   # carl

#  !------------------------------------THREADS SECTION------------------------------------!

root.protocol("WM_DELETE_WINDOW", stop_prog)
root.mainloop()
