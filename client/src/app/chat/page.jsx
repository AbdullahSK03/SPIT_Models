"use client";

import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = (event) => {
    event.preventDefault();
    setMessages([...messages, input]);
    setInput('');
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="overflow-auto p-4">
        {messages.map((message, index) => (
          <div key={index} className="p-2 bg-blue-500 text-white my-2 rounded">
            {message}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage} className="m-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          type="text"
          className="w-full p-2 border rounded"
        />
        <button type="submit" className="w-full p-2 bg-blue-500 text-white mt-2 rounded">
          Send
        </button>
      </form>
    </div>
  );
}
