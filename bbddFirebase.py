import pyrebase

firebaseConfig = {"apiKey": "AIzaSyAdNxdx-VKLVy1bT_R86p2GPlIs59jSH_0",
                  "authDomain": "instalacions-interactives.firebaseapp.com",
                  "databaseURL": "https://instalacions-interactives-default-rtdb.europe-west1.firebasedatabase.app",
                  "projectId": "instalacions-interactives",
                  "storageBucket": "instalacions-interactives.appspot.com",
                  "messagingSenderId": "1013681284704",
                  "appId": "1:1013681284704:web:cfcce9b84960e132784505"
                  }

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


def upload_img(image, cont_img):
    storage.child("images").child("image" + cont_img + ".jpg").put(image)


def upload_video(video, cont_video):
    storage.child("videos").child("video" + cont_video + ".mp4").put(video)
