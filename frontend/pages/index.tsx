import { useState } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  async function send() {
    if (!input.trim()) return;
    const userMsg: Message = { role: 'user', content: input };
    setMessages((m) => [...m, userMsg]);
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input }),
      });
      const data = await res.json();
      const botMsg: Message = { role: 'assistant', content: data.answer };
      setMessages((m) => [...m, botMsg]);
    } catch (err) {
      const errorMsg: Message = {
        role: 'assistant',
        content: 'Error contacting backend.',
      };
      setMessages((m) => [...m, errorMsg]);
    }
    setInput('');
  }

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center p-6">
      <Head>
        <title>AURA</title>
      </Head>
      <motion.h1
        className="text-4xl mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        AURA
      </motion.h1>
      <div className="w-full max-w-2xl flex-1 overflow-y-auto mb-4">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`p-3 my-2 rounded-lg bg-gray-800 ${m.role === 'user' ? 'self-end' : 'self-start'} w-fit max-w-full`}
          >
            {m.content}
          </div>
        ))}
      </div>
      <div className="w-full max-w-2xl flex">
        <input
          className="flex-1 p-2 bg-gray-700 text-white rounded-l-md focus:outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              send();
            }
          }}
        />
        <button
          className="px-4 bg-blue-600 rounded-r-md"
          onClick={send}
        >
          Send
        </button>
      </div>
    </div>
  );
}
