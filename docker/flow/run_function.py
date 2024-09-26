# Import libraries
from promptflow.core import tool
import json
import pandas as pd
from azure.storage.blob import BlobServiceClient
import io
import os
from io import StringIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from azureml.core import Workspace, Model

url = 'https://businessai0409202401.blob.core.windows.net/demo-data/DemoKPI.xlsx'
def get_data():

    data = pd.read_excel(url)
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])
    # Save the filtered data to a new Excel file
    data['Date']=data['Date'].dt.strftime('%d/%m/%Y')
    json_to_xls(data.to_json(),'data.xlsx')
    return data.to_json()


def get_dep_data(name):
  try:
    data = pd.read_excel(url,sheet_name=['Total','IT','HR','AC'])[name]
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])
    # Save the filtered data to a new Excel file
    data['Date']=data['Date'].dt.strftime('%d/%m/%Y')
    json_to_xls(data.to_json(),'department_data.xlsx')
    return data.to_json()
  except Exception as e:
    # Trả về thông báo lỗi bằng tiếng Việt, mã hóa UTF-8
    error_message = f"Không thể lấy dữ liệu phòng ban: {str(e)}"
    return json.dumps({"error": error_message}, ensure_ascii=False)

def get_date_data(date,dep):
  try:
    # Read the Excel file
    data = pd.read_excel(url, engine='openpyxl',
                        sheet_name=['Total','IT','HR','AC'])[dep]
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])
    # Filter by specific dated
    filtered_data = data[data['Date'] == date]
    # Save the filtered data to a new Excel file
    filtered_data['Date']=filtered_data['Date'].dt.strftime('%d/%m/%Y')
    json_to_xls(filtered_data.to_json(),'week_data.xlsx')
    return filtered_data.to_json()
  except Exception as e:
    # Trả về thông báo lỗi bằng tiếng Việt, mã hóa UTF-8
    error_message = f"Không thể lấy dữ liệu ngày: {date} phòng ban: {str(e)}"
    return json.dumps({"error": error_message}, ensure_ascii=False)

def get_month_of_year_data(month,year,dep):
  try:
    # Read the Excel file
    data = pd.read_excel(url, engine='openpyxl',
                        sheet_name=['Total','IT','HR','AC'])[dep]
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])
    # Filter the data by the specified month
    data_in_month = data[data['Date'].dt.month == int(month)]
    # Filter the data by the specified year
    data_in_month = data_in_month[data_in_month['Date'].dt.year == int(year)]
    # Format the 'Date' column to 'dd/MM/yyyy'
    data_in_month['Date'] = data_in_month['Date'].dt.strftime('%d/%m/%Y')
    # Optionally, save the filtered data to a new Excel file
    json_to_xls(data_in_month.to_json(),'month_data.xlsx')
    return data_in_month.to_json()
  except Exception as e:
    # Trả về thông báo lỗi bằng tiếng Việt, mã hóa UTF-8
    error_message = f"Không thể lấy dữ liệu tháng {month} năm {year} tại phòng ban: {str(e)}"
    return json.dumps({"error": error_message}, ensure_ascii=False)

def get_year_data(year,dep):
  try:
    # Read the Excel file
    data = pd.read_excel(url, engine='openpyxl',
                        sheet_name=['Total','IT','HR','AC'])[dep]
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])
    # Filter the data by the specified year
    data_in_year = data[data['Date'].dt.year == int(year)]
    # Format the 'Date' column to 'dd/MM/yyyy'
    data_in_year['Date'] = data_in_year['Date'].dt.strftime('%d/%m/%Y')
    # Optionally, save the filtered data to a new Excel file
    json_to_xls(data_in_year.to_json(),'year_data.xlsx')
    return data_in_year.to_json()
  except Exception as e:
    # Trả về thông báo lỗi bằng tiếng Việt, mã hóa UTF-8
    error_message = f"Không thể lấy dữ liệu năm {year} tại phòng ban: {str(e)}"
    return json.dumps({"error": error_message}, ensure_ascii=False)

def get_quarter_data(year, quarter,dep):
  try:
    # Read the Excel file
    data = pd.read_excel(url, engine='openpyxl',
                         sheet_name=['Total', 'IT','HR', 'AC'])[dep]
    # Convert the 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])
    # Filter the data by the specified year and quarter
    data_in_quarter = data[(data['Date'].dt.year == int(year)) &
     (data['Date'].dt.quarter == int(quarter))]
    # Format the 'Date' column to 'dd/MM/yyyy
    data_in_quarter['Date'] = data_in_quarter['Date'].dt.strftime('%d/%m/%Y')
    # Optionally, save the filtered data to a new Excel file
    json_to_xls(data_in_quarter.to_json(),'quarter_data.xlsx')
    return data_in_quarter.to_json()
  except Exception as e:
    # Trả về thông báo lỗi bằng tiếng Việt, mã hóa UTF-8
    error_message = f"Không thể lấy dữ liệu năm {year} của quý {quarter} tại phòng ban: {str(e)}"
    return json.dumps({"error": error_message}, ensure_ascii=False)

def get_prediction_data():
    # URI tĩnh của Blob Storage
    uri = "https://procedureautom5977433134.blob.core.windows.net/azureml-blobstore-20274f28-f1cf-423d-81a7-d08d46da5ff4/score-data.csv"

    # Tạo BlobServiceClient từ URI
    blob_service_client = BlobServiceClient(account_url="https://procedureautom5977433134.blob.core.windows.net/")

    # Xác định tên container và blob từ URI
    container_name = "azureml-blobstore-20274f28-f1cf-423d-81a7-d08d46da5ff4"
    blob_name = "score-data.csv"

    # Lấy blob client từ service client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Tải dữ liệu từ blob
    stream_downloader = blob_client.download_blob()

    # Đọc dữ liệu vào DataFrame
    data = pd.read_csv(io.StringIO(stream_downloader.content_as_text()))

    # Chỉ giữ lại hai cột tĩnh
    selected_columns = ["KPI", "Scored Labels"]  # Thay thế bằng tên cột thực tế
    selected_data = data[selected_columns]

    return selected_data.to_json()

def send_email_with_attachment():

    subject = "Báo cáo"
    body = "Đây là báo cáo của bạn."
    receiver_email = "nguyenngogiahuy79@gmail.com"
    sender_email = "huynng2379@gmail.com"
    sender_password = "iwhx edws pgmn uvez"
    port = 587
    smtp_server = "smtp.gmail.com"
    file_path = None
    if(get_data()):
      file_path = "data.xlsx"
    elif(get_date_data()):
      file_path = "week_data.xlsx"
    elif(get_dep_data()):
      file_path = "department_data.xlsx"
    elif(get_month_of_year_data()):
      file_path = "month_data.xlsx"
    elif(get_year_data()):
      file_path = "year_data.xlsx"
    elif(get_quarter_data()):
      file_path = "quarter_data.xlsx"
    # Tạo đối tượng MIMEMultipart
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Thêm nội dung email
    message.attach(MIMEText(body, 'plain'))

    # Kiểm tra xem file có tồn tại không
    if os.path.exists(file_path):
        # Đọc file và đính kèm vào email
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Mã hóa file để gửi qua email
        encoders.encode_base64(part)

        # Thêm header vào phần đính kèm
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(file_path)}",
        )

        # Đính kèm phần file vào email
        message.attach(part)
    else:
        print("File không tồn tại!")

    # Kết nối với server SMTP và gửi email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Bắt đầu mã hóa TLS
            server.login(sender_email, sender_password)  # Đăng nhập vào tài khoản email
            server.send_message(message)  # Gửi email
            print("Email đã được gửi thành công!")
    except Exception as e:
        print(f"Đã có lỗi xảy ra khi gửi email: {e}")

def json_to_xls(json_data, output_file):
    try:
        # Chuyển đổi JSON thành DataFrame
        df = pd.read_json(json_data)

        # Lưu DataFrame thành file Excel
        df.to_excel(output_file, index=False)

    except Exception as e:
        print(f"Đã xảy ra lỗi khi chuyển đổi JSON sang Excel: {e}")

@tool
def run_function(response_message: dict) -> str:
    function_call = response_message.get("function_call", None)
    if function_call and "name" in function_call and "arguments" in function_call:
        function_name = function_call["name"]
        function_args = json.loads(function_call["arguments"])
        print(function_args)
        result = globals()[function_name](**function_args)
    else:
        print("No function call")
        if isinstance(response_message, dict):
            result = response_message.get("content", "")
        else:
            result = response_message
    return result
