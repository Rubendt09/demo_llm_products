import React from 'react';
import { type Message } from '../types/demo';
import FormattedText from './FormattedText';

interface ChatHeaderProps {
  title?: string;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({ 
  title = "🤖 Agente de Pedidos Inteligente (DEMO)" 
}) => (
  <header className="p-4 bg-indigo-600 text-white rounded-t-xl">
    <h1 className="text-xl font-bold">{title}</h1>
    <p className="text-sm opacity-90">
      Demostrando Tool Calling y RAG - Gemini 2.5 Flash
    </p>
  </header>
);

interface LoadingIndicatorProps {}

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = () => (
  <div className="flex justify-start">
    <div className="max-w-xs md:max-w-md lg:max-w-lg p-3 rounded-xl shadow-md bg-gray-200 text-gray-800 rounded-tl-none">
      <div className="flex space-x-1">
        <div className="h-2 w-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
        <div className="h-2 w-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        <div className="h-2 w-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.3s' }}></div>
      </div>
    </div>
  </div>
);

interface WelcomeMessageProps {}

export const WelcomeMessage: React.FC<WelcomeMessageProps> = () => (
  <div className="text-center text-gray-500 mt-20 p-4 border border-indigo-200 bg-indigo-50 rounded-lg">
    <p className="font-semibold text-indigo-700 mb-2">Instrucciones para la Demo:</p>
    <ul className="text-sm list-disc list-inside text-left mx-auto max-w-sm space-y-1">
      <li><strong>RAG:</strong> Pregunta: "¿Cuál es la descripción del Monitor 4K Curvo?"</li>
      <li><strong>Tool Calling:</strong> Pregunta: "¿Hay existencias del producto S001?"</li>
      <li><strong>System Prompt:</strong> Intenta que hable de fútbol. El Agente te recordará su rol.</li>
    </ul>
  </div>
);

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => (
  <div className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
    <div className={`max-w-xs md:max-w-md lg:max-w-lg p-3 rounded-xl shadow-md ${
      message.sender === 'user' 
        ? 'bg-indigo-500 text-white rounded-br-none' 
        : 'bg-gray-200 text-gray-800 rounded-tl-none'
    }`}>
      <div className="text-sm whitespace-pre-wrap">
        <FormattedText text={message.text} />
      </div>
      {message.timestamp && (
        <p className={`text-xs mt-1 opacity-70 ${
          message.sender === 'user' ? 'text-indigo-100' : 'text-gray-500'
        }`}>
          {message.timestamp.toLocaleTimeString()}
        </p>
      )}
    </div>
  </div>
);

interface ChatInputProps {
  input: string;
  isLoading: boolean;
  onInputChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export const ChatInput: React.FC<ChatInputProps> = ({ 
  input, 
  isLoading, 
  onInputChange, 
  onSubmit 
}) => (
  <footer className="p-4 border-t border-gray-200 bg-gray-50 rounded-b-xl">
    <form onSubmit={onSubmit} className="flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => onInputChange(e.target.value)}
        placeholder="Pregunta o ejecuta una acción (ej. ¿Hay stock del T010?)"
        className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 transition duration-150"
        disabled={isLoading}
      />
      <button
        type="submit"
        className="bg-indigo-600 text-white p-3 rounded-lg font-semibold hover:bg-indigo-700 transition duration-150 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
        disabled={isLoading || !input.trim()}
      >
        {isLoading ? 'Enviando...' : 'Enviar'}
      </button>
    </form>
  </footer>
);