# Combines all .mp4 files into a single .mp4 file
# Requires ffmpeg to be installed
import os
import pathlib

def list_file(folder_path: str):
    """
        Generates a .txt file that contains the 
        path of all the files in the folder_path.
        Will only include .mp4 files
    """
    rootdir = os.getcwd()

    # Change dir to folder_path
    os.chdir(folder_path)

    files = filter(os.path.isfile, os.listdir(folder_path))
    files = [folder_path + '/' + f for f in files]

    # Sort files by date created (from oldest to newest)
    files.sort(key=lambda x: os.path.getmtime(x))

    # Change dir back to current directory
    os.chdir(rootdir)

    with open("list.txt", "w") as f:
        for file in files:
            if file.endswith(".mp4"):
                f.write("file " + file + "\n")

def draw_text(path):
    """
        Creates a folder with all the videos from the path,
        but with the filename drawn to the video, excluding
        the file extension. list.txt also has to be recreated
        with the updated filenames.
    """
    try:
        filelist = [f for f in os.listdir('text') if f.endswith('.mp4')]
        for f in filelist:
            os.remove(os.path.join('text', f))
    except:
        # Means there is no dir named text/, so we create one
        os.mkdir("text")

    with open("list.txt") as f:
        for line in f:
            filename = line.split()[1]
            videoname = filename.split('/')[-1].replace(".mp4", "")
            os.system(f'ffmpeg -i "{filename}" -vf "drawtext=fontfile=\'C\\:/Windows/Fonts/Arial.ttf\':text=\'{videoname}\':x=10:y=10:fontsize=48:fontcolor=white" -codec:a copy "text/{videoname}_text.mp4"')

    list_file(path + "/text")

def concat():
    """
        Stitches the videos by making a system call with ffmpeg
    """
    # Change this to the path of your videos
    path = "C:/Users/JohnnyB/coding/scripts/video"

    # If out.mp4 exists, delete it
    if os.path.exists("out.mp4"):
        os.remove("out.mp4")

    # Generate .txt list file
    list_file(path)

    create_text = input("Would you like to draw the filename onto the video? [y/n] ")

    # Create videos with text overlay 
    # If ran, will take quite some time depending on the amount of input
    if create_text.lower() == 'y':
        draw_text(path)

    os.system("ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4")
    
    # Confirm the video was created
    if os.path.exists("out.mp4"):
        return True
    else:
        return False

def main():
    success = concat()

    if success:
        print("Video created successfully!")
    else:
        print("ERROR: Video was not created...")

if __name__ == '__main__':
    main()