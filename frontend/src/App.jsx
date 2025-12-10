import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      content: 'Bonjour ! Je suis votre sommelier personnel. Comment puis-je vous aider aujourd\'hui ?' 
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const threadIdRef = useRef(crypto.randomUUID());
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    
    // message from user
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // call api from backend
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userMessage,
          thread_id: threadIdRef.current 
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      // dots to show assistant is typing
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const text = decoder.decode(value, { stream: true });
        
        // update assistant message with streamed text
        setMessages(prev => {
          const newMessages = [...prev];
          const lastIndex = newMessages.length - 1;
          const lastMessage = newMessages[lastIndex];

          newMessages[lastIndex] = {
            ...lastMessage,
            content: lastMessage.content + text
          };
          
          return newMessages;
        });
      }

    } catch (error) {
      console.error(error);
      setMessages(prev => {
          const newMessages = [...prev];
          const lastIndex = newMessages.length - 1;
          newMessages[lastIndex] = {
              ...newMessages[lastIndex],
              content: "**Erreur** : Impossible de contacter le sommelier."
          };
          return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-background">
      <div className="mobile-container">
        
        {/* HEADER */}
        <header className="chat-header">
          <div className="avatar-circle">🍷</div>
          <div className="header-info">
            <h1>Sommelier Privé</h1>
            <p><span className="dot"></span> En ligne • Valais</p>
          </div>
        </header>

        {/* MESSAGES AREA */}
        <div className="messages-area">
          {messages.map((msg, index) => (
            <div key={index} className={`message-row ${msg.role}`}>
              <div className="bubble">
                
              
                {msg.role === 'assistant' && msg.content === '' ? (
                  // if assistant message empty it means it is generating the answer
                  <div className="typing-indicator">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                ) : (
                  // markdown text since assistant send markdown
                  <ReactMarkdown 
                    components={{
                      a: ({node, ...props}) => <a target="_blank" rel="noopener noreferrer" {...props} />
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                )}

              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <form className="input-area" onSubmit={handleSubmit}>
          <button type="button" className="icon-btn">🎙️</button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Posez votre question..."
            disabled={isLoading}
          />
          <button type="submit" className="send-btn" disabled={isLoading || !input.trim()}>
            ➤
          </button>
        </form>

      </div>
    </div>
  )
}

export default App