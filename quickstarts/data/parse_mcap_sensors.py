#!/usr/bin/env python3
"""
Specialized MCAP parser for extracting and processing sensor data
from HWC-TEST-1-MINUTE dataset
"""

import sys
import json
import numpy as np
import cv2
from datetime import datetime
from mcap.reader import make_reader

class SensorDataExtractor:
    def __init__(self, mcap_path):
        self.mcap_path = mcap_path
        
    def extract_images(self, output_dir="extracted_images"):
        """Extract and save camera images"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        camera_topics = {
            "/ml2/rgb/left": "left",
            "/ml2/rgb/center": "center", 
            "/ml2/rgb/right": "right",
            "/ml2/rgb/picture": "picture"
        }
        
        image_counts = {name: 0 for name in camera_topics.values()}
        
        with open(self.mcap_path, "rb") as f:
            reader = make_reader(f)
            
            for schema, channel, message in reader.iter_messages():
                if channel.topic in camera_topics:
                    camera_name = camera_topics[channel.topic]
                    
                    # Convert raw data to image (this may need adjustment based on actual format)
                    try:
                        # Assuming the data is in a format that can be decoded
                        # You may need to adjust this based on the actual image format
                        nparr = np.frombuffer(message.data, np.uint8)
                        
                        # Try to decode as image
                        if camera_name == "picture":
                            # RGB image
                            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        else:
                            # Monochrome image
                            img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                        
                        if img is not None:
                            filename = f"{output_dir}/{camera_name}_{image_counts[camera_name]:06d}.jpg"
                            cv2.imwrite(filename, img)
                            image_counts[camera_name] += 1
                            
                    except Exception as e:
                        print(f"Error processing image from {channel.topic}: {e}")
        
        print(f"Extracted images to {output_dir}/")
        for camera, count in image_counts.items():
            print(f"  {camera}: {count} images")
    
    def extract_audio(self, output_file="extracted_audio.wav"):
        """Extract and save audio data"""
        import wave
        
        audio_data = []
        sample_rate = 16000  # From documentation
        
        with open(self.mcap_path, "rb") as f:
            reader = make_reader(f)
            
            for schema, channel, message in reader.iter_messages():
                if channel.topic == "/ml2/audio/mic":
                    audio_data.append(message.data)
        
        if audio_data:
            # Combine all audio chunks
            combined_audio = b''.join(audio_data)
            
            # Save as WAV file
            with wave.open(output_file, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(combined_audio)
            
            print(f"Extracted audio to {output_file}")
            print(f"  Duration: {len(combined_audio) / (sample_rate * 2):.2f} seconds")
        else:
            print("No audio data found")
    
    def extract_pose_data(self, output_file="pose_data.json"):
        """Extract head pose data"""
        pose_data = []
        
        with open(self.mcap_path, "rb") as f:
            reader = make_reader(f)
            
            for schema, channel, message in reader.iter_messages():
                if channel.topic == "/ml2/head/pose":
                    # Parse pose data (format may vary)
                    try:
                        # This is a placeholder - you'll need to decode based on actual format
                        pose_info = {
                            'timestamp': message.log_time,
                            'data_size': len(message.data),
                            'raw_data': message.data.hex()  # Convert to hex for inspection
                        }
                        pose_data.append(pose_info)
                    except Exception as e:
                        print(f"Error processing pose data: {e}")
        
        with open(output_file, 'w') as f:
            json.dump(pose_data, f, indent=2)
        
        print(f"Extracted pose data to {output_file}")
        print(f"  Total pose samples: {len(pose_data)}")
    
    def extract_hand_tracking(self, output_file="hand_tracking.json"):
        """Extract hand tracking data"""
        hand_data = {'left': [], 'right': []}
        
        with open(self.mcap_path, "rb") as f:
            reader = make_reader(f)
            
            for schema, channel, message in reader.iter_messages():
                if channel.topic in ["/ml2/hands/left", "/ml2/hands/right"]:
                    hand = "left" if "left" in channel.topic else "right"
                    
                    try:
                        hand_info = {
                            'timestamp': message.log_time,
                            'data_size': len(message.data),
                            'raw_data': message.data.hex()  # Convert to hex for inspection
                        }
                        hand_data[hand].append(hand_info)
                    except Exception as e:
                        print(f"Error processing hand data: {e}")
        
        with open(output_file, 'w') as f:
            json.dump(hand_data, f, indent=2)
        
        print(f"Extracted hand tracking data to {output_file}")
        print(f"  Left hand samples: {len(hand_data['left'])}")
        print(f"  Right hand samples: {len(hand_data['right'])}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_mcap_sensors.py <path_to_mcap_file>")
        sys.exit(1)
    
    mcap_path = sys.argv[1]
    extractor = SensorDataExtractor(mcap_path)
    
    print("Extracting sensor data from MCAP file...")
    print("=" * 50)
    
    # Extract different types of data
    extractor.extract_images()
    extractor.extract_audio()
    extractor.extract_pose_data()
    extractor.extract_hand_tracking()
    
    print("\nExtraction complete!")

if __name__ == "__main__":
    main()
