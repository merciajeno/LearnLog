import { useState } from "react";
import {useParams} from "react-router-dom";

const AddLogForm = () => {
    const {userId,subjectId} = useParams()
    const [content, setContent] = useState("");
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch("http://127.0.0.1:5000/add_log", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, subject_id:subjectId,content:content }),
            });

            const data = await res.json();
            console.log(data);

            if (res.ok) {
                alert("Log added successfully!");
                setContent(""); // reset input

            } else {
                alert("Error adding log details");
            }
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="What did you learn today?"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
            />
            <button type="submit">Enter </button>
        </form>
    );
};

export default AddLogForm;
