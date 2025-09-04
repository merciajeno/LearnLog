import { useEffect, useState } from "react";
import {useParams} from "react-router-dom";

const LogList = () => {
    const [logs, setLogs] = useState([]);
    const{ userId,subjectId } = useParams();
    useEffect(() => {
        fetch(`http://127.0.0.1:5000/users/${userId}/subjects/${subjectId}/logs`)
            .then(res => res.json())
            .then(data => setLogs(data.logs || []))
            .catch(err => console.error(err));
    }, [userId, subjectId]);

    return (
        <div>
            <h3>Logs</h3>
            <ul>
                {logs.map((log) => (
                    <li key={log.id}>
                        {log.content} - {new Date(log.date).toLocaleDateString()}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default LogList;
