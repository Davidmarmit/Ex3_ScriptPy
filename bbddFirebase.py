import pyrebase

firebaseConfig = {"apiKey": "AIzaSyCkaNNfSH4J3f8Y7iEcMAyf4qN4coDmC4Q",
                  "authDomain": "iniex4cam.firebaseapp.com",
                  "projectId": "iniex4cam",
                  "storageBucket": "iniex4cam.appspot.com",
                  "messagingSenderId": "909543523593",
                  "appId": "1:909543523593:web:129947cbc56792a8e8ffd8"
                  }

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


def upload_img(image, cont_img):
    storage.child("images").child("image" + cont_img + ".jpg").put(image)


def upload_video(video, cont_video):
    storage.child("videos").child("video" + cont_video + ".mp4").put(video)
