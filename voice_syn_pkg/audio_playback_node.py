import rclpy
from rclpy.node import Node
import wave
import pyaudio
import os

class AudioPlaybackNode(Node):
    def __init__(self):
        super().__init__('audio_playback_node')

    def play_audio(self, filename):
        with wave.open(filename, 'rb') as wf:
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            data = wf.readframes(1024)
            while data:
                stream.write(data)
                data = wf.readframes(1024)

            stream.stop_stream()
            stream.close()
            p.terminate()

def main(args=None):
    rclpy.init(args=args)
    audio_playback_node = AudioPlaybackNode()

    file_path = os.path.expanduser("~/voice_syn_ws/output.wav")
    if not os.path.exists(file_path):
        audio_playback_node.get_logger().error(f"Audio file not found: {file_path}")
        return

    audio_playback_node.play_audio(file_path)
    rclpy.spin(audio_playback_node)

if __name__ == '__main__':
    main()