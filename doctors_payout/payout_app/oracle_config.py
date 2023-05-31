from contextlib import nullcontext
import cx_Oracle as oracle

# from oracle_config import *


# ora_db = oracle.connect("appluser","appluser",dsn_tns)

# cursor = ora_db.cursor()


# host = 'khdb-scan'

# port = 1521

# service_name = "newdb.kdahit.com"

# instance_name = "NEWDB"

# dsn_tns = oracle.makedsn(ip,port,instance_name)

# ora_db = oracle.connect("ibaehis","ib123",dsn_tns)

# cursor = ora_db.cursor()


#   'oracle': {
#     'ENGINE': 'django.db.backends.oracle',
#     'NAME': 'NEWDB:1521/newdb.kdahit.com',
#     'NAME': ('(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=khdb-scan)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=newdb.kdahit.com)))'),
#     'USER': 'ibaehis',
#     'PASSWORD': 'ib123',


class Ora:
    def __init__(self):
        ip = "172.20.200.16"

        host = "khdb-scan.kdahit.com"

        port = 1521

        service_name = "newdb.kdahit.com"

        instance_name = "NEWDB"
        username = "ibaehis"
        password = "ib123"
        self.dsn_tns = oracle.makedsn(host, port, service_name=service_name)
        self.ora_db = oracle.connect(username, password, self.dsn_tns)
        self.cursor = self.ora_db.cursor()
        self.pool = oracle.SessionPool(
            username,
            password,
            self.dsn_tns,
            min=3,
            max=5,
            increment=1,
            getmode=0,
        )

    def status_update(self):
        if self.ora_db:
            return "You have connected to the Database"

        else:
            return "Unable to connect to the database! Please contact the IT Department"

    # def __del__(self):
    # self.cursor.close()
    # self.ora_db.close()

    def doctor_payout_IP_KH(self, from_date, to_date):
        sql_qurey = f""" 
        

            SELECT   a.service_date,a.patient_id, a.episode_id,
            b.patient_name, a.service_code,a.service_desc, 
            blcommonproc.get_blng_class_code_desc (a.blng_class_code, 'en') PATIENT_TYPE,
            a.gross_amount, a.net_amt net_amount, 
            SUM (a.doctor_share) Doctor_share,
            blcommonproc.get_practitioner_name (a.physician_id, 'en' ) doctor_name,
            a.physician_id physician_id  --V191016
            FROM 
            (SELECT   TO_CHAR (a.service_date, 'DD/MM/RRRR') service_date, 
            a.patient_id, a.episode_id, a.episode_type,a.operating_facility_id,
            DECODE (d.rate_entry_by_user_flag,
            'R', d.short_desc,
            NVL (a.serv_item_desc, d.short_desc)
            ) service_desc,
            DECODE (d.rate_entry_by_user_flag,
            'R', a.blng_serv_code,
            NVL (a.serv_item_code, a.blng_serv_code)
            ) service_code,
            a.physician_id, a.blng_serv_code,
            d.serv_classification_code, d.serv_grp_code,
            a.blng_class_code,
            SUM (NVL (a.org_net_charge_amt, 0)) net_amt,
            SUM (NVL (a.org_gross_charge_amt, 0))
            gross_amount,
            SUM
            (  a.org_net_charge_amt
            * NVL
            (bl_get_dr_fee_percentage
            (a.operating_facility_id,
            a.physician_id,
            a.episode_type,
            a.blng_serv_code,
            d.serv_grp_code,
            d.serv_classification_code
            ),
            0
            )
            / 100
            ) doctor_share
            FROM bl_patient_charges_folio a, bl_blng_serv d
            WHERE a.blng_serv_code = d.blng_serv_code
            AND a.trx_status IS NULL
            AND a.operating_facility_id = 'KH'
            AND a.service_date between {from_date} and TO_DATE({to_date}) + 1
            AND a.episode_type IN ('I', 'D')
            AND a.physician_id =
            DECODE (NVL (:p_frm_doctor_id, '**'),
            '**', a.physician_id,
            :p_frm_doctor_id
            )
            GROUP BY a.operating_facility_id,
            a.patient_id,
            a.episode_id,
            a.episode_type,
            a.service_date,
            d.short_desc,
            d.rate_entry_by_user_flag,
            a.physician_id,
            a.serv_item_code,
            a.serv_item_desc,
            a.blng_serv_code,
            d.serv_classification_code,
            d.serv_grp_code,
            a.blng_class_code
            HAVING SUM (NVL (a.org_gross_charge_amt, 0)) <> 0) a,
            mp_patient b
            WHERE a.patient_id = b.patient_id
            GROUP BY operating_facility_id,
            a.patient_id,
            a.episode_id,
            patient_name,
            service_date,
            a.physician_id, ---V191016
            blcommonproc.get_blng_class_code_desc (a.blng_class_code,
            'en'
            ),
            a.service_code,
            a.net_amt,
            a.gross_amount,
            a.service_desc,
            blcommonproc.get_practitioner_name (a.physician_id,
            'en'
            )
            HAVING SUM (a.doctor_share) <> 0
            ORDER BY blcommonproc.get_practitioner_name (a.physician_id,
            'en'
            ) ASC

        """
        # p_language_id total 5 first at 72, p_facility_id at 111, :p_fm_bill_date at 113, p_to_bill_date at 115
        # p_frm_doctor_id at 172
        p_frm_doctor_id = None

        with self.pool.acquire() as connection:
            cursor = connection.cursor()
            for result in cursor.execute(
                sql_qurey, [from_date, to_date, p_frm_doctor_id]
            ):
                result = cursor.fetchall()

            # self.cursor.execute(sql_qurey, [from_date, to_date, p_frm_doctor_id])
            # data = self.cursor.fetchall()

            column_name = [i[0] for i in cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return result, column_name

    def doctor_payout_OP_KH(self, from_date, to_date):
        sql_qurey = f""" 
        

        select a.service_date, a.patient_id, a.episode_id, 
        b.patient_name, a.blng_srv_code Service_code, a.service_desc, 
        blcommonproc.get_blng_class_code_desc(a.blng_class_code,'en') PATIENT_TYPE,
        sum(a.Gross_amt) gross_amount, sum(a.Net_amt) net_amount, sum(a.Doctor_share) Doctor_share,
        blcommonproc.get_practitioner_name (a.physician_id,'en') doctor_name,
        a.physician_id physician_id
        from    
        (
        SELECT   a.operating_facility_id,a.patient_id,a.episode_id, a.episode_type,
        TO_CHAR (a.service_date, 'DD/MM/RRRR') Service_date,
        decode(d.RATE_ENTRY_BY_USER_FLAG,'R',d.long_desc,nvl(a.serv_item_desc,d.long_desc)) service_desc,
        decode(d.RATE_ENTRY_BY_USER_FLAG,'R',a.blng_serv_code,NVL (a.serv_item_code, a.blng_serv_code)) blng_srv_code,
        a.physician_id,a.blng_serv_code, d.serv_classification_code, 
        d.serv_grp_code,a.blng_class_code,
        SUM (NVL (a.org_gross_charge_amt, 0)) Gross_amt,
        SUM(NVL(a.org_net_charge_amt,0)) Net_amt,
        SUM(a.org_net_charge_amt * nvl(bl_get_dr_fee_percentage(a.operating_facility_id, a.physician_id, a.episode_type, a.blng_serv_code, d.serv_grp_code, d.serv_classification_code),0)/100) DOCTOR_SHARE
        FROM bl_patient_charges_folio a,
        bl_blng_serv d
        WHERE a.blng_serv_code = d.blng_serv_code
        AND a.trx_status IS NULL
        AND a.bill_doc_num is not null
        AND (('A' !='A' and a.episode_type = 'A')
        or ('A' ='A' and a.episode_type =a.episode_type)) 
        AND a.operating_facility_id = 'KH'
        AND a.bill_doc_date between {from_date} and TO_DATE({to_date}) + 1
        AND a.episode_type IN ('O', 'E', 'R')
        AND a.physician_id =
        DECODE (NVL (:p_frm_doctor_id, '**'),
        '**', a.physician_id,
        :p_frm_doctor_id
        )
        AND d.comm_doctor_service_yn = 'Y'
        GROUP BY a.operating_facility_id,
        a.physician_id,
        a.patient_id,
        a.episode_id,
        a.episode_type,
        a.service_date,
        d.long_desc,d.RATE_ENTRY_BY_USER_FLAG,
        a.physician_id,a.serv_item_code,a.serv_item_desc,
        a.blng_serv_code, a.blng_class_code,d.serv_classification_code, d.serv_grp_code
        HAVING SUM (NVL (a.org_gross_charge_amt, 0)) <> 0
        ) a, mp_patient b
        where a.patient_id=b.patient_id
        GROUP BY operating_facility_id,A.patient_id,
        a.physician_id,
        patient_name,
        episode_id,
        service_date,a.Gross_amt,a.Net_amt,
        blcommonproc.get_blng_class_code_desc(a.blng_class_code,'en'),
        a.service_desc,a.blng_srv_code,
        blcommonproc.get_practitioner_name
        (a.physician_id,
        'en'
        ) 
        HAVING  sum(a.doctor_share) <> 0
        ORDER BY  blcommonproc.get_practitioner_name
        (a.physician_id,
        'en'
        )  ASC

        """
        # p_language_id total 5 first at 72, p_facility_id at 111, :p_fm_bill_date at 113, p_to_bill_date at 115
        # p_frm_doctor_id at 172
        p_frm_doctor_id = None

        with self.pool.acquire() as connection:
            cursor = connection.cursor()
            for result in cursor.execute(
                sql_qurey, [from_date, to_date, p_frm_doctor_id]
            ):
                result = cursor.fetchall()

            # self.cursor.execute(sql_qurey, [from_date, to_date, p_frm_doctor_id])
            # data = self.cursor.fetchall()

            column_name = [i[0] for i in cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return result, column_name

    def check_dr_pead(self, pr_number):
        sql_qurey = f""" 
        
        select PRACTITIONER_NAME,LONG_DESC
        from AM_PRACTITIONER,AM_SPECIALITY
        where PRIMARY_SPECIALITY_CODE =  speciality_code
        and LONG_DESC in ('PAEDIATRIC MEDICINE','PAEDIATRIC SURGERY')
        and PRACTITIONER_ID = :pr_number
        
        """
        # p_language_id total 5 first at 72, p_facility_id at 111, :p_fm_bill_date at 113, p_to_bill_date at 115
        # p_frm_doctor_id at 172

        with self.pool.acquire() as connection:
            cursor = connection.cursor()
            cursor.execute(sql_qurey, [pr_number])
            result = cursor.fetchall()

            # self.cursor.execute(sql_qurey, [from_date, to_date, p_frm_doctor_id])
            # data = self.cursor.fetchall()

            column_name = [i[0] for i in cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return result

    def ehc_dr_share(self, from_date, to_date):
        sql_qurey = f""" 
        
        select b.patient_id as PATIENT_ID,b.ADDED_DATE as SERVICE_DATE,B.LOCN_CODE as SERVICE_CODE,c.PRACTITIONER_NAME as DOCTOR_NAME,
        b.ENCOUNTER_ID as EPISODE_ID
        from op_patient_queue_dtls b , AM_PRACTITIONER c where b.PRACTITIONER_ID = c.PRACTITIONER_ID 
        AND B.ORDER_ID like'CNOP%'and B.ADDED_DATE between {from_date} and to_date({to_date}) + 1
        order by b.ADDED_DATE

        
        """
        # p_language_id total 5 first at 72, p_facility_id at 111, :p_fm_bill_date at 113, p_to_bill_date at 115
        # p_frm_doctor_id at 172

        with self.pool.acquire() as connection:
            cursor = connection.cursor()
            cursor.execute(sql_qurey, [from_date, to_date])
            result = cursor.fetchall()

            # self.cursor.execute(sql_qurey, [from_date, to_date, p_frm_doctor_id])
            # data = self.cursor.fetchall()

            column_name = [i[0] for i in cursor.description]

        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return result, column_name

    def gst_on_service_check(self, service_code):
        get_gst_on_service_check = f"""
        select a.LONG_DESC 
        from BL_ADDL_CHARGE_RULE a, BL_ADDL_CHARGE_RULE_BY_BS b
        where a.RULE_CODE = b.RULE_CODE
        and b.BLNG_SERV_CODE = :service_code

        """
        self.cursor.execute(get_gst_on_service_check, [service_code])
        data = self.cursor.fetchall()
        column_name = [i[0] for i in self.cursor.description]
        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data

    #        SELECT RULE_CODE,blng_serv_code
    #       FROM BL_ADDL_CHARGE_RULE_BY_CS
    #       WHERE BLNG_SERV_CODE IN (SELECT blng_Serv_code from bl_patient_charges_interface where patient_id= :uhid and episode_id= :service_code)

    def service_check_on_cosmetic(self, uhid, episode_id):
        get_service_check_on_cosmetic = f"""

        SELECT RULE_CODE,blng_serv_code
        FROM BL_ADDL_CHARGE_RULE_BY_CS
        WHERE BLNG_SERV_CODE IN (SELECT blng_Serv_code from bl_patient_charges_interface 
        where patient_id= :uhid 
        and episode_id= :episode_id)


        """
        self.cursor.execute(get_service_check_on_cosmetic, [uhid, episode_id])
        data = self.cursor.fetchall()
        column_name = [i[0] for i in self.cursor.description]

        return data, column_name

    def get_plastic_surgeons(
        self,
    ):
        plastic_surgeons_query = f"""

        select PRACTITIONER_NAME
        from AM_PRACTITIONER,AM_SPECIALITY
        where PRIMARY_SPECIALITY_CODE =  speciality_code
        and LONG_DESC = 'PLASTIC SURGERY'
        and APC_NO is not Null


        """
        self.cursor.execute(plastic_surgeons_query)
        data = self.cursor.fetchall()
        column_name = [i[0] for i in self.cursor.description]
        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def gst_on_cosmetic_and_plastic(self):
        plastic_surgeons_query = f"""

        select PRACTITIONER_NAME,LONG_DESC
        from AM_PRACTITIONER,AM_SPECIALITY
        where PRIMARY_SPECIALITY_CODE =  speciality_code
        and LONG_DESC in ('PLASTIC SURGERY','DERMATOLOGY','DENTAL SURGERY','AESTHETIC CLINIC')


        """
        self.cursor.execute(plastic_surgeons_query)
        data = self.cursor.fetchall()
        column_name = [i[0] for i in self.cursor.description]
        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()

        return data, column_name

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.ora_db:
            self.ora_db.close()




    def run_query(self, sql_qurey):
            
            with self.pool.acquire() as connection:
                cursor = connection.cursor()
                for result in cursor.execute(sql_qurey):
                    result = cursor.fetchall()
                column_name = [i[0] for i in cursor.description]

            if self.cursor:
                self.cursor.close()
            if self.ora_db:
                self.ora_db.close()

            return result, column_name
    
    def run_query_with_none_value(self, sql_qurey,none_value=None):
            try:
                print("Started")
                with self.pool.acquire() as connection:
                    cursor = connection.cursor()
                    for result in cursor.execute(sql_qurey,[none_value]):
                        result = cursor.fetchall()
                    column_name = [i[0] for i in cursor.description]
                print("Ended")

                if self.cursor:
                    self.cursor.close()
                if self.ora_db:
                    self.ora_db.close()

                return result, column_name
            except:
                print("Error")

if __name__ == "__main__":
    a = Ora()
    # b = a.get_online_consultation_report('01-Mar-2022','03-Apr-2022')
    b = a.get_package_contract_report("16-Jun-2018", "12-Jan-2022", "KH")

    print(b)

    for x in b:
        print(x)
