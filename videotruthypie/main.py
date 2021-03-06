import numpy as np
import argparse
import glob
import cv2
import os

# Because mac is doggy doo doo
NAUTY_WORDS = ['.DS_Store']

# How many frames to skip, 2 = every other, 3 = every third etc.
PROCESS_EVERY_N_FRAME = 2

def play_video(file):
    print("Playing:", file)

    # Setup our data
    videoData = np.zeros((0,), dtype=str)

    # Temp hack, set file name for first row
    videoData = np.append(videoData, [file])

    # load video capture from file
    video = cv2.VideoCapture(file)

    # get metadata
    width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # window name and size
    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)

    # Get number of frames
    frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    while video.isOpened():
        frameNumber = video.get(cv2.CAP_PROP_POS_FRAMES)

        # Read video capture
        ret, frame = video.read()

        # Ensure we have video left to play
        if not ret:
            break

        # Only Process every n frames
        if frameNumber % PROCESS_EVERY_N_FRAME == 0:
            # Draw UI
            cv2.putText(frame, "Frame " + str(int(frameNumber)) + " (" + str(int((frameNumber / frameCount) * 100)) + "%)", (0, height - 5), cv2.FONT_HERSHEY_SIMPLEX, height / 400, (255, 255, 255))

            # Display each frame
            cv2.imshow("video", frame)
            
            # show one frame at a time
            key = cv2.waitKey(0)
            while key not in [ord('q'), ord('a'), ord('s'), ord('d'), ord('f'), ord('g'), ord('h'), ord('j'), ord('k'), ord('l'), ord(':')]:
                key = cv2.waitKey(0)

            # Quit when 'q' is pressed
            if key == ord('q'):
                break

            # ? Frame
            if key == ord('a'):
                videoData = np.append(videoData, [0])
            
            # ? Frame
            if key == ord('s'):
                videoData = np.append(videoData, [1])

            # ? Frame
            if key == ord('d'):
                videoData = np.append(videoData, [2])

            # ? Frame
            if key == ord('f'):
                videoData = np.append(videoData, [3])

            # ? Frame
            if key == ord('g'):
                videoData = np.append(videoData, [4])

            # ? Frame
            if key == ord('h'):
                videoData = np.append(videoData, [5])

            # ? Frame
            if key == ord('j'):
                videoData = np.append(videoData, [6])

            # ? Frame
            if key == ord('k'):
                videoData = np.append(videoData, [7])

            # ? Frame
            if key == ord('l'):
                videoData = np.append(videoData, [8])

            # ? Frame
            if key == ord(':'):
                videoData = np.append(videoData, [9])

    # Release capture object
    video.release()

    # Exit and distroy all windows
    cv2.destroyAllWindows()

    # Show and return the beautiful data
    print(videoData)
    return videoData

def start():
    # Get options from user
    parser = argparse.ArgumentParser(description='Kaylas Magic Video Truthy Pie, made fresh every morning with love!')
    parser.add_argument('assets', type=str, help='Glob pattern for assets location')
    parser.add_argument('--output', dest='output', default="./output.csv", help='where to save data (default: ./output.csv)')
    args = parser.parse_args()

    # Find all files in glob path
    filenames = glob.glob(args.assets)

    # Remove garbage
    safeFilenames = [word for word in filenames if word not in NAUTY_WORDS]

    # Setup our data
    data = []

    # Loop over each and play the video
    for path in safeFilenames:
        videoData = play_video(path)
        data.append(videoData.tolist())

    # We determine the max length of frames in any of the videos
    rowLengths = []
    for row in data:
        rowLengths.append(len(row))
    maxLength = max(rowLengths)

    # Then "pad" the remaining data so that we have a "balanced" matrix
    for row in data:
        while len(row) < maxLength:
            row.append('')
    balancedArray = np.array(data)

    # Transpose so that each column is a video
    finalData = balancedArray.transpose()

    # Save the beautiful data
    np.savetxt(args.output, finalData, fmt="%s", delimiter=",")
