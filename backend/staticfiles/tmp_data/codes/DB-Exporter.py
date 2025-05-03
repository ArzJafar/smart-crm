import mysql.connector
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
connection = mysql.connector.connect(**db_config)


def export_table_to_csv(connection, table_name, file_path):
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
        writer.writerows(result)
        print(f"✅Done! {table_name} CSV created in: {file_path}")

    cursor.close()


def export_tables_to_excel(connection, tables, excel_file_path):
    tables["mbti_results"] = [os.path.join(data_dir, "mbti_results.csv")]
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        for table_name, file_path in tables.items():
            cursor = connection.cursor()
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(result, columns=column_names)
            sheet_name = table_name[:30]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"✅Done! Sheet '{sheet_name}' added to Excel: {excel_file_path}")

            cursor.close()


def merge_tables(connection):
    query1 = "SELECT * FROM wp_wp_pro_quiz_statistic_ref"
    query2 = "SELECT * FROM wp_wp_pro_quiz_statistic"
    query3 = "SELECT * FROM wp_wp_pro_quiz_toplist"

    table1 = pd.read_sql(query1, connection)
    table2 = pd.read_sql(query2, connection)
    table3 = pd.read_sql(query3, connection)

    merged_1_2 = pd.merge(table1, table2, on="statistic_ref_id", how="inner")
    final_merged = pd.merge(merged_1_2, table3, on=["quiz_id", "user_id"], how="inner")

    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS final_table")

    create_table_query = """
    CREATE TABLE final_table (
        statistic_ref_id INT,
        question_id INT,
        correct_count INT,
        incorrect_count INT,
        hint_count INT,
        solved_count INT,
        points FLOAT,
        question_time INT,
        answer_data TEXT,
        quiz_id INT,
        user_id INT,
        create_time BIGINT,
        is_old TINYINT,
        form_data TEXT,
        toplist_id INT,
        date BIGINT,
        name VARCHAR(255),
        email VARCHAR(255),
        result FLOAT,
        ip VARCHAR(45)
    )
    """
    cursor.execute(create_table_query)

    for _, row in final_merged.iterrows():
        insert_query = """
        INSERT INTO final_table (
            statistic_ref_id, question_id, correct_count, incorrect_count, hint_count, solved_count, points, 
            question_time, answer_data, quiz_id, user_id, create_time, is_old, form_data, toplist_id, 
            date, name, email, result, ip
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row.get("statistic_ref_id", None), row.get("question_id", None), row.get("correct_count", None),
            row.get("incorrect_count", None), row.get("hint_count", None), row.get("solved_count", None),
            row.get("points", None), row.get("question_time", None), row.get("answer_data", None),
            row.get("quiz_id", None), row.get("user_id", None), row.get("create_time", None),
            row.get("is_old", None), row.get("form_data", None), row.get("toplist_id", None),
            row.get("date", None), row.get("name", None), row.get("email", None),
            row.get("result", None), row.get("ip", None)
        )
        cursor.execute(insert_query, values)

    connection.commit()
    print("✅Done! Final table created and updated in database.")

    cursor.close()


def mbti_export():
    login_url = "https://hr.chekad.com/wp-login.php"
    target_url = "https://hr.chekad.com/wp-admin/edit.php?post_type=wpt_test&page=wpt_test_respondents_results"
    username = os.getenv("WP_USERNAME")
    password = os.getenv("WP_PASSWORD")
    session = requests.Session()
    
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")
    hidden_fields = {tag['name']: tag['value'] for tag in soup.find_all("input", {"type": "hidden"})}
    login_data = {
        'log': username,
        'pwd': password,
        'rememberme': 'forever',
        'wp-submit': 'Log In',
        'redirect_to': '/wp-admin/',
        'testcookie': '1',
        **hidden_fields
    }
    
    login_response = session.post(login_url, data=login_data, allow_redirects=True)
    if "wp-admin" in login_response.url:
        print("✅Done! Logged In.")
    else:
        print("❌incomplete! Logging failed.")
        print(login_response.text)
        exit()

    response = session.get(target_url, allow_redirects=True)
    if response.status_code == 200 and "wp-admin" in response.url:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        
        data_dir = os.getenv("DATA_DIR")
        csv_file = os.path.join(data_dir, "mbti_data.csv")
        
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Test", "result scale", "results", "Username", "Dvice", "IP", "Browser", "Date"])
            
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 9:
                    id_value = re.sub(r'\D', '', cols[0].get_text(strip=True))
                    result_scale = cols[2].get_text(strip=True)
                    results = cols[3].get_text(strip=True)
                    name = cols[4].get_text(strip=True)
                    device = cols[5].get_text(strip=True)
                    ip = cols[6].get_text(strip=True)
                    browser = cols[7].get_text(strip=True)
                    date = cols[8].get_text(strip=True)
                    
                    writer.writerow([id_value, result_scale, results, name, device, ip, browser, date])
                else:
                    print(f"Skipping row with insufficient columns: {row}")
        
        print(f"✅Done! MBTI data saved to {csv_file}.")
    else:
        print(f"❌incomplete! Error accessing page: {response.status_code}")
        print(response.url)


def save_csv_to_db(connection):
    data_dir = os.getenv("DATA_DIR")
    csv_file = os.path.join(data_dir, "mbti_data.csv")
    df = pd.read_csv(csv_file)
    df = df.where(pd.notnull(df), None)

    cursor = connection.cursor()
    table_name = "mbti_results"
    
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    create_table_query = f"""
    CREATE TABLE {table_name} (
        ID INT PRIMARY KEY,
        Test VARCHAR(255),
        result_scale VARCHAR(255),
        results VARCHAR(255),
        username VARCHAR(255),
        device VARCHAR(255),
        ip VARCHAR(255),
        browser VARCHAR(255),
        date VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)
    
    insert_query = f"""
    INSERT INTO {table_name} (ID, Test, result_scale, results, username, device, ip, browser, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    data = df.values.tolist()
    
    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"✅Done! MBTI data saved to database table '{table_name}'.")
    except mysql.connector.Error as err:
        print(f"❌Error: {err}")
        connection.rollback()

    cursor.close()


data_dir = os.getenv("DATA_DIR")
tables = {
    "wp_wp_pro_quiz_category": os.path.join(data_dir, "quiz_category.csv"),
    "wp_wp_pro_quiz_lock": os.path.join(data_dir, "quiz_lock.csv"),
    "wp_wp_pro_quiz_statistic": os.path.join(data_dir, "quiz_statistic.csv"),
    "wp_wp_pro_quiz_statistic_ref": os.path.join(data_dir, "statistic_ref.csv"),
    "wp_wp_pro_quiz_toplist": os.path.join(data_dir, "toplist.csv"),
    "final_table": os.path.join(data_dir, "final_table.csv"),
}
excel_file_path = os.path.join(data_dir, "all_data(excel_view).xlsx")

mbti_export()
save_csv_to_db(connection)
merge_tables(connection)

for table_name, file_path in tables.items():
    export_table_to_csv(connection, table_name, file_path)
export_tables_to_excel(connection, tables, excel_file_path)

connection.close()

print("✅Everything done.")