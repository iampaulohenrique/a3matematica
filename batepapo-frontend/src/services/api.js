// src/services/api.js

import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000', // URL do seu backend
});


export const sendMessage = async (userId, key, message, mediaType) => {
  return await api.post('/send_message', {
    user_id: userId,
    key,
    message,
    media_type: mediaType,
  });
};

export const getMessages = async (userId, key) => {
  return await api.get(`/get_messages/${userId}`, {
    params: { key },
  });
};
