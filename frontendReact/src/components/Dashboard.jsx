import React, { useEffect, useState } from 'react';
import CropForm from './CropForm';
import axios from 'axios';

const Dashboard = () => {
    const [username, setUsername] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Check if user is authenticated
        const token = localStorage.getItem('token');
        const storedUsername = localStorage.getItem('username');

        if (!token) {
            window.location.href = '/login';
            return;
        }

        // Configure axios to use the token for all requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        // Verify token is valid by making a request to protected endpoint
        axios.get('http://localhost:5000/protected')
            .then(response => {
                setIsAuthenticated(true);
                setUsername(storedUsername || response.data.message.split(' ')[1]);
            })
            .catch(error => {
                console.error('Authentication error:', error);
                localStorage.removeItem('token');
                window.location.href = '/login';
            })
            .finally(() => {
                setIsLoading(false);
            });
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = '/login';
    };

    if (isLoading) {
        return (
            <div className="loading">
                <p>Loading...</p>
            </div>
        );
    }

    return (
        <div className="dashboard">
            <header className="dashboard-header">
                <h1>FieldStat Dashboard</h1>
                <div className="user-info">
                    <span>Welcome, {username}</span>
                    <button onClick={handleLogout} className="logout-button">
                        Logout
                    </button>
                </div>
            </header>

            <div className="dashboard-content">
                <CropForm />
            </div>
        </div>
    );
};

export default Dashboard;
