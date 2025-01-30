import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai

class ChatGPTNode(Node):
    def __init__(self):
        super().__init__('chatgpt_node')
        self.subscription = self.create_subscription(
            String,
            'recognized_text',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(String, 'generated_response', 10)

        # OpenAI APIキーの設定
        openai.api_key = 'YOUR_OPENAI_API_KEY'

    def listener_callback(self, msg):
        recognized_text = msg.data
        self.get_logger().info(f"Received text: {recognized_text}")

        # ChatGPT に問い合わせて応答を生成
        response = openai.chat_completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": recognized_text}],
            max_tokens=150
        )
        generated_response = response['choices'][0]['message']['content'].strip()

        # 応答を ROS トピックで送信
        msg = String()
        msg.data = generated_response
        self.publisher_.publish(msg)
        self.get_logger().info(f"Generated Response: {generated_response}")

def main(args=None):
    rclpy.init(args=args)
    chatgpt_node = ChatGPTNode()
    rclpy.spin(chatgpt_node)

if __name__ == '__main__':
    main()
