import time
import pandas as pd
import numpy as np
import logging
import gc
import os
import socket

from pathlib import Path
from datetime import datetime
from ftplib import FTP
from payout_app.email_sender import Email_Sender
from payout_app.models import Query

try:
    from .oracle_config import Ora
except:
    from oracle_config import Ora


class Support:
    def __init__(self, *args, **kwargs):
        "Later define a init fuction as per requirement"

    def delete_dataframe(self, dataframe):
        del [[dataframe]]
        gc.collect()
        dataframe = pd.DataFrame()
        return dataframe

    def excel_generator(self, excel_data, page_name, from_date=None, to_date=None):
        # datetime object containing current date and time
        add_time_to_page = datetime.now()

        # dd/mm/YY H:M:S
        # Add time with miliseconds to avoid conflict with apache and nginx
        if from_date and to_date:
            add_time_to_page_string = f"{from_date}--TO--{to_date}"
        else:
            add_time_to_page_string = add_time_to_page.strftime("%d-%b-%Y-%H-%M-%S-%f")
            add_time_to_page_string = str(add_time_to_page_string)

        # gives you location of manage.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # write the print fuction in error log. Test on Apache reverse proxy but not on nginx
        # sys.stderr.write(excel_file_path)

        excel_file_path = (
            f"{current_dir}/excel_files/{page_name}-{add_time_to_page_string}.xlsx"
        )

        # creates a log file and report errors
        # logging.basicConfig(filename="report_error.log", level=logging.DEBUG)
        # logging.error(f"Error on {add_time_to_page_string} :")
        # sys.stderr.write(excel_file_path)

        # excel_file_path = page_name + ".xlsx"
        # excel_data = pd.DataFrame(data=data, columns=list(column))

        # Set destination directory to save excel.
        generate_excel = pd.ExcelWriter(
            excel_file_path,
            engine="xlsxwriter",
            datetime_format="dd-mm-yyyy hh:mm:ss",
            date_format="dd-mm-yyyy",
        )

        # Write excel to file using pandas to_excel
        if len(page_name) > 31:
            page_name = page_name[0:31]
        excel_data.to_excel(
            generate_excel, startrow=0, sheet_name=page_name, index=False
        )

        # Indicate workbook and worksheet for formatting
        workbook = generate_excel.book
        worksheet = generate_excel.sheets[page_name]

        # Iterate through each column and set the width == the max length in that column. A padding length of 2 is also added.
        for i, col in enumerate(excel_data.columns):
            # find length of column i
            try:
                column_len = excel_data[col].astype(str).str.len().max()

            except:
                pass

            # Setting the length if the column header is larger
            # than the max column value length
            try:
                column_len = max(column_len, len(col)) + 4

            except:
                pass

            # set the column length
            worksheet.set_column(i, i, column_len)

        generate_excel.close()
        return excel_file_path

    def error_log(self):
        """
        Prints an error message and exits the program
        """
        logging.basicConfig(filename="timestamp.log", level=logging.DEBUG)
        timenow = datetime.now()
        timenow_string = timenow.strftime("%d-%b-%Y-%H-%M-%S-%f")
        timenow_string = str(timenow_string)
        logging.info(f"Finished processing on :  {timenow_string}")

    def filter_colum_from_keyword(self, dataframe, column_name, keyword):
        dataframe.drop(
            dataframe[dataframe["PATIENT_TYPE"] == "Emergency"].index, inplace=True
        )
        return dataframe

    def add_new_column(self, dataframe, column_name, column_value):
        dataframe[column_name] = column_value
        return dataframe

    def concat_dataframes(self, dataframe1, dataframe2):
        df_merged = pd.concat([dataframe1, dataframe2], ignore_index=True, sort=False)
        return df_merged

    def filter_aplicable_doctor(
        self,
        main_dataframe,
        main_dataframe_column,
        doctors_list_df,
        doctors_list_df_column,
    ):
        main_dataframe = main_dataframe[
            main_dataframe[main_dataframe_column]
            .apply(str.upper)
            .isin(doctors_list_df[doctors_list_df_column].apply(str.upper))
        ]
        return main_dataframe

    def rename_columns(self, dataframe, dist):
        dataframe.rename(columns=dist, inplace=True)
        return dataframe

    def delete_columns(self, dataframe, col_list):
        dataframe.drop(col_list, axis=1, inplace=True)
        return dataframe

    def CINP_OR_CNOP_ANE(self, row):
        if "CNIP" in row:
            return "IP Consultation"
        elif "CNOP" in row:
            return "OP Consultation"
        else:
            return "Procedure"

        # dataframe["REFERENCE_GROUP"] = [
        #     "IP Consultation" if "CNIP" in x else "Procedure"
        #     for x in dataframe["SERVICE_CODE"]
        # ]
        # return dataframe

    def set_dataframe(self, dataframe):
        self.dataframe = dataframe

    def get_dataframe(self):
        return self.dataframe

    def transplant_working(self, dataframe, tranplant_df, uhid_list):
        # run Query to get Transplant Doctors

        transplant_doctor = set(tranplant_df["doctors_name"])
        uhid_list = set(uhid_list)
        #  Itteration
        for i in range(len(dataframe)):
            # Curent Row
            row = dataframe.iloc[[i]]
            row_uhid = set(row["PATIENT_ID"])
            # set doc name to find
            doc_name_in_df = set([dataframe.at[i, "DOCTOR_NAME"]])

            # Finally intersection between current uhid and uhid from Transplant list give by Rekha Barot
            if row_uhid.intersection(uhid_list):
                # Intersect doctor name and query doctors name
                if doc_name_in_df.intersection(transplant_doctor):
                    # To find Transplant keyword
                    if "transplant" in dataframe.at[i, "SERVICE_DESC"].lower():
                        # defining Doctor share
                        dr_share_t = int(dataframe.at[i, "DOCTOR_SHARE"])
                        # Iteration and adding all doctor from query to main dataframe
                        for doc in transplant_doctor:
                            row["DOCTOR_NAME"] = doc
                            doctors_share = float(
                                tranplant_df[tranplant_df["doctors_name"].isin([doc])][
                                    "doctors_share"
                                ]
                            )
                            row["DOCTOR_SHARE"] = (
                                float(dr_share_t) * doctors_share / 100
                            )
                            # adding all current row with changed doctor and doctor share accoridng to the caculations
                            dataframe = self.concat_dataframes(dataframe, row)
                        # Changing value to empty sting after calculation and distribution
                        dataframe.at[i, "DOCTOR_SHARE"] = ""

                    # same iteration from above only key word difference
                    if "surgeon fees su" in dataframe.at[i, "SERVICE_DESC"].lower():
                        dr_share_s = float(dataframe.at[i, "DOCTOR_SHARE"])
                        for doc in transplant_doctor:
                            row["DOCTOR_NAME"] = doc
                            doctors_share = float(
                                tranplant_df[tranplant_df["doctors_name"].isin([doc])][
                                    "doctors_share"
                                ]
                            )
                            row["DOCTOR_SHARE"] = (
                                float(dr_share_s) * doctors_share / 100
                            )

                            dataframe = self.concat_dataframes(dataframe, row)
                        dataframe.at[i, "DOCTOR_SHARE"] = ""

        return dataframe

    def srs_distribution(self, dataframe):
        # Iterate through each filtered DataFrame.
        filter_df_srs = dataframe[
            dataframe["SERVICE_DESC"].isin(["EDGE SRS Doctor Fees"])
        ]
        if not filter_df_srs.empty:
            for i in range(len(filter_df_srs)):
                # Define Current Row
                row = filter_df_srs.iloc[[i]]
                # Define Doctor Share
                dr_share_amount = float(row["DOCTOR_SHARE"])

                # Insert First doctor share and d
                row["DOCTOR_SHARE"] = dr_share_amount * 0.5

                # Upack index value
                index = "".join(str(elem) for i, elem in enumerate(row.index))
                dataframe.at[int(index), "DOCTOR_SHARE"] = ""
                dataframe = self.concat_dataframes(dataframe, row)

                # TO find the order doctor in Radiation department and add his name and share in the Dataframe
                filter_df = dataframe[
                    dataframe["EPISODE_ID"].isin([int(row["EPISODE_ID"])])
                ]
                filter_df = filter_df[
                    ~filter_df["DOCTOR_NAME"].isin(list(row["DOCTOR_NAME"]))
                ]
                print(filter_df)
                print(filter_df.shape)
                if not filter_df.empty:
                    print("Was not empty")
                    row["DOCTOR_NAME"] = filter_df.iloc[0]["DOCTOR_NAME"]
                    dataframe = self.concat_dataframes(dataframe, row)
        try:
            del filter_df
        except Exception:
            pass
        try:
            del filter_df_srs
        except Exception:
            pass

        return dataframe

    def check_peadiatric(self, dataframe):
        df_filter = ""
        # Filter Only Peadiatric Fe
        pead_filter_df = dataframe[dataframe["SERVICE_DESC"].isin(["Paediatrican Fe"])]

        for i in range(len(pead_filter_df)):
            # Current row with pead fe
            row = pead_filter_df.iloc[[i]]
            # convert pr number from dataframe object  to string
            pr_number = "".join(
                [str(elem) for i, elem in enumerate(row["PHYSICIAN_ID"])]
            )

            # check if dr is a peads dr from Oracle Database
            sql_qurey = Query.objects.get(query_name="Check Paediatric Doctors").query
            sql_qurey = sql_qurey.format(variable=f"'{pr_number}'")
            db = Ora()
            doctor_data, _ = db.run_query(sql_qurey)
            # doctor_data = db.check_dr_pead(pr_number)

            # IF Dr is not Peadiatric  change the doctor name
            if not doctor_data:
                #  change index value from pandas object to string
                index = "".join(str(elem) for i, elem in enumerate(row.index))
                dataframe.at[int(index), "DOCTOR_SHARE"] = ""

                # Filter the found patient from dataframe to get all doctor
                df_filter = dataframe[
                    dataframe["PATIENT_ID"].isin(row["PATIENT_ID"].values.astype(str))
                ]

                # Filter the current unwanted doctor
                df_filter = df_filter[
                    ~df_filter["DOCTOR_NAME"].isin(row["DOCTOR_NAME"])
                ]

                for i in range(len(df_filter)):
                    df_row = df_filter.iloc[[i]]

                    # get pr numbers of other doctors to check , also convert prnumber from dataframe object to string
                    pr_number_df = "".join(
                        [str(elem) for i, elem in enumerate(df_row["PHYSICIAN_ID"])]
                    )

                    # Check wheter doctor is a peads doctors
                    db = Ora()
                    sql_qurey = Query.objects.get(
                        query_name="Check Paediatric Doctors"
                    ).query
                    sql_qurey = sql_qurey.format(variable=f"'{pr_number}'")
                    find_if_paeds, _ = db.run_query(sql_qurey)
                    # find_if_paeds = db.check_dr_pead(pr_number_df)

                    if find_if_paeds:
                        old_dr_name = dataframe.at[int(index), "DOCTOR_NAME"]

                        new_dr_name = df_row["DOCTOR_NAME"].values.astype(str)[0]

                        # change the old dr name to new doctor who is a peads
                        dataframe.at[int(index), "DOCTOR_NAME"] = new_dr_name

                        # Add A comment in the comment section
                        dataframe.at[
                            int(index), "COMMENTS"
                        ] = f"Changed from {old_dr_name} to {new_dr_name}"
        try:
            del pead_filter_df
        except Exception:
            pass
        try:
            del df_filter
        except Exception:
            pass
        return dataframe

    def ehc_patient_working(self, dataframe, doctors_list_df, from_date, to_date):
        sql_qurey = Query.objects.get(query_name="Doctors Share on EHC").query
        sql_qurey = sql_qurey.format(from_date=f"'{from_date}'", to_date=f"'{to_date}'")
        db = Ora()
        ehc_data, ehc_column = db.run_query(sql_qurey)
        # ehc_data, ehc_column = db.ehc_dr_share("01-Aug-2022", "31-Aug-2022")
        ehc_df = pd.DataFrame(data=ehc_data, columns=list(ehc_column))
        ehc_df["PATIENT_TYPE"] = "EHC"
        ehc_df["NET_AMOUNT"] = 400
        ehc_df["DOCTOR_SHARE"] = 400
        ehc_df["GROSS_AMOUNT"] = 400
        ehc_df["SOURCE OF DATA"] = "EHC Query"
        ehc_df["REFERENCE_GROUP"] = "OP Consultation"

        ehc_df = pd.merge(
            ehc_df,
            doctors_list_df[["DOCTOR_NAME", "DOCTORS_GROUP"]],
            on="DOCTOR_NAME",
            how="left",
        )

        dataframe = self.concat_dataframes(dataframe, ehc_df)
        try:
            del ehc_df
        except Exception:
            pass
        return dataframe

    def rh_working(self, rh_dataframe, main_dataframe):
        # make a set of main dataframe sevice code to intersect with rh dataframe
        main_serv = set(main_dataframe["SERVICE_CODE"])

        for i in range(len(rh_dataframe)):
            # Define row
            row = rh_dataframe.iloc[[i]]
            # Define current row's service code  to set for intercestion
            rh_serv = set(row["SERVICE_CODE"])

            # Changing Doctor's Share In RH Dataframe from 80% to 100%
            if rh_dataframe.at[i, "DOCTOR_SHARE"] > 0:
                rh_dataframe.at[i, "DOCTOR_SHARE"] = (
                    rh_dataframe.at[i, "DOCTOR_SHARE"] * 100 / 80
                )

            # Keep all the vaild values
            if rh_serv.intersection(main_serv):
                pass
            elif "grade" in row["SERVICE_DESC"].values.astype(str)[0].lower():
                pass
            # else any other service to be 0 includeing 2D Echo and Dressing
            else:
                rh_dataframe.at[i, "DOCTOR_SHARE"] = 0

        return rh_dataframe

    def rev_coloumn_data(self, main_dataframe):
        main_dataframe["DOCTOR_SHARE"] = pd.to_numeric(
            main_dataframe["DOCTOR_SHARE"], errors="coerce"
        )
        main_dataframe.loc[
            main_dataframe["DOCTOR_SHARE"].values.astype(int) > 1, "REV_STREAM"
        ] = 1
        main_dataframe.loc[main_dataframe["DOCTOR_SHARE"] < 1, "REV_STREAM"] = -1
        main_dataframe.loc[main_dataframe["DOCTOR_SHARE"].isnull(), "REV_STREAM"] = 1
        return main_dataframe

    # Prototype not in use
    def cosmetic_service_deductions(self, dataframe):
        tax_df = ""
        all_entery_of_episode = ""
        # Defining unique episode id uising set
        episode_id = set(dataframe["EPISODE_ID"].values.astype(str))

        for episode in episode_id:
            # Defining UHID to search later
            uhid = dataframe.loc[dataframe["EPISODE_ID"] == int(episode)][
                "PATIENT_ID"
            ].values.astype(str)[0]
            # Running Query
            sql_qurey = Query.objects.get(query_name="Service Check on Cosmetic").query
            sql_qurey = sql_qurey.format(variable=f"'{uhid}'", variable1=f"'{episode}'")
            db = Ora()
            tax_data, column_name = db.run_query(sql_qurey)
            # tax_data, column_name = db.service_check_on_cosmetic(uhid, episode)
            # Data comes from the query means this paticular service is charegeable
            if tax_data:
                # Creating new Dataframe to extract all billing service code
                tax_df = pd.DataFrame(data=tax_data, columns=list(column_name))
                # Get All the serviec where GST is Charged at 18% Percent
                service_id = list(set(tax_df["BLNG_SERV_CODE"]))
                # filter the above service from data frame to iterate
                all_entery_of_episode = dataframe[
                    (dataframe["PATIENT_ID"] == uhid)
                    & (dataframe["EPISODE_ID"] == int(episode))
                    & dataframe["SERVICE_CODE"].isin(service_id)
                ]
                # Creating a list of Index values to Iterate
                index = list(all_entery_of_episode.index)
                for i in index:
                    # Definind Dr share for calucalations
                    dr_share = dataframe.iloc[i]["DOCTOR_SHARE"]
                    # Dataframe.loc or iloc will create a slice so remeber to always use .at method to change
                    # the value in dataframe
                    dataframe.at[i, "DOCTOR_SHARE"] = float(dr_share) / 1.18
                    dataframe.at[i, "COMMENTS"] = f"Changed from {dr_share}"

        # Garbage Collection
        try:
            del tax_df
        except Exception:
            pass
        try:
            del all_entery_of_episode
        except Exception:
            pass

        return dataframe

    # Prototype not in use
    def plastic_surgeons_working_gst(self, dataframe):
        sql_qurey = Query.objects.get(query_name="List of Plastic Surgeons").query
        db = Ora()
        plastic_dr, column_name = db.run_query(sql_qurey)
        # plastic_dr, column_name = db.get_plastic_surgeons()
        plastic_df = pd.DataFrame(data=plastic_dr, columns=list(column_name))
        plastic_dr_filter = dataframe[
            dataframe["DOCTOR_NAME"].isin(list(plastic_df["PRACTITIONER_NAME"]))
        ]
        return plastic_dr_filter

    def plastic_cosmetic_gst(self, dataframe):
        sql_qurey = Query.objects.get(query_name="GST on Cosmetic and Plastic").query
        db = Ora()
        dr_list, _ = db.run_query(sql_qurey)
        # dr_list, _ = db.gst_on_cosmetic_and_plastic()
        episode_id = np.array(
            list(
                map(
                    str,
                    dataframe[dataframe["DOCTOR_NAME"].isin(dr[0] for dr in dr_list)][
                        "EPISODE_ID"
                    ].unique(),
                )
            )
        ).astype(int)

        df_filtered = dataframe[dataframe["EPISODE_ID"].isin(episode_id)]

        sql_qurey = Query.objects.get(query_name="Service Check on Cosmetic").query
        db = Ora()
        tax_data = np.array(
            np.unique(
                [
                    data_tuple[1]
                    for data, _ in [
                        db.run_query_without_self_close_db(
                            sql_qurey.format(
                                variable=f"'{patient_id}'", variable1=f"'{episode_id}'"
                            )
                        )
                        for patient_id, episode_id in zip(
                            df_filtered["PATIENT_ID"].tolist(),
                            df_filtered["EPISODE_ID"].tolist(),
                        )
                    ]
                    if data
                    for data_tuple in data
                ]
            )
        )
        db.close_connection()
        all_entery_of_episode = np.unique(
            dataframe[dataframe["SERVICE_CODE"].isin(tax_data)]["EPISODE_ID"].to_numpy()
        )
        dataframe.loc[
            dataframe["EPISODE_ID"].isin(all_entery_of_episode), "COMMENTS"
        ] = (
            dataframe.loc[
                dataframe["EPISODE_ID"].isin(all_entery_of_episode), "COMMENTS"
            ].fillna("")
            + " Changed from "
            + dataframe.loc[
                dataframe["EPISODE_ID"].isin(all_entery_of_episode), "DOCTOR_SHARE"
            ].astype(str)
        )
        dataframe.loc[
            dataframe["EPISODE_ID"].isin(all_entery_of_episode), "DOCTOR_SHARE"
        ] = np.divide(
            dataframe.loc[
                dataframe["EPISODE_ID"].isin(all_entery_of_episode), "DOCTOR_SHARE"
            ],
            1.18,
        )

        return dataframe

    def negative_to_postive_entry_check(self, dataframe):
        negative_share_rows = dataframe[dataframe["DOCTOR_SHARE"] < 0]

        for _, row in negative_share_rows.iterrows():
            doctor_share = abs(row["DOCTOR_SHARE"])
            doctor_name = row["DOCTOR_NAME"]
            episode_id = row["EPISODE_ID"]
            comments = (
                str(dataframe.loc[row.name, "COMMENTS"]) + "   ---   "
                if str(dataframe.loc[row.name, "COMMENTS"]) != "nan"
                else ""
            )  # Convert float to string

            matching_rows = dataframe[
                (dataframe["DOCTOR_SHARE"] == doctor_share)
                & (dataframe["DOCTOR_NAME"] == doctor_name)
                & (dataframe["EPISODE_ID"] == episode_id)
            ]
            if not matching_rows.empty:
                dataframe.loc[row.name, "COMMENTS"] = comments + " Positive Entry Found"
            else:
                dataframe.loc[row.name, "COMMENTS"] = (
                    comments + " No!!! Positive Entry Found. Manual Check is Required"
                )

        return dataframe

    def elapsed_time(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            print(f"Elapsed time: {end_time - start_time:.2f} seconds")
            return result

        return wrapper

    def get_container_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def upload_file_to_ftp(
        self,
        file_path,
        ftp_server="172.20.200.135",
        ftp_username="ftpuser",
        ftp_password="kh@12345",
        ftp_folder="d_excel",
        ftp_port=21,
    ):
        ftp = FTP()
        ftp.connect(ftp_server, ftp_port)
        ftp.login(ftp_username, ftp_password)
        ftp.cwd(ftp_folder)
        file_name = file_path.split("/")[-1]
        with open(file_path, "rb") as file:
            ftp.storbinary(f"STOR {file_name}", file)
        ftp.quit()

    def send_email_user(
        self,
        excel_file_path,
        user_email,
        from_date,
        to_date,
        msg="File Access",
        subject=None,
    ):
        email_config = {
            "send_from": "Ahmed Qureshi <ahmed.qureshi@kokilabenhospitals.com>",
            "send_to": user_email,
            "send_to_cc": "ahmed.qureshi@kokilabenhospitals.com",
            "subject": f"Automated Email -- Doctors KD Report --- From : {from_date} - To : {to_date}",
            "text": f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>File Access</title>
                </head>
                <body style="font-family: Arial, sans-serif;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 5px;">
                        <h1>{msg}</h1>
                        <p>This file, along with all the previous files, is accessible by pasting the following link into the URL field of the File Explorer:</p>
                        <p style="word-break: break-all; margin-bottom: 10px;">ftp://172.20.200.135/d_excel/</p>
                        <p>and entering the following credentials:</p>
                        <div style="margin-top: 20px;">
                            <p><strong>ID/username:</strong> ftpuser</p>
                            <p><strong>Password:</strong> kh@12345</p>
                        </div>
                    </div>
                </body>
                </html>
            """,
            "server": "172.20.200.29",
            "port": 25,
        }

        if subject:
            email_config["subject"] = subject

        if excel_file_path:
            # Get the size of the file in bytes
            file_size_mb = os.path.getsize(excel_file_path) / (1024 * 1024)

            # FTP and email configuration
            ftp_config = {
                "ftp_server": "172.20.200.135",
                "ftp_username": "ftpuser",
                "ftp_password": "kh@12345",
                "ftp_folder": "d_excel",
                "ftp_port": 21,
            }
            # Upload file to FTP
            self.upload_file_to_ftp(excel_file_path, **ftp_config)

            # Check if the file size is greater than 25 MB and send email accordingly
            if file_size_mb >= 25:
                Email_Sender(**email_config)
            else:
                email_config["attachment"] = excel_file_path
                Email_Sender(**email_config)
        else:
            Email_Sender(**email_config)

    def get_ip_kh_data(self, from_date, to_date):
        sql_qurey = Query.objects.get(query_name="Doctors Payout IP KH").query
        sql_qurey = sql_qurey.format(from_date=f"'{from_date}'", to_date=f"'{to_date}'")
        db = Ora()
        data, column = db.run_query_with_none_value(sql_qurey)
        df_dp_ip_kh = pd.DataFrame(data=data, columns=list(column))
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # df_dp_ip_kh = pd.read_excel(f"{current_dir}/resources/ip_payout.xlsx")
        return df_dp_ip_kh

    def get_op_kh_data(self, from_date, to_date):
        sql_qurey = Query.objects.get(query_name="Doctors Payout OP KH").query
        sql_qurey = sql_qurey.format(from_date=f"'{from_date}'", to_date=f"'{to_date}'")
        db = Ora()
        data, column = db.run_query_with_none_value(sql_qurey)
        df_dp_op_kh = pd.DataFrame(data=data, columns=list(column))
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # df_dp_op_kh = pd.read_excel(f"{current_dir}/resources/op_payout.xlsx")
        return df_dp_op_kh


def post_files_to_uploaded_folder(file_name, file):
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "uploaded_files", file_name
    )
    if os.path.exists(data_path):
        os.remove(data_path)
    # Save rh_data in ../uploaded_files directory and replace if already exists
    with open(data_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return data_path
