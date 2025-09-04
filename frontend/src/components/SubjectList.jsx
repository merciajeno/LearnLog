import { useEffect, useState } from "react";
import {useParams} from "react-router-dom";

const SubjectList = () => {
    const {userId}  = useParams()
    const [subjects, setSubjects] = useState([]);

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/get_subjects/${userId}`)
            .then(res => res.json())
            .then(data =>
            {
                console.log(data)
                setSubjects(data.subjects || [])
            })

            .catch(err => console.error(err));
    }, [userId]);

    return (
        <div>
            <h2>Your Subjects</h2>
            <ul>
                {subjects.map((subject) => (
                    <li key={subject.id}>{subject.name}</li>
                ))}
            </ul>

        </div>
    );
};

export default SubjectList;
