from gradio.components.chatbot import MessageDict, Message
import asyncio
import gradio as gr
from chat_app import ChatApp

def create_ui():
    app = ChatApp()

    with gr.Blocks(title="ChatApp") as demo:
        gr.Markdown("# 🤖 ChatApp with Gradio")

        def to_list_message_dict(messages) -> list[Message | MessageDict]:
            return messages
        
        chatbot = gr.Chatbot(
            value=to_list_message_dict(app.messages),
            height=600
        )

        msg = gr.Textbox(placeholder="Type your message here...", show_label=False)
        clear = gr.Button("Clear Session (New Chat)")

        def user(user_message, history):
            # Gradio 6 history is a list of dictionaries
            if history is None:
                history = []
            return "", history + [{"role": "user", "content": user_message}]

        def bot(history):
            if not history:
                return history
            
            user_message = history[-1]["content"]
            
            # Add assistant message placeholder
            history.append({"role": "assistant", "content": ""})
            
            # yield history
            for chunk in app.send_message(user_message):
                history[-1]["content"] += chunk
                yield history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )

        def handle_clear():
            app.new_session()
            return []

        clear.click(handle_clear, None, chatbot)

    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch()
