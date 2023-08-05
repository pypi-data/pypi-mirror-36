# Docx to Google Drive uploader for Foliant

Gdoc is an extension of Pandoc backend, it's used to upload created docx documents to Google Drive.

Gdoc adds `gdoc` target to Foliant.


## Installation

```shell
$ pip install foliantcontrib.gdoc
```


## Config

To enable the backend, add `gdoc` to `backend_config` section in the project config. As `gdoc` needs *docx* to upload, `pandoc` settings also have to be here.

Backend has a number of options (all fields are required but can have no values):

```yaml
backend_config:
    pandoc:
        ...
    gdoc:
        gdrive_folder_name: Foliant upload
        gdrive_folder_id:
        gdoc_title:
        gdoc_id:
        under_docker: false
```

`gdrive_folder_name`
:   Folder with this name will be created on Google Drive to upload file.

`gdrive_folder_id`
:   This field is necessary to upload files to previously created folder.

`gdoc_title`
:   Uploaded file will have this title. If empty, real filename will be used.

`gdoc_id`
:   This field is necessary to rewrite previously uploaded file and keep the link to it.


## Usage

At first you have to get Google Drive authentication file.

1. Go to [APIs Console](https://console.developers.google.com/cloud-resource-manager) and make your own project.
2. Go to [library](https://console.developers.google.com/apis/library), search for ‘Google Drive API’, select the entry, and click ‘Enable’.
3. Select ‘Credentials’ from the left menu, click ‘Create Credentials’, select ‘OAuth client ID’.
4. Now, the product name and consent screen need to be set -> click ‘Configure consent screen’ and follow the instructions. Once finished:
    - Select ‘Application type’ to be *Other types*.
    - Enter an appropriate name.
    - Input http://localhost:8080 for ‘Authorized JavaScript origins’.
    - Input http://localhost:8080/ for ‘Authorized redirect URIs’.
    - Click ‘Save’.
5. Click ‘Download JSON’ on the right side of Client ID to download client_secret_<really long ID>.json. The downloaded file has all authentication information of your application.
6. Rename the file to “client_secrets.json” and place it in your working directory near foliant.yml.

Now add the backend to the project config with all settings strings. At this moment you have no data to set *Google Drive folder ID* and *google doc ID* so keep it empty.

Run Foliant with `gdoc` target:

```shell
$ foliant make gdoc
✔ Parsing config
✔ Applying preprocessor flatten
✔ Making docx with Pandoc
Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?...

Authentication successful.
─────────────────────
Result:
Doc link: https://docs.google.com/document/d/1GPvNSMJ4ZutZJwhUYM1xxCKWMU5Sg/edit?usp=drivesdk
Google drive folder ID: 1AaiWMNIYlq9639P30R3T9
Google document ID: 1GPvNSMJ4Z19YM1xCKWMU5Sg
```

Authentication form will be opened. Choose account to log in.

Under Docker authentication differs little bit:

```
$ docker-compose run --rm foliant make gdoc
✔ Parsing config
✔ Applying preprocessor flatten
✔ Making docx with Pandoc
Go to the following link in your browser:

    https://accounts.google.com/o/oauth2/auth?...

Enter verification code: 4/XgBllTXpxv8kKjsiTxLc
Authentication successful.
─────────────────────
Result:
Doc link: https://docs.google.com/document/d/1GPvNSMJ4ZutZJwhUYM1xxCKWMU5Sg/edit?usp=drivesdk
Google drive folder ID: 1AaiWMNIYlq9639P30R3T9
Google document ID: 1GPvNSMJ4Z19YM1xCKWMU5Sg
```

Copy link from terminal to your browser, choose account to log in and copy generated code back to the terminal.

After that docx will be uploaded to Google Drive in google doc format and opened in new browser tab.

Now you can use *Google Drive folder ID* to upload files to the same folder and *google doc ID* (the same as in the link) to rewrite document.

### Notes

If you set up *google doc ID* without *Google Drive folder ID* file will be moved to the new folder with the same link.
