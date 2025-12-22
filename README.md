# pychat

- Dùng openai API để tạo một chatbot, chạy trong môi trường terminal, gõ câu hỏi và chương trình sẽ trả lời dạng stream các từ. Nó có khả năng nhớ ngữ cảnh kể cả lúc thoát chương trình và chạy lại nhờ lưu vào thư mục data.
- Dữ liệu được lưu trữ trong thư mục data như sau:
    - Có một file data/config.json chứa system prompt và last sessiion id
    - có một thư mục data/sessions/ chứa chat-[session_id].json
- Trong bộ nhớ của chương trình, nó sẽ quản lý session hiện tại với session_id được tạo mới nếu chưa có hoặc lấy lại id cũ từ config.json 
- Mỗi khi có một message mới, nó sẽ ghi vào file chat-[session_id].json và gửi vào openai API
- ưu tiên dùng dùng API  client.chat.completions() với stream=True, có gửi kèm system prompt và chat history của session hiện tại
- khi user gõ "new" thì tạo một session mới thay vì xem đó là prompt
