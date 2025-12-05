import React, { useState, useEffect, useCallback, useRef } from 'react';
import { sendMessage, checkHealth, type Message as OrchestratorMessage } from './services/orchestrator';
import { type Message } from './types/demo';
import { 
  ChatHeader, 
  LoadingIndicator, 
  WelcomeMessage, 
  MessageBubble, 
  ChatInput 
} from './components/ChatComponents';

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [orchestratorReady, setOrchestratorReady] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Verificar que el orquestador esté disponible
  useEffect(() => {
    checkHealth().then(isHealthy => {
      if (isHealthy) {
        console.log('✅ Orquestador LLM disponible');
        setOrchestratorReady(true);
        setError(null);
      } else {
        console.error('❌ Orquestador LLM no disponible');
        setError('El microservicio orquestador no está disponible. Asegúrate de que esté corriendo en http://localhost:8001');
      }
    });
  }, []);

  // SCROLL AL FINAL DEL CHAT
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // MANEJADOR DE ENVÍO DE MENSAJE
  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !orchestratorReady) return;

    const userMessage: Message = { 
      sender: 'user', 
      text: input.trim(),
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      // Convertir mensajes al formato del orquestador
      const conversationHistory: OrchestratorMessage[] = messages.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      }));
      
      // Llamar al microservicio orquestador
      const response = await sendMessage(userMessage.text, conversationHistory);
      
      console.log('📊 Tokens usados:', response.tokens_used);
      if (response.functions_called && response.functions_called.length > 0) {
        console.log('🔧 Funciones ejecutadas:', response.functions_called);
      }
      
      const botMessage: Message = { 
        sender: 'bot', 
        text: response.response,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
      
    } catch (error) {
      console.error("Error durante la orquestación full stack:", error);
      const errorMessage: Message = {
        sender: 'bot',
        text: 'Ocurrió un error al comunicarse con el orquestador. Verifica que el microservicio esté corriendo.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, orchestratorReady, messages]);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="bg-red-50 border border-red-300 rounded-lg p-6 max-w-md">
          <h2 className="text-red-800 font-bold mb-2">⚠️ Servicio No Disponible</h2>
          <p className="text-red-700 mb-4">{error}</p>
          <ol className="text-sm text-red-600 list-decimal list-inside space-y-1">
            <li>Verifica que el microservicio orquestador esté corriendo: `docker-compose up -d`</li>
            <li>Verifica que el puerto 8001 esté disponible</li>
            <li>Revisa los logs: `docker logs llm-orchestrator`</li>
          </ol>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-4xl bg-white shadow-2xl rounded-xl flex flex-col h-[80vh]">
        
        <ChatHeader title={import.meta.env.VITE_APP_TITLE} />

        {/* Área de Chat */}
        <main className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
          {messages.length === 0 && <WelcomeMessage />}
          
          {messages.map((msg, index) => (
            <MessageBubble key={index} message={msg} />
          ))}
          
          {isLoading && <LoadingIndicator />}
          <div ref={chatEndRef} />
        </main>

        <ChatInput
          input={input}
          isLoading={isLoading}
          onInputChange={setInput}
          onSubmit={handleSubmit}
        />
      </div>
    </div>
  );
};

export default App;
