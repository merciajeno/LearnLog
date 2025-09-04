import { useState } from "react";
import {useParams} from "react-router-dom";

const AddSubjectForm = () => {
     const {userId} = useParams()
    const [name, setName] = useState("");
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch("http://127.0.0.1:5000/add_subject", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, name: name }),
            });

            const data = await res.json();
            console.log(data);

            if (res.ok) {
                alert("Subject added successfully!");
                setName(""); // reset input
                // refresh subject list if parent passes callback
            } else {
                alert("Error adding subject");
            }
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Enter subject name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
            />
            <button type="submit">Add Subject</button>
        </form>
    );
};

export default AddSubjectForm;
