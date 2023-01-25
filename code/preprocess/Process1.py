from Get_Category import *
from Helper import *

import pandas as pd
import numpy as np


class Create_Contact:
    def __init__(self):
        super().__init__()
        self.rawdata_path =  '../../data/raw_data/'
        self.save1data_path = '../../data/processed1/'
        self.save2data_path = '../../data/processed2/'
        self.label_path = './labelling_category/'

    def delete_testID(self, contactDB):
        delete_contacts = pd.read_csv(self.label_path + 'test_contactId.txt', sep = ',', header = None)

        del_colnames = ['Date Created', 'Date Modified', 'Eloqua Contact ID', 'Title (KR)', 'Subscribe', 'Department', 'Subscribe Date', 'Interests (Others)',
        '개인정보 수집•이용 동의 (필수)', '개인정보 수집•이용 동의 (선택)', '(필수) 개인정보 수집•이용 동의 날짜', '(선택) 개인정보 수집•이용 동의 날짜', 'Unsubscribe Date', '회사홈페이지',
        'Subscribe Date_Display', 'Unsubscribe Date_Display', '(임시) NCD웨비나참여', '(홈페이지) BlogNews_Subscribe', '(홈페이지) Job Group', 'Interests (KR)',
        'KeyPerson Source', 'KeyPerson Source_History', '(임시) 보안웨비나참여', '(홈페이지) BlogNews_Subscribe Date','(홈페이지) BroDN_Pagename',
        '(홈페이지) BlogNews_Unsubscribe Date', '(홈페이지) BlogNews_Unsubscribe Date_Display', 'Unsubscribe Reason', 'Unsubscribe Reason (Others)',
        'Subscribe (Program)', 'Text Email only', 'withyou_webinarname', 'Contact_Management', 'withyou_eventname', 'Lead Source Code(변환용)']
        
        # CNS 에 소속된 고객 삭제 
        cns_name = ['LG CNS','LG_CNS', 'LGCNS', 'Lgcns', 'lgcns', 'cns', 'MS CLOUD 사업팀 | LG CNS', '솔루션영업팀 / lgcns']
        index_list = []
        for  i in range(len(cns_name)):
            cns = cns_name[i]
            idx = list(contactDB[contactDB.Company == cns].index)
            index_list += idx
        contactDB.drop(index_list, axis = 0, inplace = True)
   
        cns = contactDB[contactDB.Company_Mapping_Code == 'lgcnscom'].index
        contactDB.drop(cns, inplace = True)

        # test_contactId.txt 파일에 있는 ContactID 삭제 
        delete_contacts = pd.Series(list(delete_contacts.iloc[0,:])).dropna()
        delete_contacts = [x for x in delete_contacts if np.isnan(x) == False]# txt 파일 변환 과정에서 생긴 nan값 삭제
        contactID = list(contactDB.ContactID)
        mask = ~contactDB.ContactID.isin(delete_contacts)
        df = contactDB[mask]
        
        df.drop(labels = del_colnames, axis = 1, inplace=True)# 미사용 변수 삭제 
        return df.reset_index(drop=True)


    def Map_Contact_Account(contactDB, accountDB):
         # Mapping
        cannot_map, to_map = Mapping.mapping0(contactDB)
        mapped1 = Mapping.mapping1(to_map)
        to_map, mapped2 = Mapping.mapping2(to_map, accountDB)
        to_map, mapped3 = Mapping.mapping3(to_map, accountDB)
        to_map, mapped4 = Mapping.mapping4(to_map)
        to_map, mapped5 = Mapping.mapping5(to_map)
        cannot_map, not_mapped, to_map, mapped6 = Mapping.mapping6(to_map, cannot_map)

        mapped = pd.concat([mapped1, mapped2, mapped3, mapped4, mapped5, mapped6])
        mapped['Mapping'] = 1
        not_mapped['CompanyID'] = None
        not_mapped['Mapping'] = 0
        cannot_map['CompanyID'] = None
        cannot_map['Mapping'] = 0

        ContactDB2 = pd.concat([mapped, cannot_map, not_mapped]).drop_duplicates()
        
        Map_Account = accountDB.loc[:,['CompanyID', 'Company Name', '기업등급(5년평균)', '산업유형', '산업상세']]
        Map_Account.columns = ['CompanyID', 'Company', '고객등급', '산업유형', '산업상세']
        mapped_c = ContactDB2[ContactDB2.Mapping == 1].drop('Company', axis = 1)
        mapped_c = pd.merge(mapped_c, Map_Account, how = 'left', on ='CompanyID')

        notmapped_c = ContactDB2[ContactDB2.Mapping == 0]
        notmapped_c['고객등급'] = 'unknown'

        ContactDB = pd.concat([mapped_c, notmapped_c])
        return ContactDB

    def unify_title_columns(self, ContactDB):
        ContactDB['직급'] = pd.Series(list(map(Title.get_title1, list(ContactDB['직급']))))
        ContactDB['Title (Others)'] = pd.Series(list(map(Title.get_title2, list(ContactDB['Title (Others)']))))
        for i in range(len(ContactDB)):
            if ContactDB.Title.isna().iloc[i] == True:
                ContactDB.Title.iloc[i] = ContactDB['직급'].iloc[i]
            elif ContactDB.Title.iloc[i] == 'Others':
                ContactDB.Title.iloc[i] = ContactDB['Title (Others)'].iloc[i]
        ContactDB.Title.fillna('Unknown', inplace = True)
        return ContactDB

def unify_industry_columns(self, contact, ContactDB):
    contact.loc[:, 'Industry'] = contact.loc[:, '산업유형']
    contact.loc[contact['산업유형'] == '금융;비영리', 'Industry'] = '금융'
    contact.loc[contact['산업유형'] == '기업집단;유통', 'Industry'] = '기업집단'
    contact.loc[contact['산업유형'] == '통신', 'Industry'] = '방송통신'
    contact.loc[contact['산업유형'] == '서비스;비영리', 'Industry'] = '비영리'
    contact.loc[contact['산업유형'] == '비영리', 'Industry'] = '비영리'

    for i in range(len(contact)):
        if contact.Industry.iloc[i] == '서비스':
            if 'IT' in contact.산업상세.iloc[i]:
                contact.Industry.iloc[i] = 'IT서비스'
            else :
                contact.Industry.iloc[i] = '일반서비스'
    for i in range(len(contact)):
        if contact.Industry.isna().iloc[i] == True:
            contact.Industry.iloc[i] = ContactDB.Industry.iloc[i]

    contact.loc[contact['Industry'] == 'Telecommunications & Media', 'Industry'] = '방송통신'
    contact.loc[contact['Industry'] == 'Manufacturing', 'Industry'] = '제조'
    contact.loc[contact['Industry'] == 'Government & Public', 'Industry'] = '공공'
    contact.loc[contact['Industry'] == 'Govermment & Public', 'Industry'] = '공공'
    contact.loc[contact['Industry'] == 'Financial Services', 'Industry'] = '금융'
    contact.loc[contact['Industry'] == 'Logistics', 'Industry'] = '물류'
    contact.loc[contact['Industry'] == 'IT Service', 'Industry'] = 'IT서비스'
    contact.loc[contact['Industry'] == 'Education', 'Industry'] = '교육'
    contact.loc[contact['Industry'] == 'Transportation', 'Industry'] = '운송'
    return contact    

def isfam(self, contact):
    company = list(contact.Company)
    isfam = list(map(get_isfam, company))
    contact['isfam'] = isfam
    return contact


class Mapping:
     def __init__(self):
        super().__init__()
    
     def mapping0(self, contactDB):# 매핑 불가한 contact 우선 제쳐두기 (cannot map)
        personal = ['naver.com', 'gmail.com', 'hanmail.net', 'daum.net', 'nate.com', 'hotmail.com', 'kakao.com', 'yahoo.com', 'Yahoo.com',\
                    'icloud.com' 'paran.com', 'empal.com' ,'yahoo.co.kr', 'outlook.com']
        contact_email = list(contactDB['Email Address Domain'])
        index = []
        for i in range(len(contact_email)):
            email = contact_email[i]
            if email in personal:
                index.append(i)
            else:
                index.append(None)
        index = pd.Series(index).dropna()
        temp = contactDB.iloc[index, ]
        cannot_map = temp[(temp.Company.isna()) & (temp.Company_Mapping_Code.isna())]

        cannot_map['CompanyID'] = None
        to_map = contactDB.drop(cannot_map.index) # 매핑 해야하는 contact
        print('mapping0 결과 -> to_map.shape: ', to_map.shape, 'cannot_map.shape: ', cannot_map.shape)
        return cannot_map, to_map
    
    # 1. ContactDB기준 Company Mapping Code가 NA가 아닌 값 우선
     def mapping1(self, to_map):
        mapped1 = to_map[to_map.Company_Mapping_Code.notna()]
        idx = mapped1.index
        mapping_code = list(mapped1.Company_Mapping_Code)
        companyid = list(map(mapping_code_id, mapping_code)) # mapping_code_id 함수사용
        mapped1['CompanyID'] = companyid 
        print('mapping1 결과 -> mapped1.shape: ', mapped1.shape)
        return mapped1

    # 2. ContactDB기준 Company Mapping Code가 NA인 값 
     def mapping2(self, to_map, accountDB):
        to_map = to_map[to_map.Company_Mapping_Code.isna()]
        notna = to_map[to_map.Company_Mapping_Code.notna()]
        
        email_list = list(accountDB[accountDB.is_identify_by_email == 'Y']['회사 이메일 도메인'])
        email_domain = list(to_map['Email Address Domain'])

        companyid = []
        for i in range(len(email_domain)):
            email = email_domain[i]
            c_id = use_email(email, email_list) # use_email 함수 사용 
            companyid.append(c_id)

        to_map['CompanyID'] = companyid
        mapped2= to_map[to_map.CompanyID.notna()]
        to_map = to_map[to_map.CompanyID.isna()]
        
        print('mapping2 결과 -> to_map.shape: ', to_map.shape, 'mapped2.shape: ', mapped2.shape)
        return to_map, mapped2


    # 3. 이름 확인 
     def mapping3(self, to_map, accountDB):
        to_map.reset_index(drop = True, inplace=True)

        not_mapped_company = list(map(manipulate_string, list(to_map.Company))) # manipulate_string 함수 사용
        accountDB_company = list(map(manipulate_string, list(accountDB['Company Name'])))

        contact_index = []; companyID = []
        for i in range(len(not_mapped_company)):
            company = not_mapped_company[i]
            if company in accountDB_company:
                account_idx = accountDB_company.index(company)
                companyid = accountDB['CompanyID'][account_idx]
                companyID.append(companyid)
                contact_index.append(i)
            else:
                pass

        mapped3 = to_map.iloc[contact_index]
        mapped3['CompanyID'] = companyID
        to_map.drop(contact_index, axis=0, inplace = True) # 미분류 
        print('mapping3 결과 -> to_map.shape: ', to_map.shape, 'mapped3.shape: ', mapped3.shape)
        return to_map, mapped3

    # 자동화 어려운 회사명은 직접 확인 후 매핑 
     def mapping4(self, to_map):
        contact_email = list(to_map['Email Address Domain'])
        companyId = list(map(get_companyID, contact_email))
        to_map['CompanyID'] = companyId 
        mapped4 = to_map[to_map.CompanyID.notna()]
        to_map = to_map.drop(mapped4.CompanyID)
        print('mapping4 결과 -> to_map.shape: ', to_map.shape, 'mapped4.shape: ', mapped4.shape)
        return to_map, mapped4

     def mapping5(self,to_map):
        category = get_companyID2()
        temp = pd.merge(to_map.drop(['CompanyID'],axis=1), category, on='Company',how='left')
        mapped5 = temp[temp.CompanyID.notna()]
        to_map =  temp[temp.CompanyID.isna()]
        print('mapping5 결과 -> to_map.shape: ', to_map.shape, 'mapped5.shape: ', mapped5.shape)
        return to_map, mapped5

     def mapping6(self, to_map, cannot_map):
        to_map.reset_index(drop = True, inplace=True)
        # 매핑 코드, 등등 다 걸어준 후에 돌리는 함수 
        to_delete = ['.','-','무','1','대학생','회사','a', 'd', 'dd', '..', 'x', '개인', 'free', '집', \
                    '개인사업', '개인사업자', 'none', 'X', 'IT', 'ABC', \
                    'ㅇ', '비공개', 'w', '개인사업', '-', 'd', '--', '대학교', 'j',\
                    'dps','ㆍ', '백수', '...','it', '123' ,'ㅇㅇ','초등학교','abc','aaa',\
                    '유진','대학원생','ss','병원','군', 'None', '11','일반인','*','회사명',\
                    'aa','연구소','asdfasdf','취준','무직','농업','없음','ㅁㄴㅇㄹ','n','ㄴ',\
                    '111','강사', '대학원', 'ㅡ','fd','미정','df', '김','유라','서연','가나다','김만기'\
                    '정윤상','정윤상','aaabbcc','(개인)', '직장인','서울','자','휴직','kk','신백초등학교',\
                    '대학','G', 'No','Freelancer','.','Home', '김만기','Freelance', None]

        contact_company = list(to_map.Company)
        index = []
        for i in range(len(contact_company)):
            company = contact_company[i]
            if company in to_delete:
                index.append(i)
            else:
                index.append(None)

        idx = list(pd.Series(index).dropna())
        temp = to_map.iloc[idx, :]
        temp['CompanyID'] = None
        cannot_map = cannot_map.append(temp)
        to_map = to_map.drop(idx)  # to_map, cannot_map, not_mapped 
        not_mapped = to_map.copy()
        not_mapped.reset_index(drop = True, inplace=True)
        
        #sk그룹만 
        sk_idx = list(not_mapped[not_mapped['Email Address Domain'] =='sk.com'].index)
        sk_to_map = not_mapped.iloc[sk_idx,:]
        not_mapped = not_mapped.drop(sk_idx)
        CompanyID = list(map(get_companyID3, list(sk_to_map.Company)))
        sk_to_map['CompanyID'] = CompanyID
        
        mapped6 = sk_to_map.copy() #mapped6, not_mapped

        #print('mapping6 결과 \n-> cannot_map.shape',cannot_map.shape, 'to_map.shape: ', to_map.shape, 'mapped6.shape: ', mapped6.shape)
        return cannot_map,not_mapped, to_map, mapped6

class Title:
    def __init__(self):
        super().__init__()

    def get_title1(title):
        jsm = ['시니어컨설턴트', '선임', '담당', '과장', '차장', '대리', '부부장', '계장', '실장', '매니저', '사원', 'PM', 'SeniorSpeciallist', '시니어매니저', '시니어미내저',
        '연구원', '책임연구원', '전임', '주임', '담당자', '선임연구원', '사원 ', '책임 ', 'manager', '비상안전기획관', '부실장',
        'Business Develop manager for Finance Industry Service', '분부장','정보보호진단분석담당', 'TM', 'Manager', 'Project Manager']
        tl = ['파트장', '팀장', '팀장/전문위원', '개발리더(연구위원)', '팀장(전임)', 'TF장', '센터장', '수석', '지점장', '부장', '부문장', "팀장\u3000", '팀원', '부장 ', '위원',
        '팀장(전문위원)', '연구위원', 'Task Leader', 'TP Leader', '팀장 ', '연구위원/TP Leader', '연구위원/Task Leader', '전문위원', 'Business Leader', '그룹장', '부서장',
        '전문위원 ', '대표/소장', '팀장/부국장', 'Principal Consultant ', '시니어매니저/팀장', 'head', '수석팀장']
        ex = ['상무', '수석연구위원(전무)', '수석연구위원(상무)', '수석전문위원(상무)', '이사', 'CIO', '본부장', '상무보', '고문', '상임이사', '부문장(상무)', '임원', 'COO/PO', 'CTO',
        'ciso', '본부장/CIO']
        ve = ['부사장', '수석연구위원(부사장)', '부회장', 'C-Level / VP / Director']
        ceo = ['대표', '회장', 'CEO', 'CEO/CIO', '대표이사', '연구소장/대표이사', 'President']

        if title in jsm:
            return 'Junior/Senior Manager'
        elif title in tl:
            return 'Team Leader'
        elif title in ex:
            return 'Executive'
        elif title in ve:
            return 'Vice-Executive'
        elif title in ceo:
            return 'CEO'
        else:
            return 'Unknown'
def get_title2(title):
    prof = ['Adjunct Professor', 'Professor', '교수', '교수진', '조교수', '연구교수']
    jsm2 = ['사원 ', '임직원', '기장', '선임 유틸리티', '과장', '매니저겸 총무', '매니저', '파트장', '사원', '대리', '생산직', 'PM', '직원', '차장', '책임', '선임','수석', '담당',
    '주임', '마케팅 실장', '토목', '연구원', '선임연구원', '실장', '장애인 복지 ', 'Unit Manager', '영양사','부부장','책임 연구원', '반장', 'Solution Engineer / 과장']
    useless = ['Attorney', 'Public Accountant', '인턴', '근로자', '교직원', '상담원', '조교', '시설관리', '종업원', '학부생', '학생', '프리랜서강사', '직급이 없습니다. ',
    '무직', '교사', '학생 고 3', '대학원생', '대학생', 'cadet', '교육생', '강사', 'X', '주부', '없음']
    unkn = ['.', '-']
    tl2 = ['부장', '지점장', '전문위원', '부서장']
    ex2 = ['고문', '자문역', '부문장 ', '부문장', '상근자문']
    if title in prof:
        return 'Professor'
    elif title in jsm2:
        return 'Junior/Senior Manager'
    elif title in useless:
        return 'useless'
    elif title in tl2:
        return 'Team Leader'
    elif title in ex2:
        return 'Executive'
    else:
        return 'Unknown'

class Grouping:
    def __init__(self):
        super().__init__()

    def group_title(self, title):# 직급 변수 
        title_dict = {'C-Level':['Vice-Executive','Executive','CEO'],
                    'Team Leader': ['Team Leader'],
                    'Manager':['Junior/Senior Manager']}

        labels =  list(title_dict.keys())
        if title in title_dict[labels[0]]:
            return labels[0]
        elif title in title_dict[labels[1]]:
            return labels[1]
        elif title in title_dict[labels[2]]:
            return labels[2]
        elif pd.isna(title):
            return 'unknown'
        elif title == 'Unknown':
            return 'unknown'
        else:
            return 'etc'
   
    def group_industry(self, industry): # 산업 변수 
        if pd.isna(industry):
            return '산업_unknown'
        elif industry == '제조':
            return '산업_제조'
        elif industry == 'IT서비스':
            return '산업_IT서비스'
        elif industry == '일반서비스':
            return '산업_일반서비스'
        elif industry == '금융':
            return '산업_금융'
        else:
            return '산업_others'
