from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import boto3
#from boto3.s3.connection import S3Connection
#from boto3.s3.key import Key
s3=boto3.client('s3',
aws_access_key_id='#your_aws_accesskey',
aws_secret_access_key='#your_aws_secretaccesskey')
#conn = S3Connection(AWS_ACCESS,AWS_SECRET)
#bucket = conn.get_bucket('be.wapptastic')
def main(argv):

        # Setup the camera
        camera = PiCamera()
        camera.resolution = ( 480, 320 )
        camera.framerate = 40
        rawCapture1 = PiRGBArray( camera, size=( 480, 320 ) )
        

        # Load a cascade file for detecting faces
        face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml' )

        #t_start = time.time()
        #fps = 0
        
        


        ### Main ######################################################################

        # Capture frames from the camera
        for frame in camera.capture_continuous( rawCapture1, format="bgr", use_video_port=True ):

            image = frame.array

            # Use the cascade file we loaded to detect faces
            gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
            faces = face_cascade.detectMultiScale( gray , 1.3, 5)

           

            # Draw a rectangle around every face and move the motor towards the face
            for ( x, y, w, h ) in faces:
                camera.capture("image.jpeg")
                #hp="image.jpeg"
                #s3=boto3.resource('s3')
                #BUCKET="mybucket789"
                s3.upload_file('key','Your_targetbucet','key')
                
                
                cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 100, 255, 100 ), 2 )
                

                # Calculate and show the FPS
                #cv2.imwrite("image%04i.jpeg", image)
                    
                time.sleep(1)    
            
            # Show the frame
            cv2.imshow( "Frame", image)
            


            
            cv2.waitKey( 1 )

            # Clear the stream in preparation for the next frame
            rawCapture1.truncate( 0 )

if __name__ == '__main__':
        main(sys.argv)
