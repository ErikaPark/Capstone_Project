#Current Directory: ./code2/preprocess/Process.py

from Process1 import *
from Process2 import *
from Get_Category import *

import pandas as pd
import numpy as np


class Preprocess1:
    def __init__(self):
        super().__init__()
        self.rawdata_path =  '../../data/raw_data/'
        self.save1data_path = '../../data/processed1/'
        self.save2data_path = '../../data/processed2/'
        self.label_path = './labelling_category/'
    
    def create_contactDB(self):
        allcontacts = pd.read_excel(self.rawdata_path+ 'All_contacts_download_2022-07-06.xlsx')
        accountDB = pd.read_excel(self.rawdata_path + 'Account_2022-07-06.xlsx')

        contactDB = Create_Contact.delete_testID(allcontacts)
        contact = Create_Contact.Map_Contact_Account(contactDB, accountDB)
        contact = Create_Contact.unify_title_columns(contact)
        ContactDB = contact.copy()
        contact = Create_Contact.unify_industry_columns(contact, ContactDB)
        contact = Create_Contact.isfam(contact)
        contact = Create_Contact.first_action(contact, self.save1data_path)
        
        contact.Title = contact.Title.apply(Grouping.group_title)
        contact.Industry = contact.Industry.apply(Grouping.group_industry)
        contact['고객등급'].replace({'Grape':8, 'Pineapple':7, 'Pear':6, 'Mango':4, 'Strawberry':3, 'Banana':2,'Apple':1, 'Lemon':5}, inplace = True)
        use_col = ['ContactID','CompanyID', 'Title', 'Industry','isfam','first_action', 'Mapping', '고객등급']
        contactDB = contact[use_col]
        return contactDB


    def json_to_csv():pass

    def create_activity_merged():pass

    def create_email_sent():pass


class Preprocess2(Preprocess1):
    def __init__(self):
        super().__init__()
        self.contactDB = pd.read_csv(self.save1data_path + 'ContactDB.csv')
        self.activity_merged = pd.read_csv(self.save1data_path + 'activity_merged.csv')
        self.EmailSent = pd.read_csv(self.save1data_path + 'EmailSent.csv')

    
