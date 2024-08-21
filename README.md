
# RAG BASED CHATBOT FINANCIAL INSIGHT

Chatbot trả lời các câu hỏi về Báo cáo tài chính của công ty Sun Asterisk dựa vào dữ liệu được cung cấp. Dữ liệu cung cấp cho mô hình có thể được thêm hoặc sửa đổi để cập nhập những thông tin mới nhất về tình hình tài chính của công ty.

## Link test sản phẩm
https://54e7pcmiyg6qlfg6uszu7rz7ia0lisxv.lambda-url.us-east-1.on.aws/docs#/default/get_query_endpoint_get_query_get
## MÔ TẢ KIẾN TRÚC
![Image Description](https://github.com/sirgecko84/RAG-based-Chatbot-Financial-Insight/blob/master/cimg.PNG)


Dữ liệu cung cấp cho mô hình sẽ là các file PDF về Báo cáo tài chính thường niên hoặc hàng quý của công ty Sun Asterisk. Sau đó, dữ liệu này sẽ được chia thành các đoạn nhỏ (chunks) để thu nhỏ nguồn thông tin cung cấp cho mô hình LLM về sau.

Các chunk dữ liệu sau đó sẽ được chuyển sang dạng vector embedding và lưu trữ trong cơ sở dữ liệu (vector database).

Khi người dùng đặt câu hỏi, mô hình sẽ thực hiện chuyển câu hỏi về dạng vector embedding và tìm kiếm trong database các thông tin có nội dung liên quan đến câu hỏi đó. Các nội dung liên quan đến câu hỏi được đưa ra (context) sẽ được thêm vào phần prompt của mô hình LLM để dựa vào đó đưa ra câu trả lời cho người dùng.

![Image Description](https://github.com/sirgecko84/RAG-based-Chatbot-Financial-Insight/blob/master/ragapppic1.PNG)

App sẽ dùng mô hình AI cloud-based từ Amazon Bedrock để thực hiện phần Embedding dữ liệu và Generate câu trả lời. Ngoài ra, App sẽ được chạy ở local, và database của App cũng được lưu tại local.

Về phần Deploy :


![Image Description](https://github.com/sirgecko84/RAG-based-Chatbot-Financial-Insight/blob/master/aiii.PNG)


Sử dụng FastAPI để tạo API Endpoint cho App. Sever sẽ làm việc với app bằng AWS Lambda thông qua Handler. Cuối cùng, ta đóng gói toàn bộ project bằng Docker trước khi deploy. Sau khi deploy, người dùng có thể truy cập vào app thông qua API Endpoint đã được public.

## Công nghệ sử dụng

- Mô hình LLM: Amazon Bedrock anthropic.claude-3-haiku-20240307-v1:0
- Embedding function: BedrockEmbeddings
- Vector database: Chroma
- Thư viện LLM: langchain
- Load các file PDF: pypdf
- Tạo API Endpoint: FastApi
- Đóng gói project: Docker
- Deploy: AWS Lambda

# Hướng dẫn chạy sản phẩm

## Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```
## Create database
```bash
python .\populate_database.py
```
## Starting FastAPI Server
```bash
# From image/src directory.
python app_api_handler.py
```
Sau đó truy cập vào đường dẫn http://0.0.0.0:8000/docs để test. Nếu gặp lỗi, hãy sửa file app_api_handler như sau: host = 127.0.0.1 
Trước khi build docker image, hãy đổi lại host = 0.0.0.0

## Build Docker Image
```bash
docker build --platform linux/amd64 -t aws_rag_app .
```
## Run Docker Image at local
```bash
docker run --rm -p 8000:8000 --entrypoint python --env-file .env aws_rag_app app_api_handler.py
```
## Deploy to AWS
```bash
cdk deploy
```
