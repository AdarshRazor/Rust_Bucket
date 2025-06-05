# AI-Diagnosis Telemedicine App - Overview, Guidelines & Blueprint

## 🎯 Project Overview

### **Vision Statement**
Create a cutting-edge, HIPAA-compliant mobile telemedicine application that leverages AI for preliminary medical diagnosis and seamlessly connects patients with healthcare specialists through integrated video calling and appointment scheduling.

### **Core Value Proposition**
- **AI-Powered Diagnosis**: Instant preliminary medical assessment using GPT-4 Vision
- **Specialist Matching**: Location-based specialist recommendations
- **Seamless Booking**: Integrated video calling and calendar management
- **HIPAA Compliance**: Enterprise-grade security and privacy
- **Cross-Platform**: Native iOS and Android experience with shared codebase

---

## 🏗️ System Architecture

### **High-Level Architecture Diagram**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │   Backend APIs  │    │  External APIs  │
│   (Expo/RN)     │◄──►│   (Supabase)    │◄──►│  (OpenAI, etc.) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Authentication │    │    Database     │    │   Video Calling │
│     (Clerk)     │    │  (PostgreSQL)   │    │    (Agora.io)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Technology Stack Rationale**

#### **Why Expo + React Native?**
<mcreference link="https://galaxies.dev/article/react-native-tech-stack-2025" index="3">3</mcreference>
- **2025 Recommendation**: Expo is now the official recommended framework for React Native
- **Cross-Platform**: Single codebase for iOS, Android, and Web
- **Developer Experience**: Hot reloading, over-the-air updates, simplified deployment
- **Ecosystem**: Rich library ecosystem with native module support

#### **Why Supabase + Clerk?**
<mcreference link="https://supabase.com/blog/react-native-authentication" index="1">1</mcreference> <mcreference link="https://clerk.com/docs/integrations/databases/supabase" index="2">2</mcreference>
- **HIPAA Compliance**: Both offer Business Associate Agreements (BAA)
- **Integration**: Native integration between Clerk and Supabase
- **Real-time**: Built-in real-time subscriptions for chat functionality
- **Scalability**: Auto-scaling PostgreSQL with global edge functions

#### **Why OpenAI GPT-4.1?**
<mcreference link="https://openai.com/index/gpt-4-1/" index="1">1</mcreference>
- **Latest Model**: GPT-4.1 offers improved instruction following and coding
- **Vision Capabilities**: Native image analysis for medical imaging
- **Context Window**: 1 million tokens for comprehensive medical context
- **Reliability**: Better instruction following for consistent medical responses

#### **Why Agora.io for Video?**
<mcreference link="https://www.agora.io/en/blog/how-to-build-a-react-native-video-calling-app-using-agora/" index="2">2</mcreference>
- **React Native Support**: Native SDK with excellent documentation
- **Scalability**: Handles millions of concurrent users
- **Quality**: Adaptive bitrate and network optimization
- **Features**: Screen sharing, recording, real-time messaging

---

## 📱 User Experience Flow

### **Patient Journey**
```
1. App Launch → Authentication (Biometric/PIN)
2. Symptom Input → AI Chat Interface
3. Image Upload → AI Analysis
4. Preliminary Diagnosis → Confidence Score
5. Specialist Recommendations → Location-based
6. Appointment Booking → Calendar Integration
7. Video Consultation → Agora.io
8. Follow-up → Prescription/Referral
```

### **Specialist Journey**
```
1. Dashboard Login → Patient Queue
2. Review AI Analysis → Medical History
3. Video Consultation → Patient Interaction
4. Diagnosis Confirmation → Treatment Plan
5. Prescription → Digital Signature
6. Follow-up Scheduling → Calendar Sync
```

---

## 🔧 Development Guidelines

### **Code Structure**
```
src/
├── app/                    # Expo Router pages
│   ├── (auth)/            # Authentication screens
│   ├── (tabs)/            # Main app tabs
│   └── _layout.tsx        # Root layout
├── components/            # Reusable UI components
│   ├── ui/               # Base UI components
│   ├── forms/            # Form components
│   └── chat/             # Chat-specific components
├── lib/                  # Utilities and configurations
│   ├── supabase.ts       # Supabase client
│   ├── clerk.ts          # Clerk configuration
│   ├── openai.ts         # OpenAI client
│   └── agora.ts          # Agora configuration
├── hooks/                # Custom React hooks
├── stores/               # Zustand stores
├── types/                # TypeScript type definitions
└── constants/            # App constants
```

### **Naming Conventions**
- **Files**: kebab-case (`user-profile.tsx`)
- **Components**: PascalCase (`UserProfile`)
- **Functions**: camelCase (`getUserProfile`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`)
- **Types**: PascalCase with suffix (`UserProfileType`)

### **State Management Pattern**
```typescript
// stores/auth-store.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  user: User | null
  isLoading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => void
}

export const useAuthStore = create<AuthState>()()
  persist(
    (set, get) => ({
      user: null,
      isLoading: false,
      signIn: async (email, password) => {
        set({ isLoading: true })
        // Implementation
      },
      signOut: () => set({ user: null })
    }),
    { name: 'auth-storage' }
  )
)
```

---

## 🔐 Security & Compliance Guidelines

### **HIPAA Compliance Checklist**
<mcreference link="https://www.pragmaticcoders.com/blog/essential-guide-to-2023s-hipaa-compliant-software-development" index="5">5</mcreference>

#### **Administrative Safeguards**
- [ ] Assign HIPAA security officer
- [ ] Conduct regular risk assessments
- [ ] Implement workforce training
- [ ] Create incident response procedures
- [ ] Establish audit controls

#### **Physical Safeguards**
- [ ] Secure data centers (Supabase/Clerk responsibility)
- [ ] Device access controls
- [ ] Workstation security
- [ ] Media disposal procedures

#### **Technical Safeguards**
- [ ] Access controls and user authentication
- [ ] Audit logs and monitoring
- [ ] Data integrity controls
- [ ] Transmission security (TLS 1.3)
- [ ] Encryption at rest and in transit

### **Data Encryption Implementation**
```typescript
// lib/encryption.ts
import * as SecureStore from 'expo-secure-store'
import * as aesjs from 'aes-js'
import 'react-native-get-random-values'

class SecureStorage {
  private async encrypt(key: string, value: string): Promise<string> {
    const encryptionKey = crypto.getRandomValues(new Uint8Array(256 / 8))
    const cipher = new aesjs.ModeOfOperation.ctr(encryptionKey, new aesjs.Counter(1))
    const encryptedBytes = cipher.encrypt(aesjs.utils.utf8.toBytes(value))
    
    await SecureStore.setItemAsync(key, aesjs.utils.hex.fromBytes(encryptionKey))
    return aesjs.utils.hex.fromBytes(encryptedBytes)
  }

  private async decrypt(key: string, encryptedValue: string): Promise<string | null> {
    const encryptionKeyHex = await SecureStore.getItemAsync(key)
    if (!encryptionKeyHex) return null

    const cipher = new aesjs.ModeOfOperation.ctr(
      aesjs.utils.hex.toBytes(encryptionKeyHex),
      new aesjs.Counter(1)
    )
    const decryptedBytes = cipher.decrypt(aesjs.utils.hex.toBytes(encryptedValue))
    return aesjs.utils.utf8.fromBytes(decryptedBytes)
  }
}
```

---

## 🤖 AI Integration Best Practices

### **Medical Prompt Engineering**
```typescript
// lib/medical-prompts.ts
export const MEDICAL_DIAGNOSIS_PROMPT = `
You are a medical AI assistant helping with preliminary diagnosis. 

IMPORTANT DISCLAIMERS:
- You are NOT a replacement for professional medical advice
- Always recommend consulting with a healthcare provider
- Provide confidence scores (0-100%) for your assessments
- Ask follow-up questions to gather more information

Patient Information:
- Age: {age}
- Gender: {gender}
- Symptoms: {symptoms}
- Duration: {duration}
- Medical History: {medicalHistory}

Analyze the symptoms and provide:
1. Possible conditions (with confidence scores)
2. Recommended specialist type
3. Urgency level (Low/Medium/High/Emergency)
4. Follow-up questions to ask
5. General care recommendations

Format your response as JSON:
{
  "possibleConditions": [
    {"condition": "string", "confidence": number, "reasoning": "string"}
  ],
  "recommendedSpecialist": "string",
  "urgencyLevel": "Low|Medium|High|Emergency",
  "followUpQuestions": ["string"],
  "generalRecommendations": ["string"],
  "disclaimer": "This is a preliminary assessment. Please consult with a healthcare provider for proper diagnosis and treatment."
}
`

export const IMAGE_ANALYSIS_PROMPT = `
Analyze this medical image and provide observations.

IMPORTANT:
- Only describe what you observe
- Do not provide definitive diagnoses
- Recommend professional evaluation
- Include confidence in observations

Provide analysis in JSON format:
{
  "observations": ["string"],
  "concerningFeatures": ["string"],
  "recommendedAction": "string",
  "confidence": number,
  "disclaimer": "Image analysis requires professional medical interpretation."
}
`
```

### **AI Safety Implementation**
```typescript
// lib/ai-safety.ts
interface SafetyCheck {
  isEmergency: boolean
  requiresImmediateAttention: boolean
  confidenceThreshold: number
}

export function performSafetyCheck(aiResponse: any): SafetyCheck {
  const emergencyKeywords = [
    'chest pain', 'difficulty breathing', 'severe bleeding',
    'loss of consciousness', 'stroke symptoms'
  ]
  
  const isEmergency = emergencyKeywords.some(keyword => 
    aiResponse.symptoms?.toLowerCase().includes(keyword)
  )
  
  return {
    isEmergency,
    requiresImmediateAttention: aiResponse.urgencyLevel === 'Emergency',
    confidenceThreshold: aiResponse.confidence || 0
  }
}
```

---

## 📞 Video Calling Implementation

### **Agora Integration Setup**
```typescript
// lib/agora-client.ts
import {
  createAgoraRtcEngine,
  IRtcEngine,
  ChannelProfileType,
  ClientRoleType
} from 'react-native-agora'

class AgoraService {
  private engine: IRtcEngine
  
  constructor() {
    this.engine = createAgoraRtcEngine()
  }
  
  async initialize(appId: string) {
    await this.engine.initialize({
      appId,
      channelProfile: ChannelProfileType.ChannelProfileCommunication
    })
    
    await this.engine.enableVideo()
    await this.engine.enableAudio()
  }
  
  async joinChannel(token: string, channelName: string, uid: number) {
    await this.engine.joinChannel(token, channelName, uid, {
      clientRoleType: ClientRoleType.ClientRoleBroadcaster
    })
  }
  
  async leaveChannel() {
    await this.engine.leaveChannel()
  }
  
  async destroy() {
    await this.engine.release()
  }
}

export const agoraService = new AgoraService()
```

### **Video Call Component**
```typescript
// components/video-call.tsx
import React, { useEffect, useState } from 'react'
import { View, StyleSheet } from 'react-native'
import { RtcSurfaceView, VideoViewSetupMode } from 'react-native-agora'
import { agoraService } from '../lib/agora-client'

interface VideoCallProps {
  channelName: string
  token: string
  uid: number
}

export function VideoCall({ channelName, token, uid }: VideoCallProps) {
  const [isJoined, setIsJoined] = useState(false)
  const [remoteUid, setRemoteUid] = useState<number | null>(null)
  
  useEffect(() => {
    const setupVideoCall = async () => {
      await agoraService.initialize(process.env.EXPO_PUBLIC_AGORA_APP_ID!)
      
      // Event listeners
      agoraService.engine.addListener('onJoinChannelSuccess', () => {
        setIsJoined(true)
      })
      
      agoraService.engine.addListener('onUserJoined', (connection, uid) => {
        setRemoteUid(uid)
      })
      
      await agoraService.joinChannel(token, channelName, uid)
    }
    
    setupVideoCall()
    
    return () => {
      agoraService.leaveChannel()
    }
  }, [])
  
  return (
    <View style={styles.container}>
      {/* Local Video */}
      <RtcSurfaceView
        style={styles.localVideo}
        canvas={{ uid: 0, setupMode: VideoViewSetupMode.VideoViewSetupReplace }}
      />
      
      {/* Remote Video */}
      {remoteUid && (
        <RtcSurfaceView
          style={styles.remoteVideo}
          canvas={{ uid: remoteUid, setupMode: VideoViewSetupMode.VideoViewSetupReplace }}
        />
      )}
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000'
  },
  localVideo: {
    position: 'absolute',
    top: 50,
    right: 20,
    width: 120,
    height: 160,
    zIndex: 1
  },
  remoteVideo: {
    flex: 1
  }
})
```

---

## 📅 Calendar Integration

### **Google Calendar Setup**
```typescript
// lib/calendar-service.ts
import { GoogleSignin } from '@react-native-google-signin/google-signin'

class CalendarService {
  async initialize() {
    GoogleSignin.configure({
      webClientId: process.env.GOOGLE_CALENDAR_CLIENT_ID,
      scopes: ['https://www.googleapis.com/auth/calendar']
    })
  }
  
  async createAppointment(appointment: {
    title: string
    startTime: Date
    endTime: Date
    attendees: string[]
    description?: string
  }) {
    const tokens = await GoogleSignin.getTokens()
    
    const event = {
      summary: appointment.title,
      start: {
        dateTime: appointment.startTime.toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      },
      end: {
        dateTime: appointment.endTime.toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      },
      attendees: appointment.attendees.map(email => ({ email })),
      description: appointment.description
    }
    
    const response = await fetch(
      'https://www.googleapis.com/calendar/v3/calendars/primary/events',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${tokens.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(event)
      }
    )
    
    return response.json()
  }
}

export const calendarService = new CalendarService()
```

---

## 🧪 Testing Strategy

### **Testing Pyramid**
```
        E2E Tests (10%)
       ┌─────────────────┐
      │   Detox Tests   │
     └─────────────────┘
    Integration Tests (20%)
   ┌─────────────────────┐
  │  Component Tests    │
 └─────────────────────┘
      Unit Tests (70%)
 ┌─────────────────────────┐
│  Jest + Testing Library │
└─────────────────────────┘
```

### **Test Examples**
```typescript
// __tests__/components/chat-message.test.tsx
import React from 'react'
import { render, screen } from '@testing-library/react-native'
import { ChatMessage } from '../src/components/chat/chat-message'

describe('ChatMessage', () => {
  it('renders user message correctly', () => {
    render(
      <ChatMessage
        message={{
          id: '1',
          text: 'Hello doctor',
          sender: 'user',
          timestamp: new Date()
        }}
      />
    )
    
    expect(screen.getByText('Hello doctor')).toBeTruthy()
  })
  
  it('renders AI message with confidence score', () => {
    render(
      <ChatMessage
        message={{
          id: '2',
          text: 'Based on your symptoms...',
          sender: 'ai',
          confidence: 85,
          timestamp: new Date()
        }}
      />
    )
    
    expect(screen.getByText('85% confidence')).toBeTruthy()
  })
})
```

---

## 🚀 Performance Optimization

### **Bundle Size Optimization**
```javascript
// metro.config.js
const { getDefaultConfig } = require('expo/metro-config')

const config = getDefaultConfig(__dirname)

// Enable tree shaking
config.resolver.platforms = ['ios', 'android', 'web']
config.transformer.minifierConfig = {
  keep_fnames: true,
  mangle: {
    keep_fnames: true
  }
}

module.exports = config
```

### **Image Optimization**
```typescript
// components/optimized-image.tsx
import { Image } from 'expo-image'

export function OptimizedImage({ source, ...props }) {
  return (
    <Image
      source={source}
      placeholder={{ blurhash: 'L6PZfSi_.AyE_3t7t7R**0o#DgR4' }}
      contentFit="cover"
      transition={200}
      {...props}
    />
  )
}
```

### **API Caching Strategy**
```typescript
// lib/api-cache.ts
import AsyncStorage from '@react-native-async-storage/async-storage'

class APICache {
  private cache = new Map()
  private readonly TTL = 5 * 60 * 1000 // 5 minutes
  
  async get(key: string) {
    const cached = this.cache.get(key)
    if (cached && Date.now() - cached.timestamp < this.TTL) {
      return cached.data
    }
    
    // Try persistent storage
    const stored = await AsyncStorage.getItem(`cache_${key}`)
    if (stored) {
      const parsed = JSON.parse(stored)
      if (Date.now() - parsed.timestamp < this.TTL) {
        this.cache.set(key, parsed)
        return parsed.data
      }
    }
    
    return null
  }
  
  async set(key: string, data: any) {
    const cacheItem = { data, timestamp: Date.now() }
    this.cache.set(key, cacheItem)
    await AsyncStorage.setItem(`cache_${key}`, JSON.stringify(cacheItem))
  }
}

export const apiCache = new APICache()
```

---

## 📊 Analytics & Monitoring

### **Key Metrics to Track**
- **User Engagement**: Session duration, feature usage
- **AI Performance**: Diagnosis accuracy, user satisfaction
- **Technical Metrics**: App crashes, API response times
- **Business Metrics**: Appointment conversion, specialist ratings

### **Implementation**
```typescript
// lib/analytics.ts
import * as Analytics from 'expo-analytics'

class AnalyticsService {
  async trackEvent(event: string, properties?: Record<string, any>) {
    await Analytics.track(event, {
      ...properties,
      timestamp: new Date().toISOString(),
      platform: Platform.OS
    })
  }
  
  async trackDiagnosis(diagnosis: {
    confidence: number
    specialty: string
    duration: number
  }) {
    await this.trackEvent('ai_diagnosis_completed', {
      confidence_score: diagnosis.confidence,
      recommended_specialty: diagnosis.specialty,
      diagnosis_duration_seconds: diagnosis.duration
    })
  }
  
  async trackAppointmentBooked(appointment: {
    specialty: string
    type: 'video' | 'voice' | 'in-person'
  }) {
    await this.trackEvent('appointment_booked', {
      specialist_type: appointment.specialty,
      appointment_type: appointment.type
    })
  }
}

export const analytics = new AnalyticsService()
```

---

## 🔄 Deployment & CI/CD

### **EAS Build Configuration**
```json
// eas.json
{
  "cli": {
    "version": ">= 12.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "env": {
        "ENVIRONMENT": "preview"
      }
    },
    "production": {
      "env": {
        "ENVIRONMENT": "production"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-apple-id@example.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABCDEFGHIJ"
      },
      "android": {
        "serviceAccountKeyPath": "../path/to/api-key.json",
        "track": "production"
      }
    }
  }
}
```

### **GitHub Actions Workflow**
```yaml
# .github/workflows/build-and-deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run test
      - run: npm run lint
      - run: npm run type-check

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          expo-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --platform all --non-interactive
```

---

## 📋 Launch Checklist

### **Pre-Launch**
- [ ] HIPAA compliance audit completed
- [ ] Security penetration testing passed
- [ ] Performance benchmarks met
- [ ] App store guidelines compliance
- [ ] Legal review completed
- [ ] Privacy policy and terms of service finalized
- [ ] Beta testing with healthcare professionals
- [ ] Accessibility testing (WCAG 2.1 AA)

### **Launch Day**
- [ ] Production deployment verified
- [ ] Monitoring and alerting active
- [ ] Customer support team trained
- [ ] Marketing materials ready
- [ ] Press release prepared
- [ ] Social media campaigns scheduled

### **Post-Launch**
- [ ] User feedback collection system active
- [ ] Analytics dashboard monitoring
- [ ] Regular security audits scheduled
- [ ] Feature roadmap communicated
- [ ] Continuous integration pipeline optimized

---

*This blueprint provides a comprehensive foundation for building a modern, scalable, and compliant telemedicine application using cutting-edge 2025 technologies.*