import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000', // Connects to deployed URL or FastAPI locally
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Sends a chat message to the backend.
 * @param {string} message - User's message
 * @param {string} model - Selected model (default: llama3)
 * @returns {Promise<string>} - AI response
 */
export const sendMessage = async (message, model = 'tinyllama') => {
    try {
        const response = await api.post('/chat', {
            message,
            model,
            use_openai: false
        });
        return response.data.response;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};

export const checkHealth = async () => {
    try {
        const response = await api.get('/health');
        return response.data;
    } catch (error) {
        console.error("Health Check Failed:", error);
        return { status: "error" };
    }
};

export default api;
