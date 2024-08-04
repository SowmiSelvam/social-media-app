// src/services/api.js
import axios from 'axios';

const api = axios.create({
    // baseURL: 'http://localhost:8000',  
    baseURL: 'http://13.56.15.81:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

const getToken = () => localStorage.getItem('access_token');

api.interceptors.request.use(config => {
    const token = getToken();
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
}, error => Promise.reject(error));

export const signupUser = async (userData) => {
    try {
        const { data } = await api.post('/signup', userData);
        return data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

// Function to handle user login
export const loginUser = async (userData) => {
    try {
        const { data } = await api.post('/login', userData);
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        return data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

// Function to fetch all notes
export const fetchAllNotes = async () => {
    try {
        const { data } = await api.get('/home');
        return data;
    } catch (error) {
        console.error('Error fetching notes:', error);
        throw error.response?.data || error.message;
    }
};

// Function to add a note
export const addNote = async (noteData) => {
    try {
        const { data } = await api.post('/add_note', noteData);
        return data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const updateNote = async (noteId, noteData) => {
    try {
        const { data } = await api.put(`/update_note/${noteId}`, noteData);
        return data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const getUserNotes = async () => {
    try {
        const { data } = await api.get('/get_user_notes');
        return data.notes;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const deleteNote = async (noteId) => {
    try {
        const { data } = await api.delete(`/delete_note/${noteId}`);
        return data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const checkAuth = async () => {
    try {
        const token = getToken(); 
        const { data } = await api.get('/check_auth_status', {
            headers: { Authorization: `Bearer ${token}` }
        });
        return data;
    } catch (error) {
        console.error('Error checking auth status:', error);
        throw error.response?.data || error.message;
    }
};

export const logoutUser = async () => {
    try {
        const refreshToken = localStorage.getItem('refresh_token');
        const { data } = await api.post('/logout_user', { refresh_token: refreshToken });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};
