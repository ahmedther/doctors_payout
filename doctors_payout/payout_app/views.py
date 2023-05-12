from ast import main
import pandas as pd
import os

from django.shortcuts import render

from .oracle_config import Ora
from .postgress_config import PostgressDB
from .models import DoctorProfile
from .excel_maker import Support


def index(request):
    sup = Support()
    postDB = PostgressDB()
    if request.method == "GET":
        current_dir = os.path.dirname(os.path.abspath(__file__))
##################################################################################################################
#Step 1
##################################################################################################################

        # Step 1 : Sub-Section 1 making the main DataFrame
        df_dp_ip_kh = pd.read_excel(f"{current_dir}\\resources\ip_payout.xlsx")
        # Step 1 : Sub-Section 2
        df_dp_ip_kh = sup.add_new_column(
            df_dp_ip_kh, "SOURCE OF DATA", "IP Admitting Doc wise rev rep"
        )
        # sup.excel_generator(excel_data=df_dp_ip_kh, page_name="test")

        df_dp_op_kh = pd.read_excel(f"{current_dir}\\resources\op_payout.xlsx")
        # Step 1 : Sub-Section 2
        df_dp_op_kh = sup.add_new_column(
            df_dp_op_kh, "SOURCE OF DATA", "Op Rev share for Ext Doc Rep"
        )

        # #Step 1 : Sub-Section 3 Combine Dataframe
        main_dataframe = sup.concat_dataframes(df_dp_ip_kh, df_dp_op_kh)

        # Delete Unused Data Frame
        df_dp_ip_kh = sup.delete_dataframe(df_dp_ip_kh)
        df_dp_op_kh = sup.delete_dataframe(df_dp_op_kh)

        # #Step 1 : Sub-Section 4  Get Doctor list form Postgres Database
        doctors_list_data, doctors_list_column = postDB.applicable_doctors()

        # Generate Dataframe of Doctor's List
        doctors_list_df = pd.DataFrame(
            data=doctors_list_data, columns=list(doctors_list_column)
        )

        # Keep only Doctor in Doctors list delete the rest name wise
        main_dataframe = sup.filter_aplicable_doctor(
            main_dataframe=main_dataframe,
            main_dataframe_column="DOCTOR_NAME",
            doctors_list_df=doctors_list_df,
            doctors_list_df_column="doctors_name",
        )

        # #Step 1 : Sub-Section 5 RH Dataframe
        df_dp_rh = pd.read_excel(f"{current_dir}\\viren_ref\RH_Data.xlsx")
        df_dp_rh = sup.add_new_column(
            df_dp_rh, "SOURCE OF DATA", "RH DATA IP Admitting Doc wise rev rep"
        )

        # RH Dataframe column rename to match with main_dataframe
        df_dp_rh = sup.rename_columns(
            df_dp_rh,
            {
                "BILLING_CLASS": "PATIENT_TYPE",
                "GROSS_AMT": "GROSS_AMOUNT",
                "NET_AMT": "NET_AMOUNT",
            },
        )

        # Delete Extra Column
        df_dp_rh = sup.delete_columns(df_dp_rh, ["SERVICE_GROUP"])
##################################################################################################################
#Step 6
##################################################################################################################

        #RH DataFrame Working
        df_dp_rh = sup.rh_working(df_dp_rh,main_dataframe)
##################################################################################################################
#End Step 6
##################################################################################################################

        # Concatanate MainDataframe and RH Dataframe
        main_dataframe = sup.concat_dataframes(main_dataframe, df_dp_rh)

        # Delete unused dataframe
        df_dp_rh = sup.delete_dataframe(df_dp_rh)

        # Add Doctor Group Column from Doctor List and Delete Doctor List Column
        # Rename to Match Main Dataframe
        doctors_list_df = sup.rename_columns(
            doctors_list_df,
            {"doctors_name": "DOCTOR_NAME", "doctors_group": "DOCTORS_GROUP"},
        )
        # Extract Two Column Will be deleted in EHC
        doctors_list_df = doctors_list_df[["DOCTOR_NAME", "DOCTORS_GROUP"]]

        # Add Doctors Group in Main Dataframe
        main_dataframe = pd.merge(
            main_dataframe,
            doctors_list_df[["DOCTOR_NAME", "DOCTORS_GROUP"]],
            on="DOCTOR_NAME",
            how="left",
        )

        # Step 1 : Sub-Section 7 add_new_column ref group column
        # Step 1 : Sub-Section 7 check and insert valuce as per CINP
        main_dataframe["REFERENCE_GROUP"] = main_dataframe.apply(
            lambda row: sup.CINP_OR_CNOP_ANE(row["SERVICE_CODE"]), axis=1
        )

        # End of Step 1
        ######################################################################################


        # Step 2 Transplant Split
        transplant_dataframe = pd.read_excel(
            f"{current_dir}\\viren_ref\\transplant.xlsx"
        )
        transplant_dataframe = transplant_dataframe.dropna()
        transp_df_uhid = list(transplant_dataframe["UHID"]) + list(
            transplant_dataframe["UHID.1"]
        )
        # main_dataframe["DOCTOR_SHARE"] = main_dataframe.apply(
        #     lambda row: sup.transplant_working(main_dataframe, row), axis=1
        # )

        # Calculations for HPB Transplant
        postDB = PostgressDB()
        transplant_doctor_data, column_name = postDB.transplant_doctors(
            "HPB and Liver Transplant"
        )
        transp_df = pd.DataFrame(
            data=transplant_doctor_data,
            columns=list(column_name),
        )

        main_dataframe = sup.transplant_working(
            main_dataframe, transp_df, transp_df_uhid
        )

        # Calculations for Liver
        postDB = PostgressDB()
        transplant_doctor_data, column_name = postDB.transplant_doctors("UROLOGY")
        # sup.excel_generator(excel_data=main_dataframe, page_name="test")
        transp_df = pd.DataFrame(
            data=transplant_doctor_data,
            columns=list(column_name),
        )

        main_dataframe = sup.transplant_working(
            main_dataframe, transp_df, transp_df_uhid
        )

        # Calculations for Cardiac
        postDB = PostgressDB()
        transplant_doctor_data, column_name = postDB.transplant_doctors("CARDIOLOGY")
        # sup.excel_generator(excel_data=main_dataframe, page_name="test")
        transp_df = pd.DataFrame(
            data=transplant_doctor_data,
            columns=list(column_name),
        )

        main_dataframe = sup.transplant_working(
            main_dataframe, transp_df, transp_df_uhid
        )
        transp_df = sup.delete_dataframe(transp_df)
        transplant_dataframe = sup.delete_dataframe(transplant_dataframe)

##################################################################################################################
#Step 3
##################################################################################################################
        # SRS EDGE Share distribution
        main_dataframe = sup.srs_distribution(main_dataframe)

##################################################################################################################
#Step 4
##################################################################################################################

        # Check Paediatrican Fe Doctor and replace with peads dr if dr is not a paediatrician
        main_dataframe = sup.check_peadiatric(main_dataframe)
##################################################################################################################
#Step 5
##################################################################################################################

        # EHC Working
        main_dataframe = sup.ehc_patient_working(main_dataframe, doctors_list_df)
        # Delete Unused Dataframe Doctors List
        doctors_list_df = sup.delete_dataframe(doctors_list_df)

##################################################################################################################
# Step 7 (Step 6 is up in Step 1)
##################################################################################################################

        # Column REV_STREAM 
        main_dataframe = sup.rev_coloumn_data(main_dataframe)

##################################################################################################################
# Step 8
##################################################################################################################

        main_dataframe = sup.plastic_cosmetic_gst(main_dataframe)

##################################################################################################################
# Step 9 covered in step 8
##################################################################################################################
        
##################################################################################################################
# Step 10 
##################################################################################################################

        
        



        sup.excel_generator(excel_data=main_dataframe, page_name="main_dataframe")
        return render(request, "payout_app/index.html")
