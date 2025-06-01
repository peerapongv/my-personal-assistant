import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Paper, 
  Typography, 
  Container, 
  CircularProgress,
  IconButton,
  Divider
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ReactMarkdown from 'react-markdown';
import { generateResponse } from '../../services/api';

// Message component to display individual chat messages
const Message = ({ message, isUser }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        mb: 2,
      }}
    >
      <Paper
        elevation={1}
        sx={{
          p: 2,
          maxWidth: '80%',
          backgroundColor: isUser ? '#e3f2fd' : '#f5f5f5',
          borderRadius: 2,
        }}
      >
        {isUser ? (
          <Typography variant="body1">{message}</Typography>
        ) : (
          <Box sx={{ '& p': { m: 0 } }}>
            <ReactMarkdown>{message}</ReactMarkdown>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message to chat
    const userMessage = input;
    setMessages((prev) => [...prev, { text: userMessage, isUser: true }]);
    setInput('');
    setIsLoading(true);

    try {
      // Call API to get response
      const response = await generateResponse(userMessage);
      
      // Add assistant response to chat
      setMessages((prev) => [...prev, { text: response.text, isUser: false }]);
    } catch (error) {
      console.error('Error getting response:', error);
      setMessages((prev) => [
        ...prev,
        { text: 'Sorry, I encountered an error. Please try again.', isUser: false },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Container maxWidth="md" sx={{ height: '100vh', display: 'flex', flexDirection: 'column', py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        My Personal Assistant
      </Typography>
      <Divider sx={{ mb: 2 }} />
      
      {/* Messages container */}
      <Box sx={{ flexGrow: 1, overflow: 'auto', mb: 2, p: 2 }}>
        {messages.length === 0 ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <Typography variant="body1" color="text.secondary">
              Start a conversation with your My Personal Assistant
            </Typography>
          </Box>
        ) : (
          messages.map((message, index) => (
            <Message key={index} message={message.text} isUser={message.isUser} />
          ))
        )}
        <div ref={messagesEndRef} />
      </Box>
      
      {/* Input area */}
      <Paper
        elevation={3}
        component="form"
        sx={{ p: 2, display: 'flex', alignItems: 'center' }}
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
      >
        <TextField
          fullWidth
          multiline
          maxRows={4}
          placeholder="Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          variant="outlined"
          sx={{ mr: 1 }}
        />
        <IconButton 
          color="primary" 
          onClick={handleSend} 
          disabled={isLoading || !input.trim()}
        >
          {isLoading ? <CircularProgress size={24} /> : <SendIcon />}
        </IconButton>
      </Paper>
    </Container>
  );
};

export default ChatInterface;
