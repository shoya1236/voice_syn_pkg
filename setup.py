from setuptools import find_packages, setup

package_name = 'voice_syn_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shoya',
    maintainer_email='shoya.yam@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'speech_to_text = voice_syn.speech_to_text:main',
            'chatgpt_node = voice_syn.chatgpt_node:main',
            'voicevox_node = voice_syn.voicevox_node:main',
            'audio_playback_node = voice_syn.audio_playback_node:main',
        ],
    },
)
