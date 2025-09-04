import {initializeApp} from 'firebase/app'
import {getAuth} from 'firebase/auth'

const firebaseConfig = {
    apiKey: "AIzaSyDZ2IvMQ9TMVgh0i1EDHiXlLq6EOW4GQBo",
    authDomain: "learnlog-85e32.firebaseapp.com",
    projectId: "learnlog-85e32"
}
const app = initializeApp(firebaseConfig)
export const auth = getAuth(app)
