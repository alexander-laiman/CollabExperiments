import ffmpeg
import glob
import os
import sys

def ffmpeg_video(target_dir):
    # Check if files exist
    print(f"Current working directory: {os.getcwd()}")
    print(f"Target directory: {target_dir}")
    png_files = sorted(glob.glob(os.path.join(target_dir, '*.png')))
    
    if not png_files:
        print(f"No PNG files found in {target_dir}")
        return
    
    print(f"Found {len(png_files)} PNG files")
    
    try:
        (
            ffmpeg
            .input(('./'+target_dir[2:-1] + '/%04d.png'), pattern_type='sequence', framerate=15)
            .output(f'{target_dir}.avi', vcodec='rawvideo')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f"Video created successfully: {target_dir}.avi")
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Pass in directory to parse <path_to_png's>")
        sys.exit(1)
    
    target = sys.argv[1]
    ffmpeg_video(target)
