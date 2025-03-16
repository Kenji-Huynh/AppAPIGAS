# Vietnamese AI Assistant

## Giới thiệu

Vietnamese AI Assistant là một ứng dụng desktop được phát triển bằng Python và Tkinter, giúp người dùng tương tác với API AI của Google Gemini để thực hiện nhiều tác vụ khác nhau. Ứng dụng có giao diện thân thiện với người dùng, hỗ trợ đa ngôn ngữ (chú trọng tiếng Việt) và có nhiều tính năng hữu ích.

## Tính năng chính

- **Tóm tắt văn bản**: Tóm tắt nội dung từ văn bản hoặc URL website
- **Chat với AI**: Trò chuyện trực tiếp với mô hình AI của Google Gemini
- **Chuyển văn bản thành giọng nói**: Đọc văn bản bằng nhiều giọng nói khác nhau
- **Tùy chỉnh cài đặt**: Cấu hình API, chọn mô hình AI và cài đặt giọng nói

## Yêu cầu hệ thống

- Python 3.7 trở lên
- Các thư viện được liệt kê trong file `requirements.txt`
- Kết nối internet để sử dụng API của Google Gemini
- API Key từ Google AI Studio (Google Gemini)

## Cài đặt

1. Clone repository hoặc tải xuống mã nguồn

2. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

3. Tạo file `.env` trong thư mục gốc của ứng dụng (hoặc thêm API key trong giao diện cài đặt):
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Chạy ứng dụng:
   ```
   python app.py
   ```

## Hướng dẫn sử dụng

### Tóm tắt văn bản

1. Truy cập tab "Tóm tắt văn bản"
2. Nhập văn bản cần tóm tắt hoặc URL website
3. Nhấn nút "Tóm tắt"
4. Kết quả sẽ hiển thị ở phần "Bản tóm tắt"
5. Có thể đọc bản tóm tắt bằng cách nhấn nút "Đọc bản tóm tắt"

### Chat với AI

1. Truy cập tab "Chat với AI"
2. Nhập câu hỏi hoặc yêu cầu vào ô văn bản
3. Nhấn nút "Gửi" hoặc phím Enter
4. AI sẽ phản hồi và hiển thị trong cửa sổ chat
5. Có thể nghe phản hồi bằng cách nhấn nút "Đọc phản hồi"

### Chuyển văn bản thành giọng nói

1. Truy cập tab "Chuyển văn bản thành giọng nói"
2. Nhập văn bản cần chuyển đổi
3. Tùy chỉnh các cài đặt giọng nói (nếu cần)
4. Nhấn nút "Đọc" để bắt đầu
5. Có thể dừng quá trình bằng nút "Dừng"

### Cài đặt

1. Truy cập tab "Cài đặt"
2. Cấu hình API key cho Google Gemini
3. Chọn mô hình AI phù hợp
4. Tùy chỉnh cài đặt giọng nói (ngôn ngữ, giới tính, tốc độ)
5. Kiểm tra cài đặt bằng các nút kiểm tra tương ứng

## Cấu trúc mã nguồn

Ứng dụng được thiết kế theo mô hình module, với mỗi tệp Python đảm nhận một chức năng cụ thể:

- `app.py`: Điểm khởi đầu của ứng dụng, khởi tạo giao diện và các module
- `api_manager.py`: Quản lý kết nối và tương tác với API của Google Gemini
- `voice_manager.py`: Quản lý các chức năng text-to-speech
- `web_scraper.py`: Trích xuất nội dung từ các trang web
- `summarizer_module.py`: Module tóm tắt văn bản
- `chat_module.py`: Module trò chuyện với AI
- `tts_module.py`: Module chuyển văn bản thành giọng nói
- `settings_module.py`: Module cài đặt ứng dụng
- `ui_factory.py`: Tạo các thành phần giao diện đồng nhất

## Lấy API Key

Để sử dụng ứng dụng, bạn cần một API key từ Google AI Studio:

1. Truy cập [Google AI Studio](https://makersuite.google.com/)
2. Đăng nhập bằng tài khoản Google
3. Tạo một API key mới
4. Sao chép API key và thêm vào ứng dụng thông qua tab Cài đặt

## Xử lý sự cố

- **Lỗi API key**: Đảm bảo rằng bạn đã nhập API key chính xác và hợp lệ
- **Lỗi mạng**: Kiểm tra kết nối internet của bạn
- **Lỗi giọng nói**: Đảm bảo rằng hệ thống của bạn có hỗ trợ text-to-speech
- **Ứng dụng không phản hồi**: Khởi động lại ứng dụng hoặc kiểm tra tài nguyên hệ thống

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng gửi Pull Request hoặc mở Issue nếu bạn có bất kỳ đề xuất cải tiến nào.

## Giấy phép

Phần mềm này được phân phối theo giấy phép MIT.
