# Phase 4: User Interface & Experience - Detailed Implementation Guide

## Week 23-24: Web Interface Foundation

### Implementation Steps

1. Next.js Application Setup
```typescript
// pages/_app.tsx
import type { AppProps } from 'next/app'
import { ChakraProvider } from '@chakra-ui/react'
import { theme } from '../theme'

function AriaApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider theme={theme}>
      <Component {...pageProps} />
    </ChakraProvider>
  )
}

export default AriaApp
```

2. Core Components
```typescript
// components/Chat/ChatInterface.tsx
import { Box, Flex, VStack } from '@chakra-ui/react'
import { useState, useEffect } from 'react'
import { Message } from '../../types'

interface ChatInterfaceProps {
  onSendMessage: (message: string) => Promise<void>
  messages: Message[]
  isTyping: boolean
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  onSendMessage,
  messages,
  isTyping
}) => {
  const [input, setInput] = useState('')

  const handleSend = async () => {
    if (!input.trim()) return
    await onSendMessage(input)
    setInput('')
  }

  return (
    <Flex direction="column" h="100vh" p={4}>
      <VStack flex={1} spacing={4} overflowY="auto">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {isTyping && <TypingIndicator />}
      </VStack>
      <MessageInput
        value={input}
        onChange={setInput}
        onSend={handleSend}
      />
    </Flex>
  )
}
```

3. State Management
```typescript
// store/chatStore.ts
import create from 'zustand'
import { Message, ChatState } from '../types'

interface ChatStore {
  messages: Message[]
  isTyping: boolean
  addMessage: (message: Message) => void
  setTyping: (typing: boolean) => void
  clearMessages: () => void
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  isTyping: false,
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message]
    })),
  setTyping: (typing) =>
    set(() => ({
      isTyping: typing
    })),
  clearMessages: () =>
    set(() => ({
      messages: []
    }))
}))
```

## Week 25-26: Advanced UI Features

### Implementation Details

1. Memory Visualization
```typescript
// components/Memory/MemoryGraph.tsx
import { useEffect, useRef } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { MemoryNode, MemoryLink } from '../../types'

interface MemoryGraphProps {
  nodes: MemoryNode[]
  links: MemoryLink[]
  onNodeClick: (node: MemoryNode) => void
}

export const MemoryGraph: React.FC<MemoryGraphProps> = ({
  nodes,
  links,
  onNodeClick
}) => {
  const graphRef = useRef()

  useEffect(() => {
    // Graph initialization and configuration
    if (graphRef.current) {
      graphRef.current.d3Force('charge').strength(-120)
      graphRef.current.d3Force('link').distance(70)
    }
  }, [])

  return (
    <ForceGraph2D
      ref={graphRef}
      graphData={{ nodes, links }}
      nodeAutoColorBy="group"
      nodeLabel="label"
      onNodeClick={onNodeClick}
      linkDirectionalParticles={2}
    />
  )
}
```

2. Emotion Dashboard
```typescript
// components/Dashboard/EmotionDashboard.tsx
import { Box, Grid, Text } from '@chakra-ui/react'
import { LineChart, PieChart } from 'recharts'
import { EmotionData } from '../../types'

interface EmotionDashboardProps {
  emotionHistory: EmotionData[]
  currentEmotion: EmotionData
}

export const EmotionDashboard: React.FC<EmotionDashboardProps> = ({
  emotionHistory,
  currentEmotion
}) => {
  return (
    <Grid templateColumns="repeat(2, 1fr)" gap={6} p={4}>
      <Box>
        <Text fontSize="xl" mb={4}>Emotion Trends</Text>
        <LineChart
          data={emotionHistory}
          width={500}
          height={300}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          {/* Chart configuration */}
        </LineChart>
      </Box>
      <Box>
        <Text fontSize="xl" mb={4}>Current Emotional State</Text>
        <PieChart width={400} height={300}>
          {/* Chart configuration */}
        </PieChart>
      </Box>
    </Grid>
  )
}
```

## Week 27-28: Desktop Application

### Implementation Guide

1. Tauri Application Setup
```rust
// src-tauri/src/main.rs
#![cfg_attr(all(not(debug_assertions), target_os = "windows"), windows_subsystem = "windows")]

use tauri::{
    CustomMenuItem, Manager, SystemTray, SystemTrayEvent,
    SystemTrayMenu, SystemTrayMenuItem
};

fn main() {
    let tray_menu = SystemTrayMenu::new()
        .add_item(CustomMenuItem::new("show".to_string(), "Show ARIA"))
        .add_native_item(SystemTrayMenuItem::Separator)
        .add_item(CustomMenuItem::new("quit".to_string(), "Quit"));

    let system_tray = SystemTray::new().with_menu(tray_menu);

    tauri::Builder::default()
        .system_tray(system_tray)
        .on_system_tray_event(|app, event| match event {
            SystemTrayEvent::MenuItemClick { id, .. } => {
                match id.as_str() {
                    "show" => {
                        let window = app.get_window("main").unwrap();
                        window.show().unwrap();
                    }
                    "quit" => {
                        app.exit(0);
                    }
                    _ => {}
                }
            }
            _ => {}
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

2. Global Hotkey System
```rust
// src-tauri/src/hotkeys.rs
use tauri::GlobalShortcutManager;

pub fn register_global_hotkeys(app: &tauri::App) -> Result<(), Box<dyn std::error::Error>> {
    let mut shortcut_manager = app.global_shortcut_manager();
    let window = app.get_window("main").unwrap();

    shortcut_manager.register("CommandOrControl+Shift+A", move || {
        if window.is_visible().unwrap() {
            window.hide().unwrap();
        } else {
            window.show().unwrap();
            window.set_focus().unwrap();
        }
    })?;

    Ok(())
}
```

## Week 29-30: Testing & Optimization

### Testing Implementation

1. UI Component Testing
```typescript
// __tests__/components/ChatInterface.test.tsx
import { render, fireEvent, waitFor } from '@testing-library/react'
import { ChatInterface } from '../../components/Chat/ChatInterface'

describe('ChatInterface', () => {
  const mockOnSendMessage = jest.fn()
  const mockMessages = [
    { id: '1', content: 'Hello', sender: 'user' },
    { id: '2', content: 'Hi there!', sender: 'assistant' }
  ]

  it('renders messages correctly', () => {
    const { getByText } = render(
      <ChatInterface
        onSendMessage={mockOnSendMessage}
        messages={mockMessages}
        isTyping={false}
      />
    )

    expect(getByText('Hello')).toBeInTheDocument()
    expect(getByText('Hi there!')).toBeInTheDocument()
  })

  it('handles message sending', async () => {
    const { getByPlaceholderText, getByRole } = render(
      <ChatInterface
        onSendMessage={mockOnSendMessage}
        messages={[]}
        isTyping={false}
      />
    )

    const input = getByPlaceholderText('Type a message...')
    const sendButton = getByRole('button', { name: /send/i })

    fireEvent.change(input, { target: { value: 'Test message' } })
    fireEvent.click(sendButton)

    await waitFor(() => {
      expect(mockOnSendMessage).toHaveBeenCalledWith('Test message')
    })
  })
})
```

2. Performance Optimization
```typescript
// utils/performance.ts
import { useCallback, useRef, useEffect } from 'react'

export const useDebounce = <T extends (...args: any[]) => any>(
  callback: T,
  delay: number
) => {
  const timeoutRef = useRef<NodeJS.Timeout>()

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  return useCallback(
    (...args: Parameters<T>) => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }

      timeoutRef.current = setTimeout(() => {
        callback(...args)
      }, delay)
    },
    [callback, delay]
  )
}

export const measurePerformance = (label: string) => {
  const start = performance.now()
  return () => {
    const duration = performance.now() - start
    console.log(`${label}: ${duration.toFixed(2)}ms`)
  }
}
```