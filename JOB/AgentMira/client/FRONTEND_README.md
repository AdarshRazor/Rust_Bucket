# 🎨 Agent Mira Frontend Documentation

## 📁 Project Structure

```
client/
├── src/
│   ├── app/                          # Next.js App Router
│   │   ├── globals.css              # Global styles and Tailwind CSS
│   │   ├── layout.tsx               # Root layout component
│   │   └── page.tsx                 # Home page component
│   ├── components/                   # React components
│   │   ├── forms/                   # Form components
│   │   │   └── PreferenceForm.tsx   # User preference input form
│   │   ├── recommendations/         # Recommendation display components
│   │   │   ├── RecommendationList.tsx    # List of recommendations
│   │   │   ├── RecommendationCard.tsx    # Individual recommendation card
│   │   │   └── ScoreBreakdown.tsx        # Detailed scoring breakdown
│   │   └── ui/                      # Reusable UI components
│   │       ├── LoadingSpinner.tsx   # Loading indicator
│   │       └── ErrorMessage.tsx     # Error display component
│   └── lib/                         # Utility functions and types
│       ├── api.ts                   # API client and integration
│       ├── types.ts                 # TypeScript type definitions
│       └── utils.ts                 # Helper functions and utilities
├── public/                          # Static assets
├── package.json                     # Dependencies and scripts
├── tailwind.config.js              # Tailwind CSS configuration
├── tsconfig.json                   # TypeScript configuration
└── next.config.ts                  # Next.js configuration
```

## 🚀 Key Features Implemented

### 1. **User Preference Form** (`PreferenceForm.tsx`)
- **Budget Input**: Currency-formatted budget selection
- **Location Input**: Free-text location preference
- **Bedroom Requirements**: Dropdown selection (1-6 bedrooms)
- **Commute Time**: Range selection (15-90+ minutes)
- **School Rating**: Slider input (0-10 scale)
- **Amenities Selection**: Multi-select checkbox grid
- **Form Validation**: Real-time validation with error messages
- **Responsive Design**: Mobile-first responsive layout

### 2. **Recommendation Display** (`RecommendationList.tsx` & `RecommendationCard.tsx`)
- **Top 3 Recommendations**: Ranked by compatibility score
- **Property Cards**: Rich property information display
- **Score Visualization**: Color-coded scoring system
- **Detailed Breakdown**: Component-wise scoring analysis
- **Reasoning Display**: Human-readable recommendation explanations
- **Interactive Actions**: View details, save, share functionality

### 3. **API Integration** (`api.ts`)
- **Type-Safe API Client**: Full TypeScript integration
- **Error Handling**: Comprehensive error management
- **Session Management**: Automatic session ID generation
- **Request/Response Types**: Strongly typed API calls
- **Utility Functions**: Currency formatting, number formatting

### 4. **UI Components** (`ui/`)
- **Loading States**: Spinner with customizable sizes
- **Error Messages**: User-friendly error display with retry options
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support

## 🎨 Design System

### Color Palette
- **Primary**: Indigo (600/700) - Main brand color
- **Secondary**: Gray (100-900) - Neutral colors
- **Success**: Green (500/600) - Positive states
- **Warning**: Yellow (500) - Caution states
- **Error**: Red (500/600) - Error states

### Typography
- **Font Family**: Inter (Google Fonts)
- **Headings**: Bold, various sizes (text-2xl to text-6xl)
- **Body Text**: Regular weight, readable sizes
- **Labels**: Medium weight, smaller sizes

### Components
- **Cards**: White background, subtle shadows, rounded corners
- **Buttons**: Primary (indigo) and secondary (gray) variants
- **Forms**: Clean inputs with focus states and validation
- **Loading**: Smooth animations and transitions

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px (sm)
- **Tablet**: 768px - 1024px (md)
- **Desktop**: > 1024px (lg)

### Mobile Features
- **Touch-Friendly**: Large tap targets (44px minimum)
- **Swipe Gestures**: Smooth scrolling and interactions
- **Optimized Layout**: Stacked layout on mobile
- **Readable Text**: Appropriate font sizes for mobile

## 🔧 Technical Implementation

### State Management
- **React Hooks**: useState, useEffect for local state
- **Form State**: Controlled components with validation
- **API State**: Loading, error, and success states
- **Session State**: Persistent session management

### Performance Optimizations
- **Code Splitting**: Next.js automatic code splitting
- **Image Optimization**: Next.js Image component
- **Lazy Loading**: Components loaded on demand
- **Memoization**: React.memo for expensive components

### Accessibility Features
- **ARIA Labels**: Screen reader support
- **Keyboard Navigation**: Full keyboard accessibility
- **Focus Management**: Visible focus indicators
- **Color Contrast**: WCAG compliant color ratios
- **Semantic HTML**: Proper heading hierarchy

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn package manager

### Installation
```bash
cd client
npm install
```

### Development
```bash
npm run dev
```

### Build
```bash
npm run build
npm start
```

## 📋 Component Usage

### PreferenceForm
```tsx
<PreferenceForm
  onSubmit={(preferences) => handleSubmit(preferences)}
  loading={isLoading}
  initialValues={savedPreferences}
/>
```

### RecommendationList
```tsx
<RecommendationList
  recommendations={recommendations}
  onNewSearch={() => handleNewSearch()}
/>
```

### RecommendationCard
```tsx
<RecommendationCard
  recommendation={recommendation}
  rank={1}
  onViewDetails={(property) => handleViewDetails(property)}
  onAddToFavorites={(property) => handleAddToFavorites(property)}
/>
```

## 🎯 Key Features

### 1. **Smart Form Validation**
- Real-time validation with immediate feedback
- Custom validation rules for each field
- Error messages with helpful suggestions
- Form state persistence across sessions

### 2. **Rich Recommendation Display**
- Visual score indicators with color coding
- Detailed property information with images
- Component-wise scoring breakdown
- Human-readable reasoning explanations

### 3. **Responsive User Experience**
- Mobile-first design approach
- Touch-friendly interactions
- Optimized for all screen sizes
- Fast loading and smooth animations

### 4. **Accessibility First**
- WCAG 2.1 AA compliance
- Screen reader support
- Keyboard navigation
- High contrast support

## 🔮 Future Enhancements

### Phase 2 Features (Planned)
- **Property Comparison**: Side-by-side property comparison
- **Favorites System**: Save and manage favorite properties
- **Advanced Filtering**: More sophisticated search options
- **Property Details Modal**: Detailed property information
- **Search History**: Track and revisit previous searches

### Phase 3 Features (Planned)
- **User Authentication**: User accounts and profiles
- **Personalized Dashboard**: Custom user experience
- **Real-time Notifications**: Property updates and alerts
- **Social Features**: Share and recommend properties
- **Analytics Dashboard**: Usage insights and metrics

## 🐛 Troubleshooting

### Common Issues
1. **API Connection**: Ensure backend is running on port 8000
2. **CORS Errors**: Check CORS configuration in backend
3. **Type Errors**: Run `npm run build` to check TypeScript errors
4. **Styling Issues**: Verify Tailwind CSS is properly configured

### Development Tips
- Use React DevTools for component debugging
- Check browser console for API errors
- Use Next.js built-in error overlay for development
- Test on multiple devices for responsive design

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
