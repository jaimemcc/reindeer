import argparse
from pathlib import Path
import os
import sys
import cv2
import pytesseract
from datetime import datetime
import subprocess

pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\jmc010\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

def get_newfilename(frame, cam_number, outputfolder):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_reduced = gray_frame[1040:,1610:]
    
    time_str = pytesseract.image_to_string(gray_frame_reduced)
    datetime_obj = datetime.strptime(time_str.strip(), '%m/%d/%Y %I:%M%p')
    formatted_date = datetime_obj.strftime('%Y-%m-%d_%H%M')
    
    # need to check if already a file and if so add suffix

    newfilename = outputfolder / f"{formatted_date}_{cam_number}.MP4"
    return newfilename

def resize_video(filename, scale, cam_number, outputfolder=None):
    if outputfolder is None:
            outputfolder = filename.parent
    
    cap = cv2.VideoCapture(filename)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    
    # Read the first frame
    ret, frame = cap.read()
    cap.release()

    x = frame.shape[1]
    newx = int(x * scale)

    newfilename = get_newfilename(frame, cam_number, outputfolder)
    inputfile = str(filename).replace('\\', '/')
    outputfile = str(newfilename).replace('\\', '/')

    command = f"ffmpeg -i {inputfile} -vf scale={newx}:-1 {outputfile}"
    print("Running", command)
    
    subprocess.run(command, shell=True)
    cap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize a video and save it with a new filename.")
    parser.add_argument("-f", "--filename", type=str, help="Path to the input video file.")
    parser.add_argument("-d", "--directory", type=str, help="Path to the input video file.")
    parser.add_argument("-s", "--scale", type=float, help="Scale factor for resizing the video.")
    parser.add_argument("-c", "--cam_number", type=int, help="Camera number to include in the output filename.")
    parser.add_argument("-o-", "--outputfolder", type=str, help="Path to the output folder.", default=None)

    args = parser.parse_args()
     
    if args.scale is None:
        scale = 0.5
    else:
        scale = args.scale
        
    if args.cam_number is None:
        cam_number = "default"
    else:
        cam_number = args.cam_number
        
    if args.filename is None and args.directory is None:
        print("Error: You must provide a filename or directory. Exiting.")
        sys.exit()
    elif args.filename is not None and args.directory is not None:
        print("Error: You cannot provide both a filename and a directory. Exiting.")
        sys.exit()
    
    if args.filename is not None:
        filename = Path(args.filename)
        outputfolder = Path(args.outputfolder) if args.outputfolder else None
        
        resize_video(Path(filename), scale, cam_number, outputfolder)
        print("Done.")
        sys.exit()
    
    if args.directory is not None:
        print("using directory")
        directory = Path(args.directory)
        outputfolder = Path(args.outputfolder) if args.outputfolder else None
        
        for file in directory.glob("*.MP4"):
            resize_video(file, scale, cam_number, outputfolder)
        print("Done.")
        sys.exit()
    
    print("hay")
        

    