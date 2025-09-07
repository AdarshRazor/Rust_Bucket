# Agent Mira - Frontend Configuration

## Frontend package.json
```json
{
  "name": "agent-mira-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "dependencies": {
    "next": "14.0.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.2",
    "@types/node": "^20.10.0",
    "@types/react": "^18.2.39",
    "@types/react-dom": "^18.2.17",
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "axios": "^1.6.2",
    "react-hook-form": "^7.48.2",
    "@hookform/resolvers": "^3.3.2",
    "zod": "^3.22.4",
    "lucide-react": "^0.294.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "react-hot-toast": "^2.4.1",
    "framer-motion": "^10.16.5"
  },
  "devDependencies": {
    "eslint": "^8.55.0",
    "eslint-config-next": "14.0.3",
    "@types/jest": "^29.5.8",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/user-event": "^14.5.1"
  }
}
```

## Frontend Dockerfile
```dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["npm", "start"]
```

## next.config.js
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost', 'example.com'],
    formats: ['image/webp', 'image/avif'],
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
    ]
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig
```

## tailwind.config.js
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
        },
        success: {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',
          600: '#d97706',
        },
        error: {
          50: '#fef2f2',
          500: '#ef4444',
          600: '#dc2626',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

## tsconfig.json
```json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/types/*": ["./src/types/*"],
      "@/services/*": ["./src/services/*"],
      "@/hooks/*": ["./src/hooks/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## .env.local.example
```
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Agent Mira

# Environment
NODE_ENV=development

# Analytics (if needed)
# NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

# Feature Flags
NEXT_PUBLIC_ENABLE_DEBUG=true
```

## Setup Script (scripts/setup.sh)
```bash
#!/bin/bash

# Agent Mira Setup Script
echo "🏠 Setting up Agent Mira..."

# Check if required tools are installed
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install $1 first."
        exit 1
    fi
}

echo "🔍 Checking required tools..."
check_command "python3"
check_command "node"
check_command "npm"
check_command "docker"
check_command "docker-compose"

# Create directories
echo "📁 Creating project directories..."
mkdir -p backend/app/{core,models,schemas,api/endpoints,services,ml,utils}
mkdir -p backend/alembic/versions
mkdir -p backend/tests/{test_api,test_services,test_utils}
mkdir -p frontend/src/{app,components/{ui,forms,property,layout},hooks,services,types,utils,styles}
mkdir -p frontend/public/images/properties
mkdir -p models
mkdir -p data
mkdir -p docs/{api,deployment,development,architecture}
mkdir -p scripts
mkdir -p infrastructure/{docker,k8s,terraform}
mkdir -p monitoring/{prometheus,grafana/dashboards,logs}

# Create placeholder files
echo "📄 Creating placeholder files..."
touch backend/app/__init__.py
touch backend/app/core/__init__.py
touch backend/app/models/__init__.py
touch backend/app/schemas/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/endpoints/__init__.py
touch backend/app/services/__init__.py
touch backend/app/ml/__init__.py
touch backend/app/utils/__init__.py
touch backend/tests/__init__.py
touch backend/tests/test_api/__init__.py
touch backend/tests/test_services/__init__.py
touch backend/tests/test_utils/__init__.py
touch frontend/src/app/globals.css
touch models/model_metadata.json
touch data/mock_properties.json
touch scripts/seed_database.py
touch monitoring/logs/.gitkeep

echo "✅ Project structure created successfully!"

# Copy configuration files
echo "📋 Setting up configuration files..."
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local

echo "🎉 Agent Mira setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and frontend/.env.local with your configuration"
echo "2. Run 'docker-compose up -d' to start services"
echo "3. Run backend setup: cd backend && pip install -r requirements.txt"
echo "4. Run frontend setup: cd frontend && npm install"
echo "5. Start development: npm run dev"
```