# Phase 2: AI Diagnosis Module - Detailed Implementation Guide

## 🎯 Phase Overview
**Duration**: 3 weeks (Week 3-5)
**Goal**: Build a functional AI-powered diagnosis system with chat interface, image analysis, and medical logic

---

## 📅 Week 3: Chat Interface Implementation

### Day 1-2: Chat UI Components

#### Step 1: Create Chat Screen Structure
```typescript
// app/(tabs)/chat/index.tsx
import React, { useState, useEffect } from 'react';
import { View, FlatList, KeyboardAvoidingView, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useUser } from '@clerk/clerk-expo';
import { MessageBubble } from '../../../components/chat/MessageBubble';
import { ChatInput } from '../../../components/chat/ChatInput';
import { TypingIndicator } from '../../../components/chat/TypingIndicator';
import { useChatStore } from '../../../store/chatStore';

export default function ChatScreen() {
  const { user } = useUser();
  const { messages, isTyping, sendMessage } = useChatStore();

  return (
    <SafeAreaView className="flex-1 bg-white">
      <KeyboardAvoidingView 
        className="flex-1" 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <FlatList
          data={messages}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <MessageBubble message={item} />}
          className="flex-1 px-4"
          showsVerticalScrollIndicator={false}
        />
        {isTyping && <TypingIndicator />}
        <ChatInput onSendMessage={sendMessage} />
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}
```

#### Step 2: Message Bubble Component
```typescript
// components/chat/MessageBubble.tsx
import React from 'react';
import { View, Text, Image } from 'react-native';
import { format } from 'date-fns';
import { Message } from '../../types/chat';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  
  return (
    <View className={`flex-row mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <View className={`max-w-[80%] rounded-2xl px-4 py-3 ${
        isUser ? 'bg-blue-500' : 'bg-gray-100'
      }`}>
        {message.type === 'image' && message.imageUri && (
          <Image 
            source={{ uri: message.imageUri }} 
            className="w-48 h-48 rounded-xl mb-2"
            resizeMode="cover"
          />
        )}
        
        <Text className={`text-base ${isUser ? 'text-white' : 'text-gray-800'}`}>
          {message.content}
        </Text>
        
        {message.confidence && (
          <View className="mt-2 px-2 py-1 bg-green-100 rounded-lg">
            <Text className="text-green-800 text-sm font-medium">
              Confidence: {message.confidence}%
            </Text>
          </View>
        )}
        
        <Text className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
          {format(new Date(message.timestamp), 'HH:mm')}
        </Text>
      </View>
    </View>
  );
};
```

#### Step 3: Chat Input Component
```typescript
// components/chat/ChatInput.tsx
import React, { useState } from 'react';
import { View, TextInput, Pressable, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { Message } from '../../types/chat';

interface ChatInputProps {
  onSendMessage: (message: Partial<Message>) => void;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage }) => {
  const [text, setText] = useState('');

  const sendTextMessage = () => {
    if (text.trim()) {
      onSendMessage({
        type: 'text',
        content: text,
        sender: 'user'
      });
      setText('');
    }
  };

  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'Camera roll permission is required');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled) {
      onSendMessage({
        type: 'image',
        content: 'Uploaded an image for analysis',
        imageUri: result.assets[0].uri,
        sender: 'user'
      });
    }
  };

  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'Camera permission is required');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled) {
      onSendMessage({
        type: 'image',
        content: 'Captured an image for analysis',
        imageUri: result.assets[0].uri,
        sender: 'user'
      });
    }
  };

  return (
    <View className="flex-row items-center px-4 py-3 bg-white border-t border-gray-200">
      <Pressable onPress={pickImage} className="mr-3">
        <Ionicons name="image-outline" size={24} color="#6B7280" />
      </Pressable>
      
      <Pressable onPress={takePhoto} className="mr-3">
        <Ionicons name="camera-outline" size={24} color="#6B7280" />
      </Pressable>
      
      <TextInput
        value={text}
        onChangeText={setText}
        placeholder="Describe your symptoms..."
        className="flex-1 border border-gray-300 rounded-full px-4 py-2 mr-3"
        multiline
        maxHeight={100}
      />
      
      <Pressable 
        onPress={sendTextMessage}
        className="bg-blue-500 rounded-full p-2"
        disabled={!text.trim()}
      >
        <Ionicons name="send" size={20} color="white" />
      </Pressable>
    </View>
  );
};
```

### Day 3-4: Real-time Messaging Setup

#### Step 4: Supabase Real-time Configuration
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';
import { Database } from '../types/supabase';

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient<Database>(supabaseUrl, supabaseKey, {
  auth: {
    storage: {
      getItem: (key: string) => {
        // Use Expo SecureStore for auth tokens
        return Promise.resolve(null);
      },
      setItem: (key: string, value: string) => {
        // Use Expo SecureStore for auth tokens
        return Promise.resolve();
      },
      removeItem: (key: string) => {
        // Use Expo SecureStore for auth tokens
        return Promise.resolve();
      },
    },
  },
});
```

#### Step 5: Chat Store with Zustand
```typescript
// store/chatStore.ts
import { create } from 'zustand';
import { supabase } from '../lib/supabase';
import { Message, Consultation } from '../types/chat';
import { generateAIResponse } from '../services/aiService';

interface ChatState {
  messages: Message[];
  isTyping: boolean;
  currentConsultation: Consultation | null;
  sendMessage: (message: Partial<Message>) => Promise<void>;
  loadMessages: (consultationId: string) => Promise<void>;
  startNewConsultation: () => Promise<string>;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isTyping: false,
  currentConsultation: null,

  sendMessage: async (message: Partial<Message>) => {
    const fullMessage: Message = {
      id: Date.now().toString(),
      consultationId: get().currentConsultation?.id || '',
      content: message.content || '',
      type: message.type || 'text',
      sender: message.sender || 'user',
      timestamp: new Date().toISOString(),
      imageUri: message.imageUri,
    };

    // Add user message
    set(state => ({
      messages: [...state.messages, fullMessage]
    }));

    // Save to database
    await supabase
      .from('messages')
      .insert([{
        consultation_id: fullMessage.consultationId,
        content: fullMessage.content,
        type: fullMessage.type,
        sender: fullMessage.sender,
        image_uri: fullMessage.imageUri,
      }]);

    // Show typing indicator
    set({ isTyping: true });

    // Generate AI response
    try {
      const aiResponse = await generateAIResponse(fullMessage, get().messages);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        consultationId: fullMessage.consultationId,
        content: aiResponse.content,
        type: 'text',
        sender: 'ai',
        timestamp: new Date().toISOString(),
        confidence: aiResponse.confidence,
      };

      set(state => ({
        messages: [...state.messages, aiMessage],
        isTyping: false
      }));

      // Save AI response
      await supabase
        .from('messages')
        .insert([{
          consultation_id: aiMessage.consultationId,
          content: aiMessage.content,
          type: aiMessage.type,
          sender: aiMessage.sender,
          confidence: aiMessage.confidence,
        }]);

    } catch (error) {
      console.error('AI response error:', error);
      set({ isTyping: false });
    }
  },

  loadMessages: async (consultationId: string) => {
    const { data, error } = await supabase
      .from('messages')
      .select('*')
      .eq('consultation_id', consultationId)
      .order('created_at', { ascending: true });

    if (data && !error) {
      const messages: Message[] = data.map(msg => ({
        id: msg.id,
        consultationId: msg.consultation_id,
        content: msg.content,
        type: msg.type as 'text' | 'image',
        sender: msg.sender as 'user' | 'ai',
        timestamp: msg.created_at,
        imageUri: msg.image_uri,
        confidence: msg.confidence,
      }));

      set({ messages });
    }
  },

  startNewConsultation: async () => {
    const { data, error } = await supabase
      .from('consultations')
      .insert([{
        symptoms: {},
        ai_diagnosis: {},
        status: 'active'
      }])
      .select()
      .single();

    if (data && !error) {
      set({ 
        currentConsultation: data,
        messages: [] 
      });
      return data.id;
    }

    throw new Error('Failed to create consultation');
  },
}));
```

### Day 5-7: Symptom Input Forms

#### Step 6: Symptom Input Component
```typescript
// components/chat/SymptomInput.tsx
import React, { useState } from 'react';
import { View, Text, ScrollView, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const SYMPTOM_CATEGORIES = {
  general: ['Fever', 'Fatigue', 'Weight Loss', 'Night Sweats'],
  respiratory: ['Cough', 'Shortness of Breath', 'Chest Pain', 'Wheezing'],
  gastrointestinal: ['Nausea', 'Vomiting', 'Diarrhea', 'Abdominal Pain'],
  neurological: ['Headache', 'Dizziness', 'Confusion', 'Numbness'],
  musculoskeletal: ['Joint Pain', 'Muscle Pain', 'Stiffness', 'Swelling'],
  skin: ['Rash', 'Itching', 'Discoloration', 'Bumps'],
};

interface SymptomInputProps {
  onSymptomsSelected: (symptoms: string[]) => void;
}

export const SymptomInput: React.FC<SymptomInputProps> = ({ onSymptomsSelected }) => {
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);

  const toggleSymptom = (symptom: string) => {
    const updated = selectedSymptoms.includes(symptom)
      ? selectedSymptoms.filter(s => s !== symptom)
      : [...selectedSymptoms, symptom];
    
    setSelectedSymptoms(updated);
    onSymptomsSelected(updated);
  };

  return (
    <View className="p-4">
      <Text className="text-xl font-bold mb-4">Select Your Symptoms</Text>
      
      <ScrollView showsVerticalScrollIndicator={false}>
        {Object.entries(SYMPTOM_CATEGORIES).map(([category, symptoms]) => (
          <View key={category} className="mb-4">
            <Pressable
              onPress={() => setExpandedCategory(
                expandedCategory === category ? null : category
              )}
              className="flex-row items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <Text className="text-lg font-semibold capitalize">
                {category.replace(/([A-Z])/g, ' $1')}
              </Text>
              <Ionicons
                name={expandedCategory === category ? 'chevron-up' : 'chevron-down'}
                size={20}
                color="#6B7280"
              />
            </Pressable>
            
            {expandedCategory === category && (
              <View className="mt-2">
                {symptoms.map(symptom => (
                  <Pressable
                    key={symptom}
                    onPress={() => toggleSymptom(symptom)}
                    className={`flex-row items-center p-3 rounded-lg mb-1 ${
                      selectedSymptoms.includes(symptom)
                        ? 'bg-blue-100 border border-blue-300'
                        : 'bg-white border border-gray-200'
                    }`}
                  >
                    <View className={`w-6 h-6 rounded-full border-2 mr-3 items-center justify-center ${
                      selectedSymptoms.includes(symptom)
                        ? 'bg-blue-500 border-blue-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedSymptoms.includes(symptom) && (
                        <Ionicons name="checkmark" size={16} color="white" />
                      )}
                    </View>
                    <Text className={`flex-1 ${
                      selectedSymptoms.includes(symptom) ? 'text-blue-700 font-medium' : 'text-gray-700'
                    }`}>
                      {symptom}
                    </Text>
                  </Pressable>
                ))}
              </View>
            )}
          </View>
        ))}
      </ScrollView>
      
      {selectedSymptoms.length > 0 && (
        <View className="mt-4 p-3 bg-blue-50 rounded-lg">
          <Text className="font-medium text-blue-800">
            Selected Symptoms ({selectedSymptoms.length}):
          </Text>
          <Text className="text-blue-600 mt-1">
            {selectedSymptoms.join(', ')}
          </Text>
        </View>
      )}
    </View>
  );
};
```

---

## 📅 Week 4: AI Integration

### Day 8-10: OpenAI API Setup

#### Step 7: AI Service Configuration
```typescript
// services/aiService.ts
import OpenAI from 'openai';
import { Message } from '../types/chat';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export interface AIResponse {
  content: string;
  confidence: number;
  followUpQuestions?: string[];
  urgencyLevel: 'low' | 'medium' | 'high' | 'emergency';
}

const MEDICAL_SYSTEM_PROMPT = `
You are a medical AI assistant designed to help users understand their symptoms and provide preliminary guidance. 

IMPORTANT DISCLAIMERS:
- You are NOT a replacement for professional medical advice
- Always recommend consulting with healthcare professionals
- Never provide definitive diagnoses
- Focus on education and guidance

RESPONSE FORMAT:
- Provide clear, empathetic responses
- Include confidence percentages (0-100%)
- Suggest follow-up questions when appropriate
- Categorize urgency levels: low, medium, high, emergency
- Use simple, non-technical language

MEDICAL KNOWLEDGE:
- Base responses on established medical knowledge
- Consider symptom combinations and patterns
- Account for common vs. rare conditions
- Always err on the side of caution
`;

export const generateAIResponse = async (
  userMessage: Message,
  conversationHistory: Message[]
): Promise<AIResponse> => {
  try {
    const messages = [
      { role: 'system' as const, content: MEDICAL_SYSTEM_PROMPT },
      ...conversationHistory.slice(-10).map(msg => ({
        role: msg.sender === 'user' ? 'user' as const : 'assistant' as const,
        content: msg.content
      })),
      { role: 'user' as const, content: userMessage.content }
    ];

    // Handle image analysis if present
    if (userMessage.type === 'image' && userMessage.imageUri) {
      return await analyzeImageWithAI(userMessage.imageUri, conversationHistory);
    }

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages,
      temperature: 0.3,
      max_tokens: 500,
    });

    const response = completion.choices[0]?.message?.content || '';
    
    // Extract confidence and urgency from response
    const confidence = extractConfidence(response);
    const urgencyLevel = determineUrgency(response, userMessage.content);
    const followUpQuestions = generateFollowUpQuestions(response);

    return {
      content: response,
      confidence,
      urgencyLevel,
      followUpQuestions,
    };

  } catch (error) {
    console.error('AI Service Error:', error);
    return {
      content: "I'm having trouble processing your request right now. Please try again or consult with a healthcare professional if this is urgent.",
      confidence: 0,
      urgencyLevel: 'medium',
    };
  }
};

const analyzeImageWithAI = async (
  imageUri: string,
  conversationHistory: Message[]
): Promise<AIResponse> => {
  try {
    const base64Image = await convertImageToBase64(imageUri);
    
    const response = await openai.chat.completions.create({
      model: 'gpt-4-vision-preview',
      messages: [
        {
          role: 'system',
          content: `${MEDICAL_SYSTEM_PROMPT}
          
          You are now analyzing a medical image. Focus on:
          - Visible symptoms or conditions
          - Recommending professional evaluation
          - Avoiding definitive diagnoses
          - Suggesting when immediate care is needed`
        },
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: 'Please analyze this medical image and provide guidance based on what you observe.'
            },
            {
              type: 'image_url',
              image_url: {
                url: `data:image/jpeg;base64,${base64Image}`,
                detail: 'high'
              }
            }
          ]
        }
      ],
      max_tokens: 500,
      temperature: 0.2,
    });

    const content = response.choices[0]?.message?.content || '';
    const confidence = extractConfidence(content);
    const urgencyLevel = determineUrgency(content, 'image analysis');

    return {
      content,
      confidence,
      urgencyLevel,
    };

  } catch (error) {
    console.error('Image Analysis Error:', error);
    return {
      content: "I'm unable to analyze the image right now. Please consult with a healthcare professional for proper evaluation.",
      confidence: 0,
      urgencyLevel: 'medium',
    };
  }
};

// Utility functions
const convertImageToBase64 = async (uri: string): Promise<string> => {
  const response = await fetch(uri);
  const blob = await response.blob();
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = (reader.result as string).split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
};

const extractConfidence = (response: string): number => {
  const confidenceMatch = response.match(/confidence[:\s]*(\d+)%?/i);
  return confidenceMatch ? parseInt(confidenceMatch[1]) : 70;
};

const determineUrgency = (response: string, userInput: string): 'low' | 'medium' | 'high' | 'emergency' => {
  const emergencyKeywords = ['emergency', 'urgent', 'severe', 'immediately', 'call 911'];
  const highKeywords = ['serious', 'concerning', 'worrisome', 'soon'];
  const lowKeywords = ['mild', 'minor', 'common', 'routine'];

  const text = (response + ' ' + userInput).toLowerCase();

  if (emergencyKeywords.some(keyword => text.includes(keyword))) return 'emergency';
  if (highKeywords.some(keyword => text.includes(keyword))) return 'high';
  if (lowKeywords.some(keyword => text.includes(keyword))) return 'low';
  
  return 'medium';
};

const generateFollowUpQuestions = (response: string): string[] => {
  // Simple implementation - can be enhanced with AI
  const questions = [
    "How long have you been experiencing these symptoms?",
    "Have you noticed any patterns or triggers?",
    "Are you currently taking any medications?",
    "Do you have any relevant medical history?",
    "On a scale of 1-10, how would you rate your discomfort?"
  ];
  
  return questions.slice(0, 2); // Return 2 relevant questions
};
```

### Day 11-12: Medical Prompt Templates

#### Step 8: Enhanced Medical Prompts
```typescript
// services/medicalPrompts.ts
export const SPECIALIZED_PROMPTS = {
  symptomAnalysis: `
    Analyze the following symptoms and provide guidance:
    
    ANALYSIS FRAMEWORK:
    1. Symptom severity assessment
    2. Possible conditions (common first, then rare)
    3. Red flags that require immediate attention
    4. Self-care recommendations
    5. When to seek professional care
    
    RESPONSE STRUCTURE:
    - Summary of symptoms
    - Likely explanations (with confidence %)
    - Recommended actions
    - Urgency level
    - Follow-up questions
  `,
  
  imageAnalysis: `
    Analyze this medical image professionally:
    
    OBSERVATION GUIDELINES:
    1. Describe what you observe objectively
    2. Note any concerning features
    3. Compare to normal presentations
    4. Suggest possible conditions (broad categories)
    5. Emphasize need for professional evaluation
    
    AVOID:
    - Definitive diagnoses
    - Overly technical terminology
    - Dismissing concerns
    - Providing treatment advice
  `,
  
  followUp: `
    Based on our conversation, ask relevant follow-up questions:
    
    QUESTION CATEGORIES:
    1. Symptom progression
    2. Associated symptoms
    3. Medical history
    4. Lifestyle factors
    5. Current treatments
    
    Keep questions:
    - Clear and specific
    - Medically relevant
    - Easy to understand
    - Focused on 2-3 key areas
  `,
  
  emergencyAssessment: `
    Assess if this situation requires emergency care:
    
    EMERGENCY INDICATORS:
    - Severe chest pain
    - Difficulty breathing
    - Loss of consciousness
    - Severe bleeding
    - Signs of stroke/heart attack
    - Severe allergic reactions
    - High fever with confusion
    - Severe abdominal pain
    
    IF EMERGENCY: Immediately advise calling 911/emergency services
    IF URGENT: Recommend same-day medical attention
    IF ROUTINE: Suggest scheduling appointment within days/weeks
  `
};

export const generateContextualPrompt = (
  messageType: 'symptom' | 'image' | 'followup' | 'emergency',
  context: {
    symptoms?: string[];
    duration?: string;
    severity?: number;
    medicalHistory?: string[];
  }
): string => {
  const basePrompt = SPECIALIZED_PROMPTS[messageType === 'symptom' ? 'symptomAnalysis' : 
                                      messageType === 'image' ? 'imageAnalysis' :
                                      messageType === 'followup' ? 'followUp' : 'emergencyAssessment'];
  
  let contextualPrompt = basePrompt + '\n\nCONTEXT:\n';
  
  if (context.symptoms) {
    contextualPrompt += `- Reported symptoms: ${context.symptoms.join(', ')}\n`;
  }
  
  if (context.duration) {
    contextualPrompt += `- Duration: ${context.duration}\n`;
  }
  
  if (context.severity) {
    contextualPrompt += `- Severity (1-10): ${context.severity}\n`;
  }
  
  if (context.medicalHistory) {
    contextualPrompt += `- Medical history: ${context.medicalHistory.join(', ')}\n`;
  }
  
  return contextualPrompt;
};
```

### Day 13-14: Confidence Scoring System

#### Step 9: Confidence and Accuracy Tracking
```typescript
// services/confidenceService.ts
export interface ConfidenceMetrics {
  overallConfidence: number;
  factorBreakdown: {
    symptomClarity: number;
    medicalHistory: number;
    imageQuality?: number;
    responseRelevance: number;
  };
  recommendations: string[];
}

export const calculateConfidenceScore = (
  userInput: string,
  conversationHistory: Message[],
  hasImage: boolean = false
): ConfidenceMetrics => {
  
  // Analyze symptom clarity
  const symptomClarity = analyzeSymptomClarity(userInput);
  
  // Check medical history completeness
  const medicalHistory = assessMedicalHistoryCompleteness(conversationHistory);
  
  // Evaluate image quality if present
  const imageQuality = hasImage ? 75 : undefined; // Placeholder - would use actual image analysis
  
  // Assess response relevance based on conversation flow
  const responseRelevance = assessResponseRelevance(conversationHistory);
  
  // Calculate overall confidence
  const factors = [symptomClarity, medicalHistory, responseRelevance];
  if (imageQuality) factors.push(imageQuality);
  
  const overallConfidence = Math.round(
    factors.reduce((sum, score) => sum + score, 0) / factors.length
  );
  
  // Generate recommendations for improving confidence
  const recommendations = generateConfidenceRecommendations({
    symptomClarity,
    medicalHistory,
    imageQuality,
    responseRelevance
  });
  
  return {
    overallConfidence,
    factorBreakdown: {
      symptomClarity,
      medicalHistory,
      imageQuality,
      responseRelevance
    },
    recommendations
  };
};

const analyzeSymptomClarity = (input: string): number => {
  let score = 50; // Base score
  
  // Check for specific symptoms
  const symptomKeywords = ['pain', 'fever', 'headache', 'nausea', 'fatigue'];
  const foundSymptoms = symptomKeywords.filter(keyword => 
    input.toLowerCase().includes(keyword)
  ).length;
  score += foundSymptoms * 10;
  
  // Check for duration indicators
  const durationKeywords = ['hours', 'days', 'weeks', 'months', 'since', 'for'];
  if (durationKeywords.some(keyword => input.toLowerCase().includes(keyword))) {
    score += 15;
  }
  
  // Check for severity indicators
  const severityKeywords = ['severe', 'mild', 'moderate', 'intense', 'slight'];
  if (severityKeywords.some(keyword => input.toLowerCase().includes(keyword))) {
    score += 15;
  }
  
  return Math.min(score, 100);
};

const assessMedicalHistoryCompleteness = (history: Message[]): number => {
  let score = 30; // Base score
  
  const historyKeywords = [
    'medication', 'allergy', 'surgery', 'condition', 'family history',
    'previous', 'diagnosed', 'treatment', 'doctor', 'hospital'
  ];
  
  const historyMentions = history.filter(msg => 
    historyKeywords.some(keyword => 
      msg.content.toLowerCase().includes(keyword)
    )
  ).length;
  
  score += Math.min(historyMentions * 15, 70);
  
  return Math.min(score, 100);
};

const assessResponseRelevance = (history: Message[]): number => {
  if (history.length < 2) return 60;
  
  // Simple relevance check based on conversation flow
  const recentMessages = history.slice(-6);
  const medicalTerms = ['symptom', 'pain', 'treatment', 'diagnosis', 'medical', 'health'];
  
  const relevantMessages = recentMessages.filter(msg =>
    medicalTerms.some(term => msg.content.toLowerCase().includes(term))
  ).length;
  
  const relevanceScore = (relevantMessages / recentMessages.length) * 100;
  return Math.round(relevanceScore);
};

const generateConfidenceRecommendations = (factors: {
  symptomClarity: number;
  medicalHistory: number;
  imageQuality?: number;
  responseRelevance: number;
}): string[] => {
  const recommendations: string[] = [];
  
  if (factors.symptomClarity < 70) {
    recommendations.push("Provide more specific details about your symptoms (duration, severity, location)");
  }
  
  if (factors.medicalHistory < 60) {
    recommendations.push("Share relevant medical history, current medications, or allergies");
  }
  
  if (factors.imageQuality && factors.imageQuality < 60) {
    recommendations.push("Consider taking a clearer photo with better lighting");
  }
  
  if (factors.responseRelevance < 70) {
    recommendations.push("Stay focused on health-related topics for better analysis");
  }
  
  return recommendations;
};
```

---

## 📅 Week 5: Medical Logic Implementation

### Day 15-17: Follow-up Question System

#### Step 10: Dynamic Question Generation
```typescript
// services/questionService.ts
export interface MedicalQuestion {
  id: string;
  question: string;
  type: 'multiple_choice' | 'scale' | 'text' | 'yes_no';
  options?: string[];
  category: 'symptoms' | 'history' | 'lifestyle' | 'severity';
  priority: 'high' | 'medium' | 'low';
}

export const generateFollowUpQuestions = (
  symptoms: string[],
  conversationHistory: Message[],
  currentDiagnosis?: string
): MedicalQuestion[] => {
  const questions: MedicalQuestion[] = [];
  const askedCategories = extractAskedCategories(conversationHistory);
  
  // Pain-related questions
  if (symptoms.some(s => s.toLowerCase().includes('pain'))) {
    if (!askedCategories.includes('pain_scale')) {
      questions.push({
        id: 'pain_scale',
        question: 'On a scale of 1-10, how would you rate your pain?',
        type: 'scale',
        category: 'severity',
        priority: 'high'
      });
    }
    
    if (!askedCategories.includes('pain_location')) {
      questions.push({
        id: 'pain_location',
        question: 'Can you describe exactly where the pain is located?',
        type: 'text',
        category: 'symptoms',
        priority: 'high'
      });
    }
  }
  
  // Fever-related questions
  if (symptoms.some(s => s.toLowerCase().includes('fever'))) {
    if (!askedCategories.includes('temperature')) {
      questions.push({
        id: 'temperature',
        question: 'Have you measured your temperature? If so, what was it?',
        type: 'text',
        category: 'symptoms',
        priority: 'high'
      });
    }
  }
  
  // Duration questions
  if (!askedCategories.includes('duration')) {
    questions.push({
      id: 'duration',
      question: 'How long have you been experiencing these symptoms?',
      type: 'multiple_choice',
      options: ['Less than 24 hours', '1-3 days', '4-7 days', 'More than a week'],
      category: 'symptoms',
      priority: 'high'
    });
  }
  
  // Medical history
  if (!askedCategories.includes('medications')) {
    questions.push({
      id: 'medications',
      question: 'Are you currently taking any medications or supplements?',
      type: 'yes_no',
      category: 'history',
      priority: 'medium'
    });
  }
  
  // Sort by priority and return top 3
  return questions
    .sort((a, b) => {
      const priorityOrder = { high: 3, medium: 2, low: 1 };
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    })
    .slice(0, 3);
};

const extractAskedCategories = (history: Message[]): string[] => {
  const categories: string[] = [];
  
  history.forEach(msg => {
    if (msg.sender === 'ai') {
      if (msg.content.toLowerCase().includes('scale') && msg.content.includes('pain')) {
        categories.push('pain_scale');
      }
      if (msg.content.toLowerCase().includes('where') && msg.content.includes('pain')) {
        categories.push('pain_location');
      }
      if (msg.content.toLowerCase().includes('temperature')) {
        categories.push('temperature');
      }
      if (msg.content.toLowerCase().includes('how long')) {
        categories.push('duration');
      }
      if (msg.content.toLowerCase().includes('medication')) {
        categories.push('medications');
      }
    }
  });
  
  return categories;
};

// Component for displaying follow-up questions
export const FollowUpQuestions: React.FC<{
  questions: MedicalQuestion[];
  onAnswerSelected: (questionId: string, answer: string) => void;
}> = ({ questions, onAnswerSelected }) => {
  return (
    <View className="p-4 bg-blue-50 rounded-lg m-4">
      <Text className="text-lg font-semibold text-blue-800 mb-3">
        Help me understand better:
      </Text>
      
      {questions.map(question => (
        <QuestionCard
          key={question.id}
          question={question}
          onAnswer={(answer) => onAnswerSelected(question.id, answer)}
        />
      ))}
    </View>
  );
};

const QuestionCard: React.FC<{
  question: MedicalQuestion;
  onAnswer: (answer: string) => void;
}> = ({ question, onAnswer }) => {
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  
  return (
    <View className="mb-4 p-3 bg-white rounded-lg border border-blue-200">
      <Text className="font-medium text-gray-800 mb-2">{question.question}</Text>
      
      {question.type === 'multiple_choice' && question.options && (
        <View>
          {question.options.map(option => (
            <Pressable
              key={option}
              onPress={() => {
                setSelectedAnswer(option);
                onAnswer(option);
              }}
              className={`p-2 rounded border mb-1 ${
                selectedAnswer === option
                  ? 'bg-blue-100 border-blue-300'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              <Text className={selectedAnswer === option ? 'text-blue-700' : 'text-gray-700'}>
                {option}
              </Text>
            </Pressable>
          ))}
        </View>
      )}
      
      {question.type === 'yes_no' && (
        <View className="flex-row gap-2">
          {['Yes', 'No'].map(option => (
            <Pressable
              key={option}
              onPress={() => {
                setSelectedAnswer(option);
                onAnswer(option);
              }}
              className={`flex-1 p-2 rounded border ${
                selectedAnswer === option
                  ? 'bg-blue-100 border-blue-300'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              <Text className={`text-center ${
                selectedAnswer === option ? 'text-blue-700' : 'text-gray-700'
              }`}>
                {option}
              </Text>
            </Pressable>
          ))}
        </View>
      )}
      
      {question.type === 'scale' && (
        <View className="flex-row justify-between items-center">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
            <Pressable
              key={num}
              onPress={() => {
                setSelectedAnswer(num.toString());
                onAnswer(num.toString());
              }}
              className={`w-8 h-8 rounded-full border items-center justify-center ${
                selectedAnswer === num.toString()
                  ? 'bg-blue-500 border-blue-500'
                  : 'bg-white border-gray-300'
              }`}
            >
              <Text className={`text-sm ${
                selectedAnswer === num.toString() ? 'text-white' : 'text-gray-700'
              }`}>
                {num}
              </Text>
            </Pressable>
          ))}
        </View>
      )}
    </View>
  );
};
```

### Day 18-19: Preliminary Diagnosis System

#### Step 11: Diagnosis Logic Implementation
```typescript
// services/diagnosisService.ts
export interface DiagnosisResult {
  primaryConditions: MedicalCondition[];
  differentialDiagnoses: MedicalCondition[];
  redFlags: string[];
  recommendations: Recommendation[];
  confidence: number;
  urgencyLevel: 'low' | 'medium' | 'high' | 'emergency';
}

export interface MedicalCondition {
  name: string;
  probability: number;
  description: string;
  commonSymptoms: string[];
  whenToSeekCare: string;
  selfCareOptions?: string[];
}

export interface Recommendation {
  type: 'self_care' | 'seek_care' | 'emergency' | 'follow_up';
  priority: 'high' | 'medium' | 'low';
  description: string;
  timeframe?: string;
}

export const generatePreliminaryDiagnosis = async (
  symptoms: string[],
  patientData: {
    age?: number;
    gender?: string;
    medicalHistory?: string[];
    currentMedications?: string[];
    duration?: string;
    severity?: number;
  },
  conversationHistory: Message[]
): Promise<DiagnosisResult> => {
  
  // Analyze symptoms using medical knowledge base
  const symptomAnalysis = analyzeSymptomCombinations(symptoms, patientData);
  
  // Generate possible conditions
  const possibleConditions = await generateConditionMatches(symptomAnalysis, patientData);
  
  // Assess urgency and red flags
  const { urgencyLevel, redFlags } = assessUrgency(symptoms, patientData);
  
  // Generate recommendations
  const recommendations = generateRecommendations(possibleConditions, urgencyLevel, patientData);
  
  // Calculate overall confidence
  const confidence = calculateDiagnosticConfidence(symptomAnalysis, patientData, conversationHistory);
  
  return {
    primaryConditions: possibleConditions.slice(0, 3),
    differentialDiagnoses: possibleConditions.slice(3, 6),
    redFlags,
    recommendations,
    confidence,
    urgencyLevel
  };
};

const analyzeSymptomCombinations = (
  symptoms: string[],
  patientData: any
): SymptomAnalysis => {
  const analysis: SymptomAnalysis = {
    primarySymptoms: [],
    associatedSymptoms: [],
    systemsInvolved: [],
    severity: patientData.severity || 5,
    duration: patientData.duration || 'unknown'
  };
  
  // Categorize symptoms by body systems
  const systemMapping = {
    respiratory: ['cough', 'shortness of breath', 'chest pain', 'wheezing'],
    gastrointestinal: ['nausea', 'vomiting', 'diarrhea', 'abdominal pain'],
    neurological: ['headache', 'dizziness', 'confusion', 'numbness'],
    musculoskeletal: ['joint pain', 'muscle pain', 'stiffness', 'swelling'],
    cardiovascular: ['chest pain', 'palpitations', 'shortness of breath'],
    general: ['fever', 'fatigue', 'weight loss', 'night sweats']
  };
  
  Object.entries(systemMapping).forEach(([system, systemSymptoms]) => {
    const matches = symptoms.filter(symptom =>
      systemSymptoms.some(sysSymptom =>
        symptom.toLowerCase().includes(sysSymptom.toLowerCase())
      )
    );
    
    if (matches.length > 0) {
      analysis.systemsInvolved.push(system);
      analysis.primarySymptoms.push(...matches);
    }
  });
  
  return analysis;
};

const generateConditionMatches = async (
  analysis: SymptomAnalysis,
  patientData: any
): Promise<MedicalCondition[]> => {
  const conditions: MedicalCondition[] = [];
  
  // Common condition patterns
  const conditionDatabase = {
    'Upper Respiratory Infection': {
      symptoms: ['cough', 'fever', 'fatigue', 'headache'],
      probability: 0.8,
      description: 'A common viral infection affecting the nose, throat, and sinuses.',
      selfCare: ['Rest', 'Fluids', 'Over-the-counter pain relievers'],
      seekCare: 'If symptoms worsen or persist beyond 10 days'
    },
    'Gastroenteritis': {
      symptoms: ['nausea', 'vomiting', 'diarrhea', 'abdominal pain'],
      probability: 0.7,
      description: 'Inflammation of the stomach and intestines, often due to infection.',
      selfCare: ['Stay hydrated', 'BRAT diet', 'Rest'],
      seekCare: 'If severe dehydration or blood in stool'
    },
    'Tension Headache': {
      symptoms: ['headache', 'fatigue', 'muscle tension'],
      probability: 0.75,
      description: 'The most common type of headache, often caused by stress or tension.',
      selfCare: ['Rest', 'Stress management', 'Over-the-counter pain relievers'],
      seekCare: 'If severe or accompanied by other neurological symptoms'
    }
  };
  
  // Match conditions based on symptoms
  Object.entries(conditionDatabase).forEach(([conditionName, conditionData]) => {
    const matchScore = calculateSymptomMatch(analysis.primarySymptoms, conditionData.symptoms);
    
    if (matchScore > 0.3) {
      conditions.push({
        name: conditionName,
        probability: Math.round(matchScore * conditionData.probability * 100),
        description: conditionData.description,
        commonSymptoms: conditionData.symptoms,
        whenToSeekCare: conditionData.seekCare,
        selfCareOptions: conditionData.selfCare
      });
    }
  });
  
  // Sort by probability
  return conditions.sort((a, b) => b.probability - a.probability);
};

const calculateSymptomMatch = (userSymptoms: string[], conditionSymptoms: string[]): number => {
  const matches = userSymptoms.filter(userSymptom =>
    conditionSymptoms.some(condSymptom =>
      userSymptom.toLowerCase().includes(condSymptom.toLowerCase())
    )
  ).length;
  
  return matches / conditionSymptoms.length;
};

const assessUrgency = (symptoms: string[], patientData: any): {
  urgencyLevel: 'low' | 'medium' | 'high' | 'emergency';
  redFlags: string[];
} => {
  const redFlags: string[] = [];
  let urgencyLevel: 'low' | 'medium' | 'high' | 'emergency' = 'low';
  
  // Emergency red flags
  const emergencySymptoms = [
    'severe chest pain',
    'difficulty breathing',
    'loss of consciousness',
    'severe bleeding',
    'signs of stroke'
  ];
  
  const highUrgencySymptoms = [
    'high fever',
    'severe pain',
    'persistent vomiting',
    'severe headache'
  ];
  
  symptoms.forEach(symptom => {
    const lowerSymptom = symptom.toLowerCase();
    
    if (emergencySymptoms.some(emergency => lowerSymptom.includes(emergency))) {
      redFlags.push(`Emergency: ${symptom}`);
      urgencyLevel = 'emergency';
    } else if (highUrgencySymptoms.some(high => lowerSymptom.includes(high))) {
      redFlags.push(`High urgency: ${symptom}`);
      if (urgencyLevel !== 'emergency') urgencyLevel = 'high';
    }
  });
  
  // Age-based adjustments
  if (patientData.age && (patientData.age < 2 || patientData.age > 65)) {
    if (urgencyLevel === 'low') urgencyLevel = 'medium';
  }
  
  // Severity-based adjustments
  if (patientData.severity && patientData.severity >= 8) {
    if (urgencyLevel === 'low') urgencyLevel = 'medium';
  }
  
  return { urgencyLevel, redFlags };
};

interface SymptomAnalysis {
  primarySymptoms: string[];
  associatedSymptoms: string[];
  systemsInvolved: string[];
  severity: number;
  duration: string;
}
```

### Day 20-21: Medical Disclaimers and Accuracy Display

#### Step 12: Disclaimer and Safety Components
```typescript
// components/medical/DisclaimerCard.tsx
import React, { useState } from 'react';
import { View, Text, Pressable, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export const DisclaimerCard: React.FC = () => {
  const [showFullDisclaimer, setShowFullDisclaimer] = useState(false);
  
  return (
    <>
      <View className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 m-4">
        <View className="flex-row items-start">
          <Ionicons name="warning" size={24} color="#F59E0B" className="mr-3 mt-1" />
          <View className="flex-1">
            <Text className="font-semibold text-yellow-800 mb-2">
              Important Medical Disclaimer
            </Text>
            <Text className="text-yellow-700 text-sm mb-3">
              This AI provides preliminary guidance only and is not a substitute for professional medical advice, diagnosis, or treatment.
            </Text>
            <Pressable
              onPress={() => setShowFullDisclaimer(true)}
              className="flex-row items-center"
            >
              <Text className="text-yellow-600 font-medium text-sm">
                Read full disclaimer
              </Text>
              <Ionicons name="chevron-forward" size={16} color="#D97706" className="ml-1" />
            </Pressable>
          </View>
        </View>
      </View>
      
      <Modal
        visible={showFullDisclaimer}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <FullDisclaimerModal onClose={() => setShowFullDisclaimer(false)} />
      </Modal>
    </>
  );
};

const FullDisclaimerModal: React.FC<{ onClose: () => void }> = ({ onClose }) => (
  <SafeAreaView className="flex-1 bg-white">
    <View className="flex-row items-center justify-between p-4 border-b border-gray-200">
      <Text className="text-xl font-bold">Medical Disclaimer</Text>
      <Pressable onPress={onClose}>
        <Ionicons name="close" size={24} color="#6B7280" />
      </Pressable>
    </View>
    
    <ScrollView className="flex-1 p-4">
      <Text className="text-base text-gray-800 mb-4">
        <Text className="font-semibold">Important Notice:</Text> The information provided by this AI-powered medical assistant is for educational and informational purposes only and is not intended as a substitute for professional medical advice, diagnosis, or treatment.
      </Text>
      
      <Text className="font-semibold text-lg mb-2">Key Points:</Text>
      
      <View className="mb-4">
        <Text className="font-medium mb-1">• Not a Medical Professional</Text>
        <Text className="text-gray-700 mb-3">
          This AI is not a licensed healthcare provider and cannot provide medical diagnoses or treatment recommendations.
        </Text>
        
        <Text className="font-medium mb-1">• Seek Professional Care</Text>
        <Text className="text-gray-700 mb-3">
          Always consult with qualified healthcare professionals for medical concerns, especially for urgent or emergency situations.
        </Text>
        
        <Text className="font-medium mb-1">• Emergency Situations</Text>
        <Text className="text-gray-700 mb-3">
          In case of medical emergencies, call emergency services (911) immediately. Do not rely on this app for emergency medical care.
        </Text>
        
        <Text className="font-medium mb-1">• Accuracy Limitations</Text>
        <Text className="text-gray-700 mb-3">
          While we strive for accuracy, medical AI systems have limitations and may not account for all individual circumstances.
        </Text>
        
        <Text className="font-medium mb-1">• Privacy and Security</Text>
        <Text className="text-gray-700 mb-3">
          Your health information is protected according to HIPAA guidelines, but avoid sharing sensitive personal details unnecessarily.
        </Text>
      </View>
      
      <View className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
        <Text className="font-semibold text-red-800 mb-2">When to Seek Emergency Care:</Text>
        <Text className="text-red-700">
          • Chest pain or difficulty breathing{'\n'}
          • Severe allergic reactions{'\n'}
          • Loss of consciousness{'\n'}
          • Severe bleeding{'\n'}
          • Signs of stroke or heart attack{'\n'}
          • Any life-threatening situation
        </Text>
      </View>
    </ScrollView>
  </SafeAreaView>
);

// Accuracy Display Component
export const AccuracyDisplay: React.FC<{
  confidence: number;
  factors: {
    symptomClarity: number;
    medicalHistory: number;
    responseRelevance: number;
  };
}> = ({ confidence, factors }) => {
  const getConfidenceColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };
  
  const getConfidenceBackground = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };
  
  return (
    <View className="bg-gray-50 rounded-lg p-4 m-4">
      <Text className="font-semibold text-gray-800 mb-3">Analysis Confidence</Text>
      
      <View className={`rounded-lg p-3 mb-3 ${getConfidenceBackground(confidence)}`}>
        <View className="flex-row items-center justify-between">
          <Text className="font-medium">Overall Confidence</Text>
          <Text className={`font-bold text-lg ${getConfidenceColor(confidence)}`}>
            {confidence}%
          </Text>
        </View>
      </View>
      
      <Text className="font-medium text-gray-700 mb-2">Contributing Factors:</Text>
      
      {Object.entries(factors).map(([factor, score]) => (
        <View key={factor} className="flex-row items-center justify-between mb-2">
          <Text className="text-gray-600 capitalize flex-1">
            {factor.replace(/([A-Z])/g, ' $1')}
          </Text>
          <View className="flex-row items-center">
            <View className="w-20 h-2 bg-gray-200 rounded-full mr-2">
              <View 
                className={`h-full rounded-full ${
                  score >= 80 ? 'bg-green-500' :
                  score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                }`}
                style={{ width: `${score}%` }}
              />
            </View>
            <Text className={`text-sm font-medium ${getConfidenceColor(score)}`}>
              {score}%
            </Text>
          </View>
        </View>
      ))}
      
      <Text className="text-xs text-gray-500 mt-3">
        Higher confidence indicates more reliable preliminary analysis. Always consult healthcare professionals for medical decisions.
      </Text>
    </View>
  );
};
```

---

## 🗂️ File Structure for Phase 2

```
src/
├── app/
│   └── (tabs)/
│       └── chat/
│           ├── index.tsx                 # Main chat screen
│           └── diagnosis/
│               └── [id].tsx              # Diagnosis details
├── components/
│   ├── chat/
│   │   ├── MessageBubble.tsx            # Message display
│   │   ├── ChatInput.tsx                # Input with image upload
│   │   ├── TypingIndicator.tsx          # AI typing animation
│   │   └── FollowUpQuestions.tsx        # Dynamic questions
│   └── medical/
│       ├── DisclaimerCard.tsx           # Legal disclaimers
│       ├── AccuracyDisplay.tsx          # Confidence metrics
│       └── SymptomInput.tsx             # Symptom selection
├── services/
│   ├── aiService.ts                     # OpenAI integration
│   ├── confidenceService.ts             # Accuracy tracking
│   ├── diagnosisService.ts              # Medical logic
│   ├── medicalPrompts.ts                # Specialized prompts
│   └── questionService.ts               # Follow-up questions
├── store/
│   └── chatStore.ts                     # State management
├── types/
│   ├── chat.ts                          # Message interfaces
│   ├── medical.ts                       # Medical types
│   └── supabase.ts                      # Database types
└── lib/
    └── supabase.ts                      # Database client
```

---

## 🧪 Testing Checklist for Phase 2

### Functionality Tests
- [ ] Chat interface loads correctly
- [ ] Messages send and display properly
- [ ] Image upload and display works
- [ ] Real-time messaging functions
- [ ] AI responses generate correctly
- [ ] Follow-up questions appear dynamically
- [ ] Confidence scoring calculates accurately
- [ ] Disclaimers display appropriately

### AI Integration Tests
- [ ] OpenAI API calls succeed
- [ ] Image analysis processes correctly
- [ ] Medical prompts generate relevant responses
- [ ] Error handling works for API failures
- [ ] Response formatting is consistent

### User Experience Tests
- [ ] Chat flows naturally
- [ ] Loading states are clear
- [ ] Error messages are helpful
- [ ] Interface is intuitive
- [ ] Performance is acceptable (<3s responses)

---

## 🚀 Phase 2 Deliverables

By the end of Week 5, you should have:

1. **Functional Chat Interface**
   - Real-time messaging
   - Image upload capability
   - Professional medical UI

2. **AI Diagnosis System**
   - OpenAI GPT-4 integration
   - Image analysis with Vision API
   - Medical prompt templates

3. **Medical Logic**
   - Dynamic follow-up questions
   - Preliminary diagnosis generation
   - Confidence scoring system

4. **Safety Features**
   - Medical disclaimers
   - Accuracy displays
   - Emergency detection

5. **Database Integration**
   - Message persistence
   - Consultation tracking
   - Real-time updates

This comprehensive implementation of Phase 2 creates the core medical AI functionality that users will interact with daily. The system is designed to be safe, accurate, and user-friendly while maintaining appropriate medical disclaimers and professional standards.