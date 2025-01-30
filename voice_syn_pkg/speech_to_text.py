import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import whisper
import wave
import pyaudio

class SpeechToTextNode(Node):
    def __init__(self):
        super().__init__('speech_to_text_node')
        self.publisher_ = self.create_publisher(String, 'recognized_text', 10)
        self.whisper_model = whisper.load_model("base")

        # オーディオの設定
        self.chunk = 1024  # 音声のチャンクサイズ
        self.sample_format = pyaudio.paInt16  # 音声のフォーマット
        self.channels = 1  # モノラル
        self.fs = 16000  # サンプリングレート

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.sample_format,
                                      channels=self.channels,
                                      rate=self.fs,
                                      frames_per_buffer=self.chunk,
                                      input=True)

    def listen_and_transcribe(self):
        self.get_logger().info("Listening...")
        frames = []
        for _ in range(0, int(self.fs / self.chunk * 5)):  # 5秒間録音
            data = self.stream.read(self.chunk)
            frames.append(data)
        self.stream.stop_stream()

        # 音声データを output.wav に保存
        with wave.open('output.wav', 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(frames))

        # Whisper で音声認識
        result = self.whisper_model.transcribe('output.wav')
        recognized_text = result['text']
        
        # テキストを ROS トピックで送信
        msg = String()
        msg.data = recognized_text
        self.publisher_.publish(msg)
        self.get_logger().info(f"Recognized Text: {recognized_text}")

def main(args=None):
    rclpy.init(args=args)
    speech_to_text_node = SpeechToTextNode()
    
    # ループして音声を聞き続ける
    while rclpy.ok():
        speech_to_text_node.listen_and_transcribe()
        rclpy.spin_once(speech_to_text_node)

if __name__ == '__main__':
    main()
