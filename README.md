[![GuardRails badge](https://badges.production.guardrails.io/Agraael/GitToDriveSync.svg?token=34fda599487d2fa333dec9761e50e5885ab4ab7ddfa4dd0b8dd0a080f9b86dc3)](https://dashboard.guardrails.io/default/gh/Agraael/GitToDriveSync)
# GitToDriveSync

GitToDrive is a python scrpit who allow to sync a git repository to a Google Drive Accout.  
It can be deployed inside a container , using the Dockerfile.

### Prerequisites

- **Python3**
- **[Drive](https://github.com/odeke-em/drive)**
- **Docker**

## Usage
```
usage: gitdrive [-h] {credential,init,start,auto} ...

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
---  
#### {credential}
```
usage: gitdrive credential [-h] [--path PATH]
```
This command allow to retrieve the **credentials.json** file that you need to access
your Google Drive account.

- **PATH** : this allow to set the path of the credential file 

```
Visit this URL to get an authorization code
[...]
Paste the authorization code: ******************

ls
credentials.json  Dockerfile  gitdrive  README.md
```
> for now the oauth2 authentification will be on your web browser
---
#### {init}
```
usage: usage: gitdrive init [-h] (--link LINK | --path PATH) [--json JSON]
```
With this command you can initialize a git repository for drive.
When initialized all the folder/repository content will be uploaded in a new directory  with the same name at the root.

- **LINK** : Link of the git repository to use (clone)
- **PATH** : if used with **LINK** it allow to set where the repository will be cloned. Otherwise if used alone, you can select an allready cloned repository
- **JSON** : use json credential instead of the default drive oauth2
---
#### {start}

```
usage: gitdrive start [-h] [--hook] [--port PORT] DIR
```

Allow to start the GitDriveSync loop that will check and update the drive directory linked to it

- **--hook** : switch the checking loop with a server , that update to POST request.
the path will be **/{DIR}** on the port 8080 (you can use it with github hook)
- **PORT** : set the server's port (with **--hook**)
- **DIR** : path of the git repository initialized iwht the **init** command
---
#### {auto}

```
usage: gitdrive auto [-h] (--link LINK | --path PATH) [--json JSON] [--hook]
```

fusion of the command **init** and **start** , arguments are exactly the same


## Docker

If you want to use it with docker, you have to build it with this :
```
docker build -t git_drive_sync \
--build-arg ssh_prv_key="$(cat ~/.ssh/id_rsa)" \
--build-arg ssh_pub_key="$(cat ~/.ssh/id_rsa.pub)" \
--build-arg credentials="test/credentials.json" .
```
You can add `--build-arg port=80` to change the expose port (8080 by default)

Then you can run it (for one repository) with this : 
```
docker run -p 8080:8080 git_drive_sync:latest git@github.com:Agraael/GitToDriveSync.git
```
Then you can update it like this
```
 curl --url "0.0.0.0:8080/GitToDriveSync" --request POST
```