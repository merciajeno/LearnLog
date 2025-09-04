

import { useEffect, useState } from "react";
import {useParams} from "react-router-dom";
function Dashboard({user_id}) {
    const {id} = useParams();
    const [data, setData] = useState(null);
    useEffect(() => {
        const fetchDashboard = async () => {
            console.log(user_id);
            const res = await fetch(`http://127.0.0.1:5000/dashboard/${id}`);
            const result = await res.json();
            setData(result);
        };
        fetchDashboard();
    }, []);

    if (!data) return <p>Loading...</p>;

    return (
        <div>
            <h2>Welcome </h2>
            <h3>🔥 Streak: {data.streak} days</h3>

            <h3> Number Of Logs: {data.today_logs}</h3>
        </div>
    );
}

export default Dashboard;
