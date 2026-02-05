import React from 'react';
import Markdown from 'react-markdown';
import { User, Bot } from 'lucide-react';

const MessageBubble = ({ role, content }) => {
    const isUser = role === 'user';

    return (
        <div className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[80%] md:max-w-[70%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-2`}>

                {/* Icon */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? 'bg-blue-600 text-white' : 'bg-emerald-600 text-white'}`}>
                    {isUser ? <User size={18} /> : <Bot size={18} />}
                </div>

                {/* Bubble */}
                <div className={`p-3 rounded-2xl shadow-sm overflow-hidden ${isUser
                        ? 'bg-blue-600 text-white rounded-tr-none'
                        : 'bg-white text-gray-800 border border-gray-100 rounded-tl-none'
                    }`}>
                    <div className={`prose text-sm ${isUser ? 'prose-invert' : ''}`}>
                        {/* Render Markdown for AI, simple text for User to avoid injection issues if any, though Markdown is safe usually */}
                        <Markdown>{content}</Markdown>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MessageBubble;
