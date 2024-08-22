import csv
import glob
import os
from datetime import datetime
import bisect

filename = "/home/pablo/Desktop/TuMag/ObservationCampaign/ls-lR.TumagAll.txt"

data_main_folder = "/work/obs/TuMAG_data"
keyword = "-rw-r--r--."

def get_time(name, format='%Y_%m_%d_%H_%M_%S'):
    return datetime.strptime(name, format)

def find_closest_folder(filename, folders, folders_timestamps):

    filename_ts = get_time(filename[:19])
    index = bisect.bisect_left(folders_timestamps, filename_ts) 

    if index > 0:
        return folders[index - 1]
    else:
        raise Exception("No pude encontrar carpeta", filename, folders)

day_folders = sorted(os.listdir(data_main_folder))
day_folders = [x for x in day_folders if os.path.isdir(f"{data_main_folder}/{x}")]
day_folders_timestamps = [get_time(fold[:19]) for fold in day_folders]

csvfile = open("Organized_files/D09.csv", 'w', newline='')
csv_writer = csv.writer(csvfile)

day = "09"
counter = 0
for folder in day_folders:
    print(f"Organizing folder: {folder}")
    
    timestamp = get_time(folder[:19])
    folder_day = folder[8:10]
    print(f"Detected day: {folder_day}")

    if folder_day != day:
        csvfile.close()
        day = folder_day
        print(f"Creating file: 'Organized_files/D{day}.csv'") 
        csvfile = open(f"Organized_files/D{day}.csv", 'w', newline='')
        csv_writer = csv.writer(csvfile)
        counter = 0
    
    hour_folders = sorted(os.listdir(f"{data_main_folder}/{folder}"))
    hour_folders = [x for x in hour_folders if os.path.isdir(f"{data_main_folder}/{folder}/{x}")]

    for hour_fold in hour_folders:

        all_files = sorted(glob.glob(f"{data_main_folder}/{folder}/{hour_fold}/*img"))
        for file in all_files:
            csv_writer.writerow([counter, file])
            counter += 1
        print(counter)


"""
with open(filename, "r") as file, open(first_csv, 'w', newline='') as csvfile:

    csv_writer = csv.writer(csvfile)
    counter = 0
    
    for line in file:
        # Split the line by spaces
        elements = line.strip().split()
        
        if len(elements) > 0:
            # Check if the first element matches the keyword
            if elements[0] == keyword and elements[-1][-3:] == "img":
                if elements[6] == day:
                    # Write the elements as a new row in the CSV file
                    day_folder = find_closest_folder(elements[-1], day_folders, day_folders_timestamps)
                    hour_folders = sorted(os.listdir(f"{data_main_folder}/{day_folder}/"))
                    hour_folders_timestamps = [get_time(fold[:19]) for fold in hour_folders]
                    hour_folder = find_closest_folder(elements[-1], hour_folders, hour_folders_timestamps)
                    csv_writer.writerow([counter, f"{day_folder}/{hour_folder}/{elements[-1]}"])
                    counter += 1
                else:
                    csvfile.close()
                    day = f"{elements[6]}"
                    csvfile = open(f"Organized_files/D{day}.csv", 'w', newline='')
                    csv_writer = csv.writer(csvfile)
                    counter = 0

                    day_folder = find_closest_folder(elements[-1], day_folders, day_folders_timestamps)
                    hour_folders = sorted(os.listdir(f"{data_main_folder}/{day_folder}/"))
                    hour_folders_timestamps = [get_time(fold[:19]) for fold in hour_folders]
                    hour_folder = find_closest_folder(elements[-1], hour_folders, hour_folders_timestamps)
                    csv_writer.writerow([counter, f"{day_folder}/{hour_folder}/{elements[-1]}"])
                    counter += 1
            
        else:
            pass

        print(counter)
        if day == "11" and counter == 50:
            break
     

file.close
"""
