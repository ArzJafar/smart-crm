import os
import pandas as pd
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

load_dotenv()

data_dir = os.getenv("DATA_DIR")
final_table_path = os.path.join(data_dir, "final_table.csv")
mbti_data_path = os.path.join(data_dir, "mbti_data.csv")
ready_data_path = os.path.join(data_dir, "ready.csv")
output_dir =  os.path.join(data_dir, "export")

data = pd.read_csv(final_table_path)
mbti_data = pd.read_csv(mbti_data_path)

tahlili = {
    10: "fail", 11: 76, 12: 79, 13: 81, 14: 83, 15: 86, 16: 88, 17: 91,
    18: 93, 19: 96, 20: 98, 21: 101, 22: 104, 23: 107, 24: 111, 25: 114,
    26: 118, 27: 122, 28: 128, 29: 131, 30: 136
}

user_data = data.groupby('user_id')

all_users_data = []

def user():
    for id, user in user_data:
        user_dic = {
            'id': id,
            'name': user['name'].iloc[0],
            'email': user['email'].iloc[0],
            'ip': user['ip'].iloc[0],
            'tahlili-c': 0,
            'tahlili-d': 0,
            'tahlili-e': 0,
            'tahlili-f': 0,
            'english-el': 0,
            'english-in1': 0,
            'english-in2': 0,
            'english-ad': 0,
            'excel-el': 0,
            'excel-in': 0,
            'excel-ad': 0,
        }

        for _, row in user.iterrows():
            if row['correct_count'] == 1:
                if 67 <= row['question_id'] < 73:
                    user_dic['tahlili-c'] += 1
                elif 73 <= row['question_id'] < 79:
                    user_dic['tahlili-d'] += 1
                elif 79 <= row['question_id'] < 85:
                    user_dic['tahlili-e'] += 1
                elif 85 <= row['question_id'] < 97:
                    user_dic['tahlili-f'] += 1
                elif 146 <= row['question_id'] < 151:
                    user_dic['english-el'] += 1
                elif 151 <= row['question_id'] < 156:
                    user_dic['english-in1'] += 1
                elif 156 <= row['question_id'] < 161:
                    user_dic['english-in2'] += 1
                elif 161 <= row['question_id'] < 166:
                    user_dic['english-ad'] += 1
                elif 168 <= row['question_id'] < 173:
                    user_dic['excel-el'] += 1
                elif 173 <= row['question_id'] < 178:
                    user_dic['excel-in'] += 1
                elif 178 <= row['question_id'] < 183:
                    user_dic['excel-ad'] += 1

        total_tahlili = sum([user_dic[key] for key in ['tahlili-c', 'tahlili-d', 'tahlili-e', 'tahlili-f']])
        iq_result = tahlili.get(total_tahlili, "Unknown")
        user_dic['IQ'] = iq_result

        add_mbti(user_dic)

        all_users_data.append(user_dic)

    write_to_csv()

def add_mbti(dic):
    user_name = dic['name']
    mbti_row = mbti_data[mbti_data['Username'] == user_name]
    
    if not mbti_row.empty:
        result_scale = mbti_row['result scale'].iloc[0]
        for row in result_scale.split(','):
            row = row.split('(')
            natije = row[1].split('\xa0')[0]
            dic[f'mbti-{row[0]}'] = natije

        dic['result_scale'] = mbti_row['result scale'].iloc[0]
        dic['results'] = mbti_row['results'].iloc[0]
    else:
        dic['result_scale'] = "Unknown"
        dic['results'] = "Unknown"

def write_to_csv():
    final_data = pd.DataFrame(all_users_data)
    final_data.to_csv(ready_data_path, index=False, encoding='utf-8')


def create_user_pdf(user_dic, filename="user_report.pdf"):
    file_path = os.path.join(output_dir, filename)
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 10)
    
    c.drawString(200, height - 40, f"User Report: {user_dic['name']}")

    y_position = height - 60
    c.drawString(50, y_position, f"Name: {user_dic['name']}")
    y_position -= 20
    c.drawString(50, y_position, f"Email: {user_dic['email']}")
    y_position -= 20
    c.drawString(50, y_position, f"IP: {user_dic['ip']}")
    y_position -= 40

    sections = ['english-el', 'english-in1', 'english-in2', 'english-ad', 'excel-el', 'excel-in', 'excel-ad']
    for section in sections:
        if section in user_dic:
            y_position -= 20
            c.drawString(50, y_position, f"{section.replace('-', ' ').capitalize()}: {user_dic[section]}")

    y_position -= 20
    c.drawString(50, y_position, f"IQ: {user_dic['IQ']}")

    c.save()

def generate_all_user_pdfs(all_users_data):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for user_dic in all_users_data:
        filename = f"{user_dic['name'].replace(' ', '_')}_Report.pdf"
        create_user_pdf(user_dic, filename)
        print(f"PDF created for {user_dic['name']}.")



user()
generate_all_user_pdfs(all_users_data)
print("All PDFs created successfully.")
print('✅Done!')
