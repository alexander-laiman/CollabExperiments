#!/usr/bin/env python3
"""
Advanced MCAP file parser for HWC-TEST-1-MINUTE dataset
Extracts and processes different sensor data types
"""

import sys
import json
import numpy as np
from datetime import datetime
from mcap.reader import make_reader

class HWCDataParser:
    def __init__(self, mcap_path):
        self.mcap_path = mcap_path
        self.data = {
            'audio': [],
            'depth': [],
            'pose': [],
            'imu': [],
            'cameras': {'left': [], 'center': [], 'right': [], 'picture': []},
            'hands': {'left': [], 'right': []},
            'narrations': []
        }
        
    def parse(self):
        """Parse the MCAP file and extract all sensor data"""
        print(f"Parsing MCAP file: {self.mcap_path}")
        
        with open(self.mcap_path, "rb") as f:
            reader = make_reader(f)
            
            for schema, channel, message in reader.iter_messages():
                self._process_message(channel.topic, message, schema)
        
        self._print_summary()
        return self.data
    
    def _process_message(self, topic, message, schema):
        """Process individual messages based on topic"""
        timestamp = message.log_time
        
        if topic == "/ml2/audio/mic":
            self.data['audio'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/depth":
            self.data['depth'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/head/pose":
            self.data['pose'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/imu":
            self.data['imu'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/rgb/left":
            self.data['cameras']['left'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/rgb/center":
            self.data['cameras']['center'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/rgb/right":
            self.data['cameras']['right'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/rgb/picture":
            self.data['cameras']['picture'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/hands/left":
            self.data['hands']['left'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/hands/right":
            self.data['hands']['right'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
            
        elif topic == "/ml2/annotations/narrations":
            self.data['narrations'].append({
                'timestamp': timestamp,
                'data': message.data,
                'size': len(message.data)
            })
    
    def _print_summary(self):
        """Print summary of extracted data"""
        print("\nData Summary:")
        print("=" * 50)
        
        print(f"Audio messages: {len(self.data['audio'])}")
        print(f"Depth messages: {len(self.data['depth'])}")
        print(f"Pose messages: {len(self.data['pose'])}")
        print(f"IMU messages: {len(self.data['imu'])}")
        
        print("\nCamera messages:")
        for camera, messages in self.data['cameras'].items():
            print(f"  {camera}: {len(messages)}")
        
        print("\nHand tracking:")
        for hand, messages in self.data['hands'].items():
            print(f"  {hand}: {len(messages)}")
        
        print(f"\nNarrations: {len(self.data['narrations'])}")
    
    def get_topic_info(self):
        """Get information about all topics in the MCAP file"""
        topic_info = {}
        
        with open(self.mcap_path, "rb") as f:
            reader = make_reader(f)
            
            for schema, channel, message in reader.iter_messages():
                topic = channel.topic
                if topic not in topic_info:
                    topic_info[topic] = {
                        'schema': schema.name if schema else 'Unknown',
                        'message_type': schema.encoding if schema else 'Unknown',
                        'first_timestamp': message.log_time,
                        'last_timestamp': message.log_time,
                        'count': 0
                    }
                else:
                    topic_info[topic]['last_timestamp'] = message.log_time
                    topic_info[topic]['count'] += 1
        
        return topic_info

def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_mcap_advanced.py <path_to_mcap_file>")
        sys.exit(1)
    
    mcap_path = sys.argv[1]
    parser = HWCDataParser(mcap_path)
    
    # Get topic information
    print("Topic Information:")
    print("=" * 50)
    topic_info = parser.get_topic_info()
    for topic, info in sorted(topic_info.items()):
        duration = (info['last_timestamp'] - info['first_timestamp']) / 1e9
        print(f"{topic}:")
        print(f"  Schema: {info['schema']}")
        print(f"  Messages: {info['count']}")
        print(f"  Duration: {duration:.2f}s")
        print()
    
    # Parse the data
    data = parser.parse()

if __name__ == "__main__":
    main()
