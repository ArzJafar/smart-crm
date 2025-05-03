import os
import pandas as pd
from dotenv import load_dotenv
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from bidi.algorithm import get_display

load_dotenv()

data_dir = os.getenv("DATA_DIR")
final_table_path = os.path.join(data_dir, "final_table.csv")
mbti_data_path = os.path.join(data_dir, "mbti_data.csv")
ready_data_path = os.path.join(data_dir, "ready.csv")
output_dir =  os.path.join(data_dir, "export")
font_path = os.getenv("FONT_PATH")
pdfmetrics.registerFont(TTFont("Vazir", font_path))


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
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, filename)
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    logo_path = 'D:/Pro/Smart/smartchekad/productionfiles/pics/Logo-Chekad-PNG.png'
    c.drawImage(logo_path, x=width / 2 - 50, y=height - 50, width=100, height=30, mask='auto')
    c.setFont("Vazir", 16)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 90, get_display(f"{user_dic['name']}"))
    c.setFillColor(colors.black)

    y_position = height - 160
    section_width = (width - 100) / 2
    margin_x = 30
    section_spacing = 20

    c.setFillColor(colors.lightblue)
    c.rect(margin_x, y_position - 110, section_width, 110, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Vazir", 12)
    c.drawString(margin_x + 10, y_position - 20, "English")
    c.setFont("Vazir", 10)

    english_total = int(user_dic['english-el']) + int(user_dic['english-in1']) + int(user_dic['english-in2']) + int(user_dic['english-ad'])
    language_data = [
        ("Elementary:", user_dic['english-el']),
        ("Intermediate 1:", user_dic['english-in1']),
        ("Intermediate 1:", user_dic['english-in2']),
        ("Advanced:", user_dic['english-ad']),
        ("Totally:", f"{english_total} / 20"),
    ]

    y_data = y_position - 40
    for label, value in language_data:
        c.drawString(margin_x + 10, y_data, f"{label} {value}")
        y_data -= 15

    c.setFillColor(colors.lightblue)
    c.rect(margin_x + section_width + section_spacing, y_position - 110, section_width, 110, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Vazir", 12)
    c.drawString(margin_x + section_width + section_spacing + 10, y_position - 20, "Excel")
    c.setFont("Vazir", 10)

    excel_total = int(user_dic['excel-el']) + int(user_dic['excel-in']) + int(user_dic['excel-ad'])
    excel_data = [
        ("Elementary:", user_dic['excel-el']),
        ("Intermediate:", user_dic['excel-in']),
        ("Advanced:", user_dic['excel-ad']),
        ("Totally:", f"{excel_total} / 15"),
    ]

    y_data = y_position - 40
    for label, value in excel_data:
        c.drawString(margin_x + section_width + section_spacing + 10, y_data, f"{label} {value}")
        y_data -= 15

    y_position -= 130
    c.setFillColor(colors.lightgrey)
    c.rect(margin_x, y_position - 40, width - 80, 40, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Vazir", 12)
    c.drawString(margin_x + 10, y_position - 23, "MBTI:")
    c.setFont("Vazir", 10)
    c.drawString(margin_x + 50, y_position - 23, user_dic['results'])

    y_position -= 60
    c.setFillColor(colors.lightgrey)
    c.rect(margin_x, y_position - 40, width - 80, 40, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Vazir", 12)
    c.drawString(margin_x + 10, y_position - 23, "IQ:")
    c.setFont("Vazir", 10)
    c.drawString(margin_x + 35, y_position - 23, str(user_dic['IQ']))

    c.save()

def generate_all_user_pdfs(all_users_data):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for user_dic in all_users_data:
        filename = f"{user_dic['name'].replace(' ', '_')}_Report.pdf"
        create_user_pdf(user_dic, filename)
        print(f"✅Done! PDF created for {user_dic['name']}.")


user()
generate_all_user_pdfs(all_users_data)
print("✅Done! All PDFs created successfully.")
print('✅Done!')
