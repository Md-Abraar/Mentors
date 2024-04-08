# import cv2
# import pyaudio
# import audioop

# class VideoCamera:
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)

#     def __del__(self):
#         self.video.release()

#     def generate_frames(self, stream):
#         max_blink_count = 5  # Maximum allowed blinks
#         blink_counter = 0

#         prev_eye_state = True
#         tab_switch_detected = False
#         noise_detected = False
#         noise_reset_counter = 0
#         noise_reset_threshold = 50 

#         while True:
#             ret, frame = self.video.read()

#             if not ret:
#                 break

#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#             face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#             faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#             if len(faces) == 0:
#                 cv2.putText(frame, "Face Not Detected!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
#             for (x, y, w, h) in faces:
#                 roi_gray = gray[y:y + h, x:x + w]

#                 # Use Haar Cascade to detect eyes
#                 eyes = cv2.Canny(roi_gray, 100, 200)

#                 # Check for eye state (open or closed)
#                 eye_state = True  # Default to open
#                 contours, _ = cv2.findContours(eyes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#                 for contour in contours:
#                     area = cv2.contourArea(contour)
#                     if area < 1000:  # Threshold for closed eyes
#                         eye_state = False  # Eyes are closed

#                 if eye_state != prev_eye_state:
#                     prev_eye_state = eye_state
#                     if not eye_state:
#                         blink_counter += 1

#             # Check for tab switching (use a more sophisticated method for actual implementation)
#             key = cv2.waitKey(1)
#             if key == 9:  # Tab key
#                 tab_switch_detected = True

#             # Check for excessive noise (audio)
#             audio_data = stream.read(1024)  # Assuming `stream` is defined somewhere globally
#             rms = audioop.rms(audio_data, 2)
#             if rms > 1000:  # Adjust the noise threshold as needed
#                 noise_detected = True
#                 noise_reset_counter = 0
#             else:
#                 if noise_reset_counter < noise_reset_threshold:
#                     noise_reset_counter += 1
#                 else:
#                     noise_detected = False

#             # Display warning if suspicious activity is detected
#             if blink_counter > max_blink_count or noise_detected:
#                 cv2.putText(frame, "Suspicious Activity Detected!", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
#             ret, buffer = cv2.imencode('.jpg', frame)
#             if not ret:
#                 continue

#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
