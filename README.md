# pychat

Một project mini thử nghiệm vibe coding, tích hợp OpenAI API để chat qua terminal hoặc giao diện web đơn giản.

## Tính năng
- Chat qua Terminal (CLI).
- Chat qua giao diện Web (Gradio).
- Tự động lưu và tải lại lịch sử hội thoại (session) trong `data/sessions/`.
- Hỗ trợ streaming response.

## Cài đặt

Yêu cầu Python 3.12+. Khuyến nghị sử dụng [uv](https://github.com/astral-sh/uv) để quản lý project.

```bash
# Cài đặt dependencies
uv sync
```

Thiết lập API Key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Cách dùng

Project hỗ trợ chạy trực tiếp thông qua command `pychat` đã được định nghĩa trong `pyproject.toml`.

### Terminal (CLI)
Chạy chế độ chat command-line mặc định:
```bash
uv run pychat
```
*Gõ `new` để tạo session mới. Gõ Ctrl+C để thoát.*

### Web UI
Chạy chế độ giao diện web (Gradio):
```bash
uv run pychat web
```

### Chạy Tests
```bash
uv run pytest
```

## Cấu trúc project
Project sử dụng **src layout** tiêu chuẩn:

- `src/pychat/`: Source code chính (logic, ui, cli).
    - `__main__.py`: Entry point điều hướng CLI/Web.
    - `chat_app.py`: Logic xử lý chính và kết nối OpenAI.
    - `cli.py`: Giao diện dòng lệnh.
    - `web.py`: Giao diện web Gradio.
- `data/`: Chứa lịch sử chat và cấu hình JSON.
- `pyproject.toml`: Quản lý dependencies và cấu hình project.