
# RAG BASED CHATBOT FINANCIAL INSIGHT

Chatbot trả lời các câu hỏi về Báo cáo tài chính của công ty Sun Asterisk dựa vào dữ liệu được cung cấp. Dữ liệu cung cấp cho mô hình có thể được thêm hoặc sửa đổi để cập nhập những thông tin mới nhất về tình hình tài chính của công ty.

## Video giới thiệu sản phẩm
https://drive.google.com/drive/folders/1sXK2pXhHTA0WTdqzlc-IqSHtH5NYMx-_?usp=sharing
## MÔ TẢ KIẾN TRÚC
![Image Description](https://github.com/sirgecko84/RAG-based-Chatbot-Financial-Insight/blob/master/cimg.PNG)


Dữ liệu cung cấp cho mô hình sẽ là các file PDF về Báo cáo tài chính thường niên hoặc hàng quý của công ty Sun Asterisk. Sau đó, dữ liệu này sẽ được chia thành các đoạn nhỏ (chunks) để thu nhỏ nguồn thông tin cung cấp cho mô hình LLM về sau.

Các chunk dữ liệu sau đó sẽ được chuyển sang dạng vector embedding và lưu trữ trong cơ sở dữ liệu (vector database).

Khi người dùng đặt câu hỏi, mô hình sẽ thực hiện chuyển câu hỏi về dạng vector embedding và tìm kiếm trong database các thông tin có nội dung liên quan đến câu hỏi đó. Các nội dung liên quan đến câu hỏi được đưa ra (context) sẽ được thêm vào phần prompt của mô hình LLM để dựa vào đó đưa ra câu trả lời cho người dùng.


## Công nghệ sử dụng

- Mô hình LLM: Mistral (self host thông qua Ollama)
- Embedding function: nomic-embed-text (self host thông qua Ollama)
- Vector database: Chroma
- UI: Streamlit
- Thư viện LLM: langchain
- Load các file PDF: pypdf
- Test mô hình: pytest

# Hướng dẫn chạy sản phẩm

## Cài đặt Ollama:
[Ollama](https://ollama.com)

## Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```
## Creaate database
```bash
python .\populate_database.py
```
## Run Streamlit app
```bash
streamlit run app.py
```

