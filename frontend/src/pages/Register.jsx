// Register.jsx
import React, { useState } from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../firebase";

function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleRegister = async () => {
        try {
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const res = await fetch("http://127.0.0.1:5000/add_user", {
                method: "POST",
                headers: {Authorization: userCredential.user.getIdToken(),
                "Content-Type": "application/json",},
                body:JSON.stringify( {
                    "uid":userCredential.user.uid,
                    "email":email
                })
            })
            console.log(res);
            console.log("Registered User:", userCredential.user);
            alert("Registration successful!");
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleRegister}>Register</button>
        </div>
    );
}

export default Register;
