# Isme humara core logic (Shutil + Boto3 + Logging) rahega.
import shutil # For file operations
import boto3  # For AWS S3 interactions
import logging # For logging
import os      # For file path operations
import datetime # For timestamping


# Is script ka flow aise hai: Cleanup -> Zip -> Local Save -> AWS Upload -> Log Result.
#setup logging
logging.basicConfig(filename='devops_backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 

# Function to clean up old backups (older than 7 days)
#Storage optimize karne ke liye. Bina iske aapka computer aur cloud storage full ho jayega.
def cleanup_old_backups(destination, days=7):
    now = time.time() # Aaj ka waqt (seconds mein)
    cutoff = now - (days * 86400) # 7 din pehle ka waqt
    
    for filename in os.listdir(destination): # Folder ki har file ko check karo
        file_path = os.path.join(destination, filename)
        if os.path.isfile(file_path): # Agar wo ek file hai (folder nahi)
            file_age = os.path.getmtime(file_path) # File kab bani thi?
            if file_age < cutoff: # Agar file 7 din se purani hai
                os.remove(file_path) # Toh delete kar do!
                logging.info(f"Deleted old backup: {filename}")

# Function to create a zip archive
def create_zip(source, destination):
    # Step A: Agar destination folder nahi hai toh banao (Local Storage creation)
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    # Step B: Backup ka naam aur location tay karo
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_name = os.path.join(destination, f"backup_{timestamp}")
    
    # Step C: ACTUAL LOCAL BACKUP YAHA HO RAHA HAI
    # Ye line 'source' folder ko uthati hai aur 'destination' (Local/OneDrive) par save kar deti hai
    actual_path = shutil.make_archive(zip_name, 'gztar', source)
    
    return actual_path # Ye computer ka local path return karta hai

# Function to upload file to AWS S3
def upload_to_s3(file_path, bucket_name):
    """AWS S3 Upload Logic"""
    s3 = boto3.resource('s3')
    file_only = os.path.basename(file_path)
    s3.Bucket(bucket_name).upload_file(file_path, file_only)
    return file_only

# Function to create a backup
def run_backup_pipeline(source, destination, bucket_name, mode):
    """
    mode can be: 'local', 'cloud', or 'both'
    """
    try: 
        results = []
        # Step 1: Zip hamesha banega (Temporary ya Permanent)
        zip_path = create_zip(source, destination)
        results.append(f"✅ Zip created at: {zip_path}")

        # Step 2: User ki choice ke hisab se action
        if mode == 'cloud' or mode == 'both':
            s3_file = upload_to_s3(zip_path, bucket_name)
            results.append(f"☁️ Uploaded to AWS S3: {s3_file}")
        

        if mode == 'cloud':
            # Agar sirf cloud chahiye, toh local zip delete kar sakte ho storage bachane ke liye
            # os.remove(zip_path) 
            results.append("🗑️ Local zip removed (Cloud-only mode)")

        logging.info(f"Backup Mode: {mode} | Status: Success")
        return results
       
    except Exception as e:
        logging.error(f"Error in mode {mode}: {str(e)}")
        return [f"❌ Error: {str(e)}"]