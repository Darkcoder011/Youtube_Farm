"""
Google Drive uploader module for uploading generated content to Drive and YouTube.
"""
import os
import json
import requests
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from google.oauth2 import service_account

# Parent folder ID for "Self" in Google Drive
PARENT_FOLDER_ID = "11BoyAH1HwU2an_2w39l2TF0-Sj3KgJ-H"
SERVICE_ACCOUNT_URL = "https://drive.google.com/file/d/1NC0n-j3Wrp7mWpSOodC7zupwLCeVcSsj/view?usp=sharing"

def download_service_account(url, save_path):
    """
    Download the service account JSON file from Google Drive.
    
    Args:
        url (str): The Google Drive sharing URL for the service account JSON
        save_path (str): Path to save the service account JSON file
        
    Returns:
        str: Path to the downloaded service account JSON file or None if failed
    """
    try:
        # Convert sharing URL to direct download link
        file_id = url.split("/d/")[1].split("/view")[0]
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        # Download the file
        print(f"Downloading service account credentials...")
        response = requests.get(download_url)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Service account credentials downloaded to {save_path}")
            return save_path
        else:
            print(f"❌ Failed to download service account. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error downloading service account: {str(e)}")
        return None

def get_drive_service(credentials_path):
    """
    Initialize and return a Google Drive API service using service account credentials.
    
    Args:
        credentials_path (str): Path to the service account credentials JSON file
        
    Returns:
        object: Google Drive API service or None if initialization failed
    """
    try:
        # Load credentials from the service account file
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, 
            scopes=['https://www.googleapis.com/auth/drive']
        )
        
        # Build the Drive API service
        service = build('drive', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"❌ Error initializing Drive service: {str(e)}")
        return None

def create_folder(service, folder_name, parent_folder_id=None):
    """
    Create a folder in Google Drive.
    
    Args:
        service: Google Drive API service
        folder_name (str): Name of the folder to create
        parent_folder_id (str, optional): ID of the parent folder
        
    Returns:
        str: ID of the created folder or None if failed
    """
    try:
        # Folder metadata
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        # If parent folder is specified, add it to metadata
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
        
        # Create the folder
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f"✅ Created folder: {folder_name} (ID: {folder['id']})")
        return folder['id']
    except Exception as e:
        print(f"❌ Error creating folder '{folder_name}': {str(e)}")
        return None

def upload_file(service, file_path, folder_id, filename=None):
    """
    Upload a file to a specific folder in Google Drive.
    
    Args:
        service: Google Drive API service
        file_path (str): Path to the file to upload
        folder_id (str): ID of the folder to upload to
        filename (str, optional): Custom filename to use (if different from original)
        
    Returns:
        str: ID of the uploaded file or None if failed
    """
    try:
        # If custom filename is not provided, use the original filename
        if not filename:
            filename = os.path.basename(file_path)
        
        # File metadata
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        
        # Create media
        media = MediaFileUpload(file_path, resumable=True)
        
        # Upload the file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f"✅ Uploaded: {filename} (ID: {file['id']})")
        return file['id']
    except Exception as e:
        print(f"❌ Error uploading {file_path}: {str(e)}")
        return None

def upload_text_content(service, content, filename, folder_id):
    """
    Upload text content directly to Google Drive without creating a local file.
    
    Args:
        service: Google Drive API service
        content (str): Text content to upload
        filename (str): Filename to save as
        folder_id (str): ID of the folder to upload to
        
    Returns:
        str: ID of the uploaded file or None if failed
    """
    try:
        # File metadata
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        
        # Create media from text content
        media = MediaIoBaseUpload(
            io.BytesIO(content.encode('utf-8')),
            mimetype='text/plain',
            resumable=True
        )
        
        # Upload the file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f"✅ Uploaded text content as: {filename} (ID: {file['id']})")
        return file['id']
    except Exception as e:
        print(f"❌ Error uploading text content as {filename}: {str(e)}")
        return None

def get_next_folder_number(service, parent_folder_id):
    """
    Get the next sequential folder number to create.
    
    Args:
        service: Google Drive API service
        parent_folder_id (str): ID of the parent folder
        
    Returns:
        int: Next folder number to use
    """
    try:
        # List all folders in the parent folder
        results = service.files().list(
            q=f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
            fields="files(name)"
        ).execute()
        
        folders = results.get('files', [])
        
        # Extract numeric parts from folder names (assuming format like "Video_001")
        folder_numbers = []
        for folder in folders:
            parts = folder['name'].split('_')
            if len(parts) > 1 and parts[1].isdigit():
                folder_numbers.append(int(parts[1]))
        
        # If no folders exist yet, start with 1, otherwise use the next number
        if not folder_numbers:
            return 1
        else:
            return max(folder_numbers) + 1
    except Exception as e:
        print(f"❌ Error getting next folder number: {str(e)}")
        # Default to a timestamp-based number if we can't determine the sequence
        import time
        return int(time.time()) % 1000  # Use last 3 digits of current timestamp

def upload_video_with_metadata(video_path, title, description, tags, thumbnail_path=None):
    """
    Upload a video and its metadata to Google Drive in a structured folder.
    
    Args:
        video_path (str): Path to the video file
        title (str): Video title
        description (str): Video description
        tags (list): List of tags for the video
        thumbnail_path (str, optional): Path to the thumbnail image
        
    Returns:
        str: ID of the folder containing the uploaded content or None if failed
    """
    try:
        # Setup paths
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        credentials_dir = os.path.join(base_dir, "credentials")
        os.makedirs(credentials_dir, exist_ok=True)
        credentials_path = os.path.join(credentials_dir, "service_account.json")
        
        # Download service account if needed
        if not os.path.exists(credentials_path):
            credentials_path = download_service_account(SERVICE_ACCOUNT_URL, credentials_path)
            if not credentials_path:
                return None
        
        # Initialize Drive service
        service = get_drive_service(credentials_path)
        if not service:
            return None
        
        # Get next folder number and create folder name
        next_number = get_next_folder_number(service, PARENT_FOLDER_ID)
        folder_name = f"Video_{next_number:03d}"
        
        # Create folder for this video
        folder_id = create_folder(service, folder_name, PARENT_FOLDER_ID)
        if not folder_id:
            return None
        
        # Upload video file
        video_id = upload_file(service, video_path, folder_id)
        if not video_id:
            print("⚠️ Video upload failed, but continuing with metadata...")
        
        # Upload metadata files
        
        # 1. Title
        title_id = upload_text_content(service, title, "title.txt", folder_id)
        
        # 2. Description
        desc_id = upload_text_content(service, description, "description.txt", folder_id)
        
        # 3. Tags (join the list with commas)
        tags_text = ",".join(tags) if isinstance(tags, list) else tags
        tags_id = upload_text_content(service, tags_text, "tags.txt", folder_id)
        
        # 4. Thumbnail (if provided)
        if thumbnail_path and os.path.exists(thumbnail_path):
            thumb_id = upload_file(service, thumbnail_path, folder_id)
        
        print(f"✅ Successfully uploaded video and metadata to folder: {folder_name}")
        return folder_id
    
    except Exception as e:
        print(f"❌ Error in uploading video with metadata: {str(e)}")
        return None
