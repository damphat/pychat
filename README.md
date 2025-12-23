# pychat

Một project mini thử nghiệm vibe coding, tích hợp OpenAI API để chat qua terminal hoặc giao diện web đơn giản.

## Tính năng
- Chat qua Terminal (CLI).
- Chat qua giao diện Web (Gradio).
- Tự động lưu và tải lại lịch sử hội thoại (session) trong `data/sessions/`.
- Hỗ trợ streaming response.

## Cài đặt

Yêu cầu Python 3.12+.

```bash
# Cài đặt bằng uv
uv sync

# Hoặc bằng pip
pip install -r pyproject.toml
```

Thiết lập API Key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Cách dùng

### Terminal (CLI)
```bash
python main.py
```
*Gõ `new` để tạo session mới.*

### Web UI
```bash
python main_ui.py
```

### Chạy Tests
```bash
pytest
```

## Cấu trúc file
- `chat_app.py`: Logic xử lý chính và kết nối OpenAI.
- `main.py` / `main_ui.py`: Entry point cho CLI và Web.
- `chat_config.py` / `data_session.py`: Quản lý cấu hình và lưu trữ session.
- `data/`: Chứa lịch sử chat và cấu hình JSON.