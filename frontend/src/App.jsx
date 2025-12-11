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
  
  // for audio recording
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // thread ids for chat management
  const threadIdRef = useRef(crypto.randomUUID());
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // handle audio transcription
  const handleVoiceInput = async () => {
    // if already recording, we stop
    if (isRecording) {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
      return;
    }

    // if not already recording, we start
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        // create audio blob from chunks
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        
        // display on input that it is transcribing
        setInput("🎧 Transcription en cours...");
        setIsLoading(true); // blocking input so user cannot write at the same time

        // send blob to backend for transcription
        const formData = new FormData();
        formData.append("file", audioBlob, "voice.webm");

        try {
          const response = await fetch('http://localhost:8000/transcribe', {
            method: 'POST',
            body: formData,
          });
          
          const data = await response.json();
          if (data.text) {
            setInput(data.text); // get transcribed text into input
          } else {
            console.error("Erreur transcription:", data.error);
            setInput(""); 
          }
        } catch (err) {
          console.error(err);
          setInput("");
        } finally {
          setIsLoading(false);
          // stop all media tracks
          stream.getTracks().forEach(track => track.stop());
        }
      };

      mediaRecorder.start();
      setIsRecording(true);

    } catch (err) {
      alert("Impossible d'accéder au micro : " + err.message);
    }
  };

  // chat
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
          
          {/* microphone */}
          <button 
            type="button" 
            className={`icon-btn ${isRecording ? 'recording' : ''}`}
            onClick={handleVoiceInput}
            title="Maintenir pour parler"
          >
            {isRecording ? '⏹️' : '🎙️'}
          </button>

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={isRecording ? "Écoute en cours..." : "Posez votre question..."}
            disabled={isLoading || isRecording}
          />
          <button type="submit" className="send-btn" disabled={isLoading || !input.trim() || isRecording}>
            ➤
          </button>
        </form>

      </div>
    </div>
  )
}

export default App