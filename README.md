# Private File Saver

![](https://github.com/melvinkcx/private-file-saver/workflows/tests/badge.svg)

## What is Private File Saver?

It is a cross-platform desktop app that sync your local files to your private AWS S3 bucket. 
S3 bucket is a cloud storage that provides end-to-end encryption, makes data stored inaccessible to 
cloud providers.

## Why Private File Saver?
If you use a conventional cloud storage, it is likely that your files are being analyzed by the storage providers.
Personally, I keep an archive of old photos and videos in my personal computer. 
It would be great if my files are not being analyzed in any way.  

### Secure with encryption at rest and on transmit
With AWS S3, all files can be encrypted from end-to-end, making sure that your files are not accessible by any parties other than yourself.
   
### Highly durable
Files (objects) stored in S3 buckets are automatically replicated into multiple facilities in an AWS region. AWS ensures 11-9s for its data durability over a given year. 


## Implementation Details

### How files are compared?

1. **Use md5sum**: Secret bucket generates md5sum for all files and added it as metadata to the s3 object. The core logic compares md5sum from local files and remotely to determine if local file has changed.

## Packaging using PyInstaller

pyinstaller can't pick up `configparser` and `botocore` depends on it.

