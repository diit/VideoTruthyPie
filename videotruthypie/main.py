import numpy as np
import cv2
import os

# Where the stuff is stored
ASSETS_DIRECTORY = 'assets'
OUTPUT_DIRECTORY = 'output'

# Because mac is doggy doo doo
NAUTY_WORDS = ['.DS_Store']

def play_video(folder, file):
    print("Playing:", folder, file)

    # load video capture from file
    video = cv2.VideoCapture(os.path.join(folder, file))

    # window name and size
    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)

    # Setup our data
    data = np.zeros((0,), dtype=int)

    # See what we're getting into
    frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    print("Frames:", frameCount)

    while video.isOpened():
        # Read video capture
        ret, frame = video.read()

        # Ensure we have video left to play
        if not ret:
            break

        # Display each frame
        cv2.imshow("video", frame)
        
        # show one frame at a time
        key = cv2.waitKey(0)
        while key not in [ord('q'), ord('k'), ord('l')]:
            key = cv2.waitKey(0)

        # Quit when 'q' is pressed
        if key == ord('q'):
            break

        # Record a "bad frame" when K is pressed
        if key == ord('k'):
            data = np.append(data, [0])
        
        # Record a "good frame" when L is pressed
        if key == ord('l'):
            data = np.append(data, [1])

    # Release capture object
    video.release()

    # Exit and distroy all windows
    cv2.destroyAllWindows()

    # Show the beautiful data
    print(data)

    # Save the beautiful data
    np.savetxt(os.path.join(OUTPUT_DIRECTORY, file + ".csv"), data, fmt='%i', delimiter=",")

def start():
    print("Hello Kayla!\n\n")

    # We want to loop over all videos in the assets folder
    filenames = next(os.walk(ASSETS_DIRECTORY), (None, None, []))[2]

    # Remove garbage
    safeFilenames = [word for word in filenames if word not in NAUTY_WORDS]

    # Loop over each and play the video
    for path in safeFilenames:
        play_video(ASSETS_DIRECTORY, path)
