# face-rekognition-AWS
Face-rekognition project is used for comparing the faces( human Beings ).
this is completely based on the AWS Cloud Services.

AWS Cloud Services- Rekognition
                    S3 bucket
                    dyanamo DB
                    API Gatway
                    Lambda
                    
The entire backend runs on AWS Lambda.
"Front end" folder is the web page ( HTML code + Flask ) to enter details and get them when ever required.
the "get.py" and "put.py" are the backend of the html page.

"pi.py" is the file that runs on the raspberry pi which uses the pi camera to capture images .
it uses 'open cv' to recognise human faces 
