#!/usr/bin/env python3
"""
Basic MCAP file parser for HWC-TEST-1-MINUTE dataset
"""

import sys
import json
from mcap.reader import make_reader

def parse_mcap_basic(mcap_path):
    """Parse MCAP file and print basic information about topics and messages"""
    
    print(f"Parsing MCAP file: {mcap_path}")
    print("=" * 50)
    
    topic_counts = {}
    topic_schemas = {}
    
    with open(mcap_path, "rb") as f:
        reader = make_reader(f)
        
        # Get basic file info
        print(f"File info: {reader.get_summary()}")
        print()
        
        # Iterate through all messages
        for schema, channel, message in reader.iter_messages():
            topic = channel.topic
            
            # Count messages per topic
            if topic not in topic_counts:
                topic_counts[topic] = 0
                topic_schemas[topic] = schema.name if schema else "Unknown"
            topic_counts[topic] += 1
            
            # Print first few messages from each topic
            if topic_counts[topic] <= 3:
                print(f"Topic: {topic}")
                print(f"Schema: {schema.name if schema else 'Unknown'}")
                print(f"Timestamp: {message.log_time}")
                print(f"Data length: {len(message.data)} bytes")
                print(f"Data preview: {message.data[:100]}...")
                print("-" * 30)
    
    print("\nTopic Summary:")
    print("=" * 50)
    for topic, count in sorted(topic_counts.items()):
        print(f"{topic}: {count} messages (Schema: {topic_schemas[topic]})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_mcap_basic.py <path_to_mcap_file>")
        sys.exit(1)
    
    mcap_path = sys.argv[1]
    parse_mcap_basic(mcap_path)
