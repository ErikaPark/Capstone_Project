import pandas as pd 
import numpy as np 



# Mapping
def mapping_code_id(mapping_code):
    global accountDB
    if mapping_code in list(accountDB.Company_Mapping_Code):
        idx = list(accountDB.Company_Mapping_Code).index(mapping_code)
        return accountDB['CompanyID'][idx]
    else:
        return None

def use_email(email, email_list):
    if email in email_list:
        idx = email_list.index(email)
        companyid = accountDB['CompanyID'][idx]
        return companyid 
    else:
        return None
    
def manipulate_string(string): # 문자열에서 띄워쓰기 없애고 소문자로 바꾸는 함수 
    string = str(string)
    res = string.strip()
    return res.lower()

def get_companyID(Email): # 이메일 사용
    if Email == 'hanafn.com':
        companyId = 1150 #하나금융지주 
    elif Email == 'kolon.com':
        companyId = 1390 #코오롱 
    elif Email == 'shinhan.com':
        companyId = 1641 # 신한금융지주 
    else:
        companyId = None 
    return companyId

def get_companyID2():
    company = ['(주)두산','두산'] + ['롯데쇼핑(주)롯데마트롭스사업본부','롯데쇼핑(주)마트사업본부'] \
    + ['현대자동차 미국법인 (재경팀)','씨티은행','삼성', 'Samsung','Hansem, Inc.', '한샘이펙스','Skt',
       '부산시','농협생명보험', '농협손해보험','효성티앤에스','한국산업기술평가관리원','귀뚜라미',
       '육군협회','삼성산업','Konkuk University','동덕여자대학교 학생생활연구소', '동덕여자대학교학생생활연구소',
       '서울과기대','한국전력기술','한국가스기술공사','정보통신','제주특별자치도','고려대',
       '다임','대상그룹','티앤씨','동진','한국조선해양','단국대학교의과대학','한국컴퓨터(주)', 
    '우리금융지주','동원무역','제주대하쿄','KT/융합ICT1TF','국가정보자원관리원','INITECH', '이니텍(주)']

    companyid = [1061]*2 + [1483]*2 + [1537,3380] + [1613]*2 + [1173]*2 + [1683,2651]+[2022]*2 \
    +[1243,1809,2395,3080,2695,1397]+[1053]*2 + [1802,1342,1388,3393,3154,1765,1793 ,1020,1246,
                                                  2528,3395,1026,1998,3022,1059,1299,1428,1948]+[3088]*2
    category = pd.DataFrame({'Company':company,'CompanyID':companyid})
    return category

def get_companyID3(Company): # SK 그룹
    if pd.isna(Company):
        return 1664 #sk그룹 
    elif Company in ['SK 그룹, 에스케이 그룹',  'FSK L&S',  'SKTELINK', 'Sk 넥실리스', 'Sk 바이오사이언스', 'SK하이닉스', 'SKT']:
        return 1664 #sk그룹
    elif ('CC' in str(Company)) or ('C&C' in str(Company)) or ('cloud / SK C&C'in str(Company)):
        return 1665 # SK C&C
    elif '십일번가주식회사' in str(Company):
        return 1663 #11번가
    elif  Company =='SKshieldus':
        return 1792
    elif Company in ['SK Networks Service', 'SKNS']:
        return 1668 # SK네트웍스서비스
    elif Company in ['ES', 'SK ES']:
        return 1666 # SK E&S
    elif Company == 'SK On':
        return 1673 # sk이노베이션
    else:
        return 1664


def get_isfam(Company):# 계열사여부 
    LGgroup = ['lg', '엘지']
    if pd.notna(Company):
        Company = str(Company).lower()
        for i in LGgroup:
            if i in Company:
                return 1
            else:
                return 0
    else:
        return 0