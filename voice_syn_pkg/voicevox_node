import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests

class VoiceVoxNode(Node):
    def __init__(self):
        super().__init__('voicevox_node')
        self.subscription = self.create_subscription(
            String,
            'generated_response',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        generated_response = msg.data
        self.get_logger().info(f"Received response: {generated_response}")

        # VoiceVox API を使って音声合成
        voicevox_url = "http://localhost:50021/synthesis"
        params = {
            "text": generated_response,
            "speaker": 1  # スピーカーID
        }

        response = requests.post(voicevox_url, params=params)

        if response.status_code == 200:
            with open('output.wav', 'wb') as f:
                f.write(response.content)
            self.get_logger().info("VoiceVox synthesis completed.")
        else:
            self.get_logger().error("VoiceVox synthesis failed.")

def main(args=None):
    rclpy.init(args=args)
    voicevox_node = VoiceVoxNode()
    rclpy.spin(voicevox_node)

if __name__ == '__main__':
    main()
