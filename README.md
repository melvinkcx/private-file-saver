# Private File Saver - Desktop client to sync local files to AWS S3 buckets
![](https://github.com/melvinkcx/private-file-saver/workflows/tests/badge.svg)

![](https://i.postimg.cc/KzjY5gsr/cover.png)

## What is Private File Saver?

It is a cross-platform desktop app that sync local files to your private AWS S3 bucket. 
AWS S3 is commercial-use cloud storage (object store) that provides end-to-end encryption, makes data stored inaccessible to 
cloud providers.

#### Features:
- Sync local files to AWS S3 bucket
- No installation required! Download and run, that's it. 
- Easy setup, with 3 simple steps
- Able to detected file changes since last synced

#### Supported platforms:
- Linux (Tested on Debian-based systems and Manjaro)
- MacOS (Not done yet, help wanted)
- Windows (Not done yet, help wanted)

#### Download page:

[Here](https://github.com/melvinkcx/private-file-saver/releases)

## Setup Guide

#### Prerequisite:
- You will need an active AWS account

1. Download the executable 
2. Double click it
3. Follow the initialization steps on the screen
 
![](https://i.postimg.cc/0y51m147/instructions.png)

## Why Private File Saver?
I personally don't trust conventional consumer cloud storage as much. I prefer storage solution with more granular control (encryption, access control, etc).
Private File Saver is not a cloud storage service, it is merely a tool or software that helps to sync local files to AWS S3 buckets. 

### Secure with encryption at rest and on transmit
With AWS S3, all files can be encrypted from end-to-end, making sure that your files are not accessible by any parties other than yourself.
   
### Highly durable
Files (objects) stored in S3 buckets are automatically replicated into multiple facilities in an AWS region. AWS ensures 11-9s for its data durability over a given year.

## For Developers
#### Implementation Details

##### How files are compared?

1. **Use md5sum**: Secret bucket generates md5sum for all files and added it as metadata to the s3 object. The core logic compares md5sum from local files and remotely to determine if local file has changed.


