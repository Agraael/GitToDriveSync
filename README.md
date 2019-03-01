# GitToDriveSync

GitToDrive is a python scrpit who allow to sync a git repository to a Google Drive Accout.  
It can be deployed inside a container , using the Dockerfile.

### Prerequisites

- **Python3**
- **[Drive](https://github.com/odeke-em/drive)**
- **Docker**

## Usage
```
usage: GitToDriveSync.py [-h] {credential,init,start,auto} ...

Service who connect every update to a git branch into a Google drive

positional arguments:
  {credential,init,start,auto}
    credential          getting json credential for GoogleDrive
    init                init the drive directory and pull the repo
    start               start the GitToDrive" service/server on the directory
    auto                init and start the GitToDrive service/server

optional arguments:
  -h, --help            show this help message and exit
```  
#### {credential}
```
usage: GitToDriveSync credential [-h] [--path path]
```
This command allow to retrieve the **credentials.json** file that you need to access
your Google Drive account.

- **PATH** : this allow to set the path of the credential file 

```
Visit this URL to get an authorization code
[...]
Paste the authorization code: ******************

ls
credentials.json  Dockerfile  GitToDriveSync  README.md
```
> for now the oauth2 authentification will be on your web browser

#### {init}
```
usage: usage: GitToDriveSync init [-h] (--link link | --path path) [--json json]
```
With this command you can initialize a git repository for drive.
When initialized all the folder/repository content will be uploaded in a new directory  with the same name at the root.

- **LINK** : 