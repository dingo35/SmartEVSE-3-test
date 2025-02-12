#this script will be run by platformio.ini from its native directory
import os, sys, gzip, shutil

#check for the two files we need to be able to keep updating the firmware by the /update endpoint:
if not os.path.isfile("data/update2.html"):
    print("Missing file: data/update2.html")
    sys.exit(1)
if os.path.isdir("pack.tmp"):
    shutil.rmtree("pack.tmp")
try:
    filelist = []
    os.makedirs("pack.tmp/data")
    non_gzip_files = {"cert.pem", "key.pem", "CH32V203.bin", "SmartEVSE.webp"}
    # now gzip the stuff except `non_gzip_files`:
    for file in os.listdir("data"):
        filename = os.fsdecode(file)
        if filename in non_gzip_files:
            source_path = os.path.join("data", filename)
            shutil.copy(source_path, os.path.join("pack.tmp", "data", filename))
            filelist.append(source_path)
            continue
        else:
            with open(f"data/{filename}", "rb") as f_in, gzip.open(f"pack.tmp/data/{filename}.gz", "wb") as f_out:
                f_out.writelines(f_in)
            filelist.append(f"data/{filename}.gz")
            continue
    os.chdir("pack.tmp")
    cmdstring = f"python ../pack.py {' '.join(filelist)}"
    os.system(f"{cmdstring} > ../src/packed_fs.c")
    os.chdir("..")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    sys.exit(100)
if shutil.rmtree("pack.tmp"):
    print("Failed to clean up temporary files")
    sys.exit(9)
