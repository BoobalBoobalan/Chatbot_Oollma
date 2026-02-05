import React, { useState, useEffect, useRef } from 'react';
import { Trash2 } from 'lucide-react';
import MessageBubble from './components/MessageBubble';
import ChatInput from './components/ChatInput';
import { sendMessage, checkHealth } from './api';

function App() {
    const [messages, setMessages] = useState([
        { role: 'system', content: 'Hello! I am your AI assistant running locally. How can I help you today?' }
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const [isBackendUp, setIsBackendUp] = useState(true);

    // Auto-scroll ref
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        // Check backend health on mount
        checkHealth().then(status => {
            if (status.status !== 'ok') {
                setIsBackendUp(false);
            }
        });
    }, []);

    const handleSendMessage = async (text) => {
        // Add User Message
        const userMessage = { role: 'user', content: text };
        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);

        try {
            // Call API
            const responseText = await sendMessage(text);

            // Add AI Response
            const aiMessage = { role: 'assistant', content: responseText };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            // Add Error Message
            setMessages(prev => [...prev, {
                role: 'system',
                content: 'Error: Could not connect to the AI model. Ensure Ollama and the Backend are running.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const clearChat = () => {
        setMessages([{ role: 'system', content: 'Chat history cleared. Start a new conversation!' }]);
    };

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white px-6 py-4 border-b border-gray-200 flex items-center justify-between sticky top-0 z-10 shadow-sm">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
                        AI
                    </div>
                    <div>
                        <h1 className="font-bold text-gray-800">LocalChat AI</h1>
                        <div className="flex items-center gap-1.5 ">
                            <span className={`w-2 h-2 rounded-full ${isBackendUp ? 'bg-green-500' : 'bg-red-500'}`}></span>
                            <span className="text-xs text-gray-500 font-medium">
                                {isBackendUp ? 'Online' : 'Backend Disconnected'}
                            </span>
                        </div>
                    </div>
                </div>
                <button
                    onClick={clearChat}
                    className="p-2 text-gray-500 hover:bg-gray-100 rounded-full hover:text-red-600 transition-colors"
                    title="Clear Chat"
                >
                    <Trash2 size={20} />
                </button>
            </header>

            {/* Chat Window */}
            <main className="flex-1 overflow-y-auto p-4 md:p-6 scroller">
                <div className="max-w-4xl mx-auto space-y-6">
                    {messages.map((msg, idx) => (
                        <MessageBubble key={idx} role={msg.role} content={msg.content} />
                    ))}
                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="bg-white p-4 rounded-2xl rounded-tl-none border border-gray-100 flex items-center gap-2">
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"></span>
                                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </main>

            {/* Input Area */}
            <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
        </div>
    );
}

export default App;
