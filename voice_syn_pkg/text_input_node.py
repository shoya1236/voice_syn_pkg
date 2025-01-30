import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TextInputNode(Node):
    def __init__(self):
        super().__init__('text_input_node')
        
        # recognized_text トピックにメッセージを送信するためのパブリッシャー
        self.recognized_text_publisher = self.create_publisher(String, 'recognized_text', 10)

        # ユーザーからの入力を促す
        self.get_logger().info("Please enter text and press Enter to send:")
        self.input_loop()

    def input_loop(self):
        # ユーザーの入力を繰り返し受け付ける
        while rclpy.ok():
            user_input = input("Enter text: ")
            if user_input.lower() == 'exit':  # 'exit' でループを終了
                break
            
            # 入力されたテキストを recognized_text トピックにパブリッシュ
            msg = String()
            msg.data = user_input
            self.recognized_text_publisher.publish(msg)
            self.get_logger().info(f"Published to 'recognized_text': {user_input}")

def main(args=None):
    rclpy.init(args=args)
    text_input_node = TextInputNode()
    rclpy.spin(text_input_node)

if __name__ == '__main__':
    main()
