# Private File Saver - A desktop app that syncs local files to a private AWS S3 bucket

![](https://github.com/melvinkcx/private-file-saver/workflows/tests/badge.svg)

![](https://i.postimg.cc/KzjY5gsr/cover.png)

## What is Private File Saver?

It is a cross-platform desktop app that sync local files to your private AWS S3 bucket. 
AWS S3 is commercial-use cloud storage (object store) that provides end-to-end encryption, makes data stored inaccessible to 
cloud providers.

No one should be allowed to snoop into our privacy. I appreciate if you could give this project a ⭐ star ⭐ so it can reach more privacy-savvy audience like you. 

#### Features:
- Sync local files to AWS S3 bucket
- No installation required! Download and run, that's it
- Easy setup, all it takes is 3 simple steps
- Able to detected file changes since last synced
- Sync files from S3 bucket to local machine smartly

#### Supported platforms:
- Linux (Tested on Debian-based systems and Manjaro)
- MacOS (help wanted)
- Windows (help wanted)

#### Download page:

[Here](https://github.com/melvinkcx/private-file-saver/releases)

## Why Private File Saver?
Private File Saver is not a cloud storage service, it is merely a tool that helps synchronising local files to AWS S3 buckets. 
I personally don't trust conventional consumer cloud storage as much. 
I prefer storage solution with more granular control (encryption, access control, etc). 

### Secure with encryption at rest and on transmit
With AWS S3, all files can be encrypted from end-to-end, making sure that your files are not accessible by any parties other than yourself.
   
### Highly durable
Files (objects) stored in S3 buckets are automatically replicated into multiple facilities in an AWS region. AWS ensures 11-9s for its data durability over a given year.


## Setup Guide

#### Prerequisite:
- You will need an active AWS account

1. Download the executable 
2. Double click it
3. Follow the initialization steps on the screen
 
![](https://i.postimg.cc/0y51m147/instructions.png)


## Feedback or Issues?

You can create a Github issue, or drop me a message on [Twitter @melvinkcx2](https://twitter.com/melvinkcx2).


## Roadmap

For development roadmap, check [the Github Project page](https://github.com/melvinkcx/private-file-saver/projects).

## For Developers

#### Application Architecture

Private File Saver is built using PyWebView + Vue.js, packaged with PyInstaller. 

The core logic is implemented in Python, while the presentation layer is in Vue.js, glued with [PyWebView](https://pywebview.flowrl.com/). 

#### Implementation Details

##### How files are compared?

**Use md5sum**: Private File Saver generates md5sum for all files and added it as metadata to the s3 object. The core logic compares md5sum from local files and remotely to determine if local file has changed.

