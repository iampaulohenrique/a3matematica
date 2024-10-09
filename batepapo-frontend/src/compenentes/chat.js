// src/components/Chat.js

import React, { useState, useEffect } from 'react';
import { sendMessage, getMessages } from '../services/api';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const userId = 1; // ID do usuário
  const key = 'sua_chave_secreta'; // Chave de criptografia

  const fetchMessages = async () => {
    const response = await getMessages(userId, key);
    setMessages(response.data);
  };

  const handleSend = async () => {
    await sendMessage(userId, key, message);
    setMessage('');
    fetchMessages(); // Atualiza a lista de mensagens
  };

  useEffect(() => {
    fetchMessages(); // Busca mensagens ao montar o componente
  }, []);

  return (
    <div>
      <h2>Chat</h2>
      <div>
        {messages.map((msg, index) => (
          <div key={index}>
            <p>{msg.message} {msg.media_type && <span>({msg.media_type})</span>}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Digite sua mensagem"
      />
      <button onClick={handleSend}>Enviar</button>
    </div>
  );
};

export default Chat;
