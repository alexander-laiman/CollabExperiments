import sys
import json
import numpy as np
import cv2
import os
from mcap.reader import make_reader

### This script is for extracting iamges into a directory. This assumes the foxglove.RawImage is some sort of protobuf file.
### Note: I've just set this up to get the mono center and rgb feeds, but you could have it check each topic.
def parse_foxglove_rawimage(data):
    """Parse Foxglove RawImage message data (Protobuf format)"""
    try:
        pos = 0
        width = None
        height = None
        encoding = None
        step = None
        raw_data = None
        
        while pos < len(data):
            if pos >= len(data):
                break
                
            # Read field tag and wire type
            tag_byte = data[pos]
            pos += 1
            
            field_number = tag_byte >> 3
            wire_type = tag_byte & 0x07
            

            if wire_type == 0:  # Varint
                value = 0
                shift = 0
                while pos < len(data):
                    byte = data[pos]
                    pos += 1
                    value |= (byte & 0x7F) << shift
                    if (byte & 0x80) == 0:
                        break
                    shift += 7
                
                if field_number == 1:  # timestamp
                    pass  # Skip timestamp
                elif field_number == 2:  # width
                    width = value
                elif field_number == 3:  # height
                    height = value
                elif field_number == 5:  # step
                    step = value
                    
            elif wire_type == 2:  # Length-delimited (string/bytes)
                # Read length
                length = 0
                shift = 0
                while pos < len(data):
                    byte = data[pos]
                    pos += 1
                    length |= (byte & 0x7F) << shift
                    if (byte & 0x80) == 0:
                        break
                    shift += 7
                                
                # Read the data
                if pos + length > len(data):
                    break
                    
                field_data = data[pos:pos + length]
                pos += length
                
                if field_number == 1:  # timestamp (nested message)
                    pass  # Skip timestamp
                elif field_number == 2:  # data (for picture stream)
                    raw_data = field_data
                elif field_number == 3:  # encoding field (for picture stream)
                    try:
                        encoding = field_data.decode('utf-8')
                    except:
                        pass
                elif field_number == 4:  # encoding
                    try:
                        encoding = field_data.decode('utf-8')
                    except:
                        pass
                elif field_number == 6:  # data (for center stream)
                    raw_data = field_data
                elif field_number == 7:  # frame_id
                    try:
                        frame_id = field_data.decode('utf-8')
                    except:
                        pass
                    
            elif wire_type == 5:  # 32-bit fixed-length
                if pos + 4 > len(data):
                    break
                    
                # Read 4 bytes as little-endian 32-bit integer
                value = int.from_bytes(data[pos:pos+4], byteorder='little')
                pos += 4
                                
                if field_number == 2:  # width
                    width = value
                elif field_number == 3:  # height
                    height = value
                elif field_number == 5:  # step
                    step = value
                    
            else:
                print(f"  Debug: Unknown wire type {wire_type}")
                break
        
        # Special handling for JPEG data - if we have raw_data but no encoding, check if it's JPEG
        if raw_data and not encoding:
            if raw_data.startswith(b'\xff\xd8\xff'):
                encoding = 'jpeg'
        
        # Also handle "picture" encoding as JPEG
        if encoding == 'picture' and raw_data and raw_data.startswith(b'\xff\xd8\xff'):
            encoding = 'jpeg'

        return width, height, encoding, step, raw_data
        
    except Exception as e:
        print(f"Error parsing Protobuf data: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None, data

def decode_image(width, height, encoding, step, raw_data):
    """Decode raw image data based on encoding"""
    if encoding == 'mono8' or encoding == '8UC1':
        # Monochrome 8-bit
        image = np.frombuffer(raw_data, dtype=np.uint8)
        image = image.reshape((height, width))
        # Flip vertically to correct orientation
        image = cv2.flip(image, 0)
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    elif encoding == 'jpeg' or encoding == 'jpg':
        # JPEG compressed image
        try:
            nparr = np.frombuffer(raw_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # Note: JPEG images are already correctly oriented, no flip needed
            return image
        except Exception as e:
            print(f"Error decoding JPEG: {e}")
            return None
        
    else:
        print(f"Unsupported encoding: {encoding}")
        return None

def main():
    if len(sys.argv) <2:
        print("Usage: No MCAP file passed. Call as python extract-images-foxglove.py <path_to_mcap_file>")
        sys.exit(1)
    
    mcap_path = sys.argv[1]
    print(f"Parsing MCAP file: {mcap_path}")
    print("Looking for Foxglove RawImage messages on /ml2/rgb/center topic...")
    


    def extract_images(topic_name):
        # Create images directory
        topic_clean = topic_name.replace("/", "-").replace("ml2", "ml2")  # ml2-rgb-center
        images_dir = topic_clean
        os.makedirs(images_dir, exist_ok=True)
        print(f"Created directory: {images_dir}")
        
        with open(mcap_path, "rb") as f:
            reader = make_reader(f)
            
            for index, (schema, channel, message) in enumerate(reader.iter_messages(topics=[topic_name])):
                
                # Parse the RawImage data
                width, height, encoding, step, raw_data = parse_foxglove_rawimage(message.data)
                
                # For JPEG, we can decode even without width/height since JPEG contains its own dimensions
                if (width is not None and height is not None) or encoding == 'jpeg':                   
                    # Decode the image
                    image = decode_image(width, height, encoding, step, raw_data)
                    
                    if image is not None:
                        # Save as PNG with meaningful filename in images directory
                        output_file = os.path.join(images_dir, f"{topic_clean}-{index:02d}.png")
                        cv2.imwrite(output_file, image)
                        
                    else:
                        print("  Failed to decode image")
                else:
                    print("  Failed to parse RawImage data")
                    print(f"  Raw data preview: {message.data[:50].hex()}")
        
            # Only process the first message
            # break
        # Calculate framerate from the extracted data to sanity check
        print(f"\n=== Framerate Analysis ===")
        if index > 1:
            # Get first and last timestamps
            timestamps = []
            with open(mcap_path, "rb") as f:
                reader = make_reader(f)
                for schema, channel, message in reader.iter_messages(topics=[topic_name]):
                    timestamps.append(message.log_time)
            
            if len(timestamps) > 1:
                duration_ns = timestamps[-1] - timestamps[0]
                duration_s = duration_ns / 1e9
                framerate = len(timestamps) / duration_s
                
                print(f"Total images: {len(timestamps)}")
                print(f"Duration: {duration_s:.2f} seconds")
                print(f"Calculated framerate: {framerate:.2f} fps")
                
                # Also check the dataset documentation framerate
                print(f"Expected framerate (from README): ~15 Hz")
                print(f"Difference: {abs(framerate - 15):.2f} fps")
    # Extract topic name for filename
    topic_name = "/ml2/rgb/center"
    extract_images(topic_name)
    topic_name = "/ml2/rgb/picture"
    extract_images(topic_name)
    
if __name__ == "__main__":
    main()