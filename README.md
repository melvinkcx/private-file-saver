# Secret Bucket

## What is Secret Bucket?

It is a cross-platform desktop app that sync your local files to your private AWS S3 bucket. 
S3 bucket is a cloud storage that provides end-to-end encryption, makes data stored inaccessible to 
cloud providers.

## Why Secret Bucket?
If you use cloud storage like Google Drive, it is likely that your files are being analyzed by the storage providers.
Personally, I keep an archive of old photos and videos in my personal computer. It would be great if my photos are not being analyzed in any way.  

### Secure with encryption at rest and on transmit
With AWS S3, all files can be encrypted from end-to-end, making sure that your files are not accessible by any parties other than yourself.

### Highly available 
AWS S3 promises 11 Nines (11-9s) for it's service availability. 
   
### Highly durable
Files (objects) stored in S3 buckets are automatically replicated into multiple facilities in an AWS region. AWS ensures 11-9s for its data durability over a given year. 



## Checklist for Features

1. A dialog to list all buckets, and to be picked
1. 


## Implementation Details

### How files are compared?

1. **Use Etag**: AWS generated ETag for each file uploaded. The algorithm is as below:
    ```
    If the file is uploaded w/o using multipart, the `etag` is the `md5 hash` of the content
    If the file is uploaded with multipart, the `etag` is the binary concatenation of `md5 sum` of each part, appended with a dash (`-`) and number of parts. 

    References:
    - [https://stackoverflow.com/questions/6591047/etag-definition-changed-in-amazon-s3](https://stackoverflow.com/questions/6591047/etag-definition-changed-in-amazon-s3)   
    ```
   
