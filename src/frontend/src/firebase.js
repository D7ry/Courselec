// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
import {getAuth, GoogleAuthProvider, signInWithPopup} from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBfXrJd-sVq2b_UyVfm2Kgy5TeQsvvuLvI",
  authDomain: "coursedemo-2aafd.firebaseapp.com",
  projectId: "coursedemo-2aafd",
  storageBucket: "coursedemo-2aafd.appspot.com",
  messagingSenderId: "611503589108",
  appId: "1:611503589108:web:0abc2ac13cbf2bf7e000a1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app)


const provider = new GoogleAuthProvider()

export const signInWithGoogle = () => {
    signInWithPopup(auth, provider).then((result) => {
        const name=result.user.displayName
        const email = result.user.email
        const profilePic = result.user.photoURL

        localStorage.setItem("name", name)
        localStorage.setItem("profilePic", profilePic)
    }).catch((error) => {
        console.log(error)
    })

};