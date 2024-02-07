import React from "react";

function Dashboard() {
    // Retrieve username from local storage
    const username = localStorage.getItem('username');

    return (
        <div>
            <div>
                <h1>Task Hub</h1>
            </div>
            <div>
                <h2>Welcome to Task Hub, {username}!</h2>

            </div>
        </div>
    );
};

export default Dashboard;
