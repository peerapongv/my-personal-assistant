import axios from 'axios';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Generate a response from the LLM through the API
 * @param {string} prompt - The user's message/prompt
 * @param {string} provider - Optional LLM provider to use
 * @returns {Promise<Object>} - The API response
 */
export const generateResponse = async (prompt, provider = null) => {
  try {
    const response = await apiClient.post('/generate', {
      prompt,
      provider,
      parameters: {},
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Check the API health status
 * @returns {Promise<Object>} - The health check response
 */
export const checkApiHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export default apiClient;
