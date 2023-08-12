from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit

# FOR AES
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# FOR RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode

# FOR TTIE
from PIL import Image
import PIL
import random

# FOR IMAGE ENCRYPTION
import cv2
# from openface import align, align_dlib, TorchNeuralNet, utilities
import face_recognition
import math
import numpy as np

# AES Decrypt
def decryptAES(enc, key):
    enc = base64.b64decode(enc)
    # cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16)

# RSA Decrypt
def decryptRSA(encrRSA):
    key = RSA.importKey(open('privatekey.pem').read())
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    decrypted_message = cipher.decrypt(b64decode(encrRSA))
    str1 = decrypted_message.decode('utf-8')
    return str1

# =========================================
# Diffie Hellman Algorithm
# =========================================
# A prime number P is taken
P = 137
# A primitive root for P, G is taken
G = 29
# User 1 will choose the private key a
a = 5
# User 2 will choose the private key b
b = 7
# Generated Secret Key for User 1
ka = 0

# skey = secret key, pkey = private key, prime = prime number
def dhalgo(skey, pkey, prime, check):
    key1 = int(pow(skey, pkey, prime)) # X^a mod prime
    if check == 0:
        return key1
    elif check == 1:
        global ka
        # Generated Secret Key for User 1
        ka = int(pow(key1, a, P))
        return key1


# def biometric():
#     camera = cv2.VideoCapture(0)
#     _, image = camera.read()

# # Load the trained face recognition model
#     align = align_dlib.AlignDlib("shape_predictor_68_face_landmarks.dat")
#     net = TorchNeuralNet("openface.nn4.small2.v1.t7")
    
#     # Load the image and preprocess it for face recognition
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     aligned_face = align.align(96, rgb_image, align.getLargestFaceBoundingBox(rgb_image), landmarkIndices=align.OUTER_EYES_AND_NOSE)
#     preprocessed_face = (aligned_face / 255.0 - 0.5) * 2

#     # Use the model to recognize the face
#     embeddings = net.forward(preprocessed_face[np.newaxis])
    
# # example usage
# plaintext = "Hello"
# key_length = len(plaintext)
# key = generate_key(key_length)
# encrypted = encrypt_message(plaintext, key)

# print(f"Plaintext: {plaintext}")
# print(f"Key: {key}")
# print(f"Encrypted message: {encrypted}")


# Diffie Hellman Key Exchange

# Shared Secret Key of User 1
x = dhalgo(G, a, P, 0)

# Shared Secret Key of User 2
# y = dhalgo(G, b, P, 0)
y = -1
# =========================================

# =========================================
# TEXT TO IMAGE ENCRYPTION ALGORITHM
# =========================================
def ttieEncrypt(text, len, private_key):
    ttieImage = Image.new('RGB', (len, len))

    # For First Plane Of Encryption
    for i in range(len):
        pixel_value = ord(text[i])
        if i % 3 == 0:
            for j in range(len):
                n2 = random.randint(0, 127)
                n3 = random.randint(0, 127)
                ttieImage.putpixel((i, j), (pixel_value, n2, n3))
        elif i % 3 == 1:
            for j in range(len):
                n1 = random.randint(0, 127)
                n3 = random.randint(0, 127)
                ttieImage.putpixel((i, j), (n1, pixel_value, n3))
        else:
            for j in range(len):
                n1 = random.randint(0, 127)
                n2 = random.randint(0, 127)
                ttieImage.putpixel((i, j), (n1, n2, pixel_value))
    ttieImage.save('C:/Users/91892/ChatWebApp using FlaskSocketIO/ChatWebApp/ttieOutput.png')

    # For Second Plane i.e. Correction Plane
    for i in range(int(len/2)):
        # pixel_value = ord(text[i])
        for j in range(len):
            pixels_value = ttieImage.getpixel((i, j))
            ttieImage.putpixel((i, j), (pixels_value[0]+private_key, pixels_value[1]+private_key, pixels_value[2]+private_key))

    # Saving the image after two layers of Text to Image Encryption
    ttieImage.save('C:/Users/91892/ChatWebApp using FlaskSocketIO/ChatWebApp/ttieOutput2.png')
    return ttieImage


def ttieDecrypt(ttieImage, len1, private_key):
    ttieText = ''
    ttieImageRGB = ttieImage.convert('RGB')
    for i in range(len1):
        if i<int(len1/2):
            if i % 3 == 0:
                for j in range(len1):
                    pixels_value = ttieImageRGB.getpixel((i, j))
                    value = pixels_value[0] - private_key;
                    # value = pixels_value[0];
                    ttieText = ttieText + chr(value)
                    break;
            if i % 3 == 1:
                for j in range(len1):
                    pixels_value = ttieImageRGB.getpixel((i, j))
                    value = pixels_value[1] - private_key;
                    # value = pixels_value[1];
                    ttieText = ttieText + chr(value)
                    break;
            else:
                for j in range(len1):
                    pixels_value = ttieImageRGB.getpixel((i, j))
                    value = pixels_value[2] - private_key;
                    # value = pixels_value[2];
                    ttieText = ttieText + chr(value)
                    break;
        else:
            if i % 3 == 0:
                for j in range(len1):
                    pixels_value = ttieImageRGB.getpixel((i, j))
                    # value = pixels_value[0] - private_key;
                    value = pixels_value[0];
                    ttieText = ttieText+chr(value)
                    break;
            if i % 3 == 1:
                for j in range(len1):
                    pixels_value = ttieImageRGB.getpixel((i, j))
                    # value = pixels_value[1] - private_key;
                    value = pixels_value[1];
                    ttieText = ttieText+chr(value)
                    break;
            else:
                for j in range(len1):
                    pixels_value = ttieImageRGB.getpixel((i, j))
                    # value = pixels_value[2] - private_key;
                    value = pixels_value[2];
                    ttieText = ttieText+chr(value)
                    break;

    # PERFORMING TEXT CORRECTION TO THE OUTPUT
    textCorr = ttieText[0]
    count = 0
    try :
        for i in range(2, len1*2):
            count = count + 1
            if count == 4:
                count = 0
                continue
            else:
                textCorr = textCorr + ttieText[i]
    except:
        return textCorr

# =========================================
# IMAGE ENCRYPTION ALGORITHM
# =========================================
def int2bin8(x):
    result = ""
    for i in range(8):
        y=x&(1)
        result+=str(y)
        x=x>>1
    return result[::-1]

def int2bin16(x):
    result=""
    for i in range(16):
        y=x&(1)
        result+=str(y)
        x=x>>1
    return result

def imageEncryption(img, j0, g0, x0, EncryptionImg):
    x = img.shape[0]
    y = img.shape[1]
    c = img.shape[2]
    g0 = int2bin16(g0)
    for s in range(x):
        for n in range(y):
            for z in range(c):
                m = int2bin8(img[s][n][z])                   # Pixel value to octet binary
                ans=""
                for i in range(8):
                    ri=int(g0[-1])                           # Take the last digit of the manual cipher machine
                    qi=int(m[i])^ri                          # XOR with pixel value qi
                    xi = 1 - math.sqrt(abs(2 * x0 - 1))      # f1(x) chaotic iteration
                    if qi==0:                                # If qi=0, use x0i+x1i=1;
                        xi=1-xi;
                    x0=xi                                    # xi iteration
                    t=int(g0[0])^int(g0[12])^int(g0[15])     # Primitive polynomial x^15+x^3+1
                    g0=str(t)+g0[0:-1]                       # gi iteration
                    ci=math.floor(xi*(2**j0))%2              # Nonlinear transformation operator
                    ans+=str(ci)
                re=int(ans,2)
                EncryptionImg[s][n][z]=re                    # Write new image

img = cv2.imread(r"C:/Users/91892/ChatWebApp using FlaskSocketIO/ChatWebApp/ttieOutput2.png", 1)

def imageDecryption(EncryptionImg, j0, g0, x0, DecryptionImg):
    x = EncryptionImg.shape[0]
    y = EncryptionImg.shape[1]
    c = EncryptionImg.shape[2]
    g0 = int2bin16(g0)
    for s in range(x):
        for n in range(y):
            for z in range(c):
                cc = int2bin8(EncryptionImg[s][n][z])
                ans = ""
                for i in range(8):
                    xi = 1 - math.sqrt(abs(2 * x0 - 1))
                    x0 = xi
                    ssi = math.floor(xi * (2 ** j0)) % 2
                    qi=1-(ssi^int(cc[i]))
                    ri = int(g0[-1])
                    mi=ri^qi
                    t = int(g0[0]) ^ int(g0[12]) ^ int(g0[15])
                    g0 = str(t) + g0[0:-1]
                    ans += str(mi)
                re = int(ans, 2)
                DecryptionImg[s][n][z] = re

# ==================================================================================

# =========================================
# FLASK & SOCKETIO
# =========================================

app = Flask(__name__)
socketio = SocketIO(app)

# Load the trained face recognition model and the user embeddings



# Load the image and extract the face location and encoding
# image = face_recognition.load_image_file("path/to/image.jpg")
# face_locations = face_recognition.face_locations(image)
# face_encodings = face_recognition.face_encodings(image, face_locations)

# # Print the face encoding
# print(face_encodings[0])

# face_model = cv2.face.LBPHFaceRecognizer_create()
# face_model.read('face_model.yml')
# user_embeddings = np.load('user_embeddings.npy')

# # Create a list of embeddings
# embeddings = [face_encodings[0], face_encodings[1], ...]

# # Convert the list to a NumPy array
# embeddings_array = np.array(embeddings)

# # Save the array to a file
# np.save("embeddings.npy", embeddings_array)

# @app.route('/')
# def index():
#     if 'username' in session:
#         return render_template('chat.html')
#     else:
#         return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Capture an image from the user's webcam or upload a photo
        image_data = request.files['image'].read()
        nparr = np.fromstring(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Preprocess the image and extract the face embeddings
        face = preprocess_image(image)
        embeddings = get_embeddings(face)

        # Compare the user's embeddings to the known user embeddings
        distances = pairwise_distances(embeddings, user_embeddings)
        min_distance = np.min(distances)

        if min_distance < 0.75:
            # If the user is recognized, add the username to the session and redirect to the chat room
            username = get_username(distances)
            session['username'] = username
            return redirect('/')
        else:
            return render_template('index.html', error='Face not recognized')
    else:
        return render_template('index.html')
# def login():
    
#     if request.method == 'POST':
#         # Capture an image from the user's webcam or upload a photo
#         image_data = request.files['image'].read()
#         nparr = np.fromstring(image_data, np.uint8)
#         image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         training_set = {
#             "person1": ["path/to/face1.jpg", "path/to/face2.jpg"],
#             "person2": ["path/to/face3.jpg", "path/to/face4.jpg", "path/to/face5.jpg"]
#         }

#         training_set_embeddings = []
#         for person, face_paths in training_set.items():
#             for face_path in face_paths:
#                 image = cv2.imread(face_path)
#                 rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#                 aligned_face = align.align(96, rgb_image, align.getLargestFaceBoundingBox(rgb_image), landmarkIndices=align.OUTER_EYES_AND_NOSE)
#                 preprocessed_face = (aligned_face / 255.0 - 0.5) * 2
#                 embeddings = net.forward(preprocessed_face[np.newaxis])
#                 training_set_embeddings.append(embeddings)
        
#             training_set_embeddings = np.vstack(training_set_embeddings)
#             distances = utilities.pairwiseDistance(embeddings, training_set_embeddings)
#             min_distance = np.min(distances)
#             min_distance_index = np.argmin(distances)

#         distances = utilities.pairwiseDistance(embeddings, training_set_embeddings)
#         min_distance = np.min(distances)
#         min_distance_index = np.argmin(distances)
#         recognized_user_name = list(training_set.keys())[min_distance_index]
#         socketio.emit('user_recognized', {
#         'name': recognized_user_name,
#         'message': json['message']
#     })

#         # Preprocess the image and extract the face embeddings
#         face = preprocess_image(image)
#         embeddings = get_embeddings(face)

#         # Compare the user's embeddings to the known user embeddings
#         distances = pairwise_distances(embeddings, user_embeddings)
#         min_distance = np.min(distances)

#         if min_distance < THRESHOLD:
#             # If the user is recognized, add the username to the session and redirect to the chat room
#             username = get_username(distances)
#             session['username'] = username
#             return redirect('/')
#         else:
#             return render_template('login.html', error='Face not recognized')
#     else:
#         return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image using the Haar Cascade classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # If no faces are detected, return None
    if len(faces) == 0:
        return None

    # Crop the first face detected and resize it to a fixed size
    (x, y, w, h) = faces[0]
    face = cv2.resize(gray[y:y+h, x:x+w], (160, 160))

    # Return the preprocessed face
    return face

def get_embeddings(face):
    model = cv2.dnn.readNetFromTensorflow('facenet.pb')

    # Preprocess the face and normalize the pixel values
    face = cv2.dnn.blobFromImage(face, 1.0/255, (160, 160), [0,0,0], swapRB=True, crop=False)

    # Set the input and output blobs for the model
    model.setInput(face)
    embeddings = model.forward()

    # Reshape the embeddings to a 1D array
    embeddings = embeddings.flatten()
    return embeddings

def pairwise_distances(embeddings, user_embeddings):
    distances = np.linalg.norm(embeddings - user_embeddings, axis=1)

    return distances

def get_username(distances):
        
    THRESHOLD = 0.75
    users = np.load('users.npy', allow_pickle=True).item()
    
    # Find the index of the user with the smallest distance
    index = np.argmin(distances)
    
    # Get the username associated with the smallest distance
    username = users[index]

   # If the smallest distance is greater than a threshold, return None
    if distances[index] > THRESHOLD:
       return None

    return username
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    return render_template('chat.html', username=username, room=room)


@socketio.on('send_message')
def handle_send_message_event(data):
    print("{} has sent message to the room {}! Message : {}".format(data['username'], data['room'], data['message']))
    encAES = data['encAES']
    encRSA = data['encRSA']

    # =========================================
    # DIFFIE HELLMAN KEY EXCHANGE ALGORITHM
    # Shared Secret Key of User 2
    y = dhalgo(G, b, P, 1)

    # Generated Secret Key for User 2
    kb = dhalgo(x, b, P, 0)

    # Checking the Keys Generated
    print(x, y, ka, kb)


    # =========================================
    # TTIE : encRSA to image

    no_pixels = len(encRSA)
    # ttie_image = PIL.Image.open("ttieOutput.png")
    # ttie_image_rgb = ttie_image.convert("RGB")
    ttieEncryptedImage = ttieEncrypt(encRSA, no_pixels, ka)


    # =========================================
    # IMAGE ENCRYPTION
    img = cv2.imread(r"C:/Users/91892/ChatWebApp using FlaskSocketIO/ChatWebApp/ttieOutput2.png", 1)

    EncryptionImg = np.zeros(img.shape, np.uint8)
    imageEncryption(img, 10, 30, 0.123345, EncryptionImg)

    # Saving the Encrypted Image
    cv2.imwrite(r"C:/Users/91892/ChatWebApp using FlaskSocketIO/ChatWebApp/ttieOutput2Enc.png", EncryptionImg)

    # =========================================
    # IMAGE DECRYPTION
    img = cv2.imread(r"C:/Users/91892/ChatWebApp using FlaskSocketIO/ChatWebApp/ttieOutput2Enc.png", 1)
    DecryptionImg = np.zeros(img.shape, np.uint8)
    imageDecryption(img, 10, 30, 0.123345, DecryptionImg)

    # Saving the Decrypted Image
    cv2.imwrite(r"C:/Users/91892/ChatWebApp using FlaskSocketIO/ChatWebApp/ttieOutput2Dec.png", DecryptionImg)

    # =========================================
    # TTIE DECRYPTION
    ttieDecryptedText = ttieDecrypt(ttieEncryptedImage, no_pixels, kb)
    print("RSA Key Obtained after TTIE Decryption")
    print(ttieDecryptedText)

    # =========================================
    # RSA DECRYPTION TO GET AES KEY
    str2 = str(encRSA)
    decryptedRSA = decryptRSA(str2)

    # =========================================
    # AES DECRYPTION TO GET MESSAGE
    key = decryptedRSA
    decryptedAES = decryptAES(encAES, key)
    data['message'] = decryptedAES.decode("utf-8", "ignore")
    print('Message: ', decryptedAES.decode("utf-8", "ignore"))


    # data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    # save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])
    # socketio.emit('enc_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


if __name__ == '__main__':
    print("success")
    socketio.run(app, port = 5000, host = '127.0.0.2', debug = True)
