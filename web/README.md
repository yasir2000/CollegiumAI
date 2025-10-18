# CollegiumAI Web Platform

A comprehensive React-based web platform for the CollegiumAI AI Multi-Agent Collaborative Framework designed for Digital Universities.

## Features

### 🎨 Modern UI/UX
- **Material-UI Design System**: Consistent, professional interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Theme Support**: Customizable themes for user preference
- **Accessibility**: WCAG 2.1 compliant interface components

### 🔐 Authentication & Authorization
- **JWT-based Authentication**: Secure token-based auth system
- **Role-based Access Control**: Student, Faculty, Staff, and Admin roles
- **Session Management**: Persistent login with secure token handling
- **Multi-institution Support**: Support for multiple university contexts

### 🤖 AI Agent Interface
- **Interactive Chat Interface**: Real-time conversations with AI agents
- **Multi-session Management**: Handle multiple agent conversations
- **Specialized Agents**: 
  - Academic Advisor
  - Student Services
  - Bologna Process Specialist
  - Admissions Assistant
  - Career Services
  - Research Assistant
- **Agent Context Awareness**: Agents understand university-specific contexts

### 🏛️ University Management
- **Dashboard Overview**: Key metrics and real-time statistics
- **Student Management**: Enrollment, progress tracking, services
- **Faculty Management**: Staff directory, roles, permissions
- **Program Management**: Academic programs, courses, requirements

### ⛓️ Blockchain Integration
- **Credential Management**: Issue, verify, and track digital credentials
- **Smart Contract Interface**: Direct interaction with blockchain contracts
- **Network Status**: Real-time blockchain network monitoring
- **Transaction History**: Complete audit trail of all operations

### 🏆 Governance Compliance
- **Multi-framework Support**: AACSB, HEFCE, WASC, QAA, Bologna Process
- **Compliance Monitoring**: Real-time compliance status tracking
- **Audit Management**: Schedule, conduct, and track compliance audits
- **Reporting Dashboard**: Comprehensive compliance reporting

### 🇪🇺 Bologna Process Integration
- **ECTS Credit Management**: European Credit Transfer System support
- **Mobility Programs**: Erasmus+ and other exchange program management
- **Automatic Recognition**: AI-powered credential recognition
- **EQF Mapping**: European Qualifications Framework integration
- **Quality Assurance**: ESG standards compliance monitoring

## Technology Stack

### Frontend
- **React 18**: Modern React with hooks and functional components
- **TypeScript**: Type-safe development
- **Material-UI (MUI)**: Professional UI component library
- **React Router**: Client-side routing
- **Redux Toolkit**: State management
- **React Query**: Server state management and caching

### Development Tools
- **Vite**: Fast build tool and development server
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting
- **Formik + Yup**: Form handling and validation

### Charts & Visualization
- **Recharts**: Interactive charts and data visualization
- **Date-fns**: Date manipulation and formatting

## Getting Started

### Prerequisites
- Node.js 16+ and npm
- CollegiumAI API server running on port 4000

### Installation

1. **Install dependencies**:
   ```bash
   cd web
   npm install
   ```

2. **Environment setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

4. **Build for production**:
   ```bash
   npm run build
   ```

## Project Structure

```
web/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── layout/        # Layout components
│   │   ├── common/        # Shared components
│   │   └── forms/         # Form components
│   ├── pages/             # Page components
│   │   ├── auth/          # Authentication pages
│   │   ├── dashboard/     # Dashboard pages
│   │   ├── agents/        # AI agent interface
│   │   ├── blockchain/    # Blockchain management
│   │   ├── governance/    # Compliance management
│   │   ├── bologna/       # Bologna Process pages
│   │   ├── students/      # Student management
│   │   ├── faculty/       # Faculty management
│   │   └── credentials/   # Credential management
│   ├── store/             # Redux store and slices
│   │   └── features/      # Feature-based state slices
│   ├── hooks/             # Custom React hooks
│   ├── utils/             # Utility functions
│   ├── types/             # TypeScript type definitions
│   └── services/          # API service layer
├── package.json           # Dependencies and scripts
└── tsconfig.json         # TypeScript configuration
```

## Key Features Implementation

### Authentication Flow
```typescript
// Login with JWT tokens
const loginResult = await dispatch(loginUser({ email, password }));
if (loginUser.fulfilled.match(loginResult)) {
  navigate('/dashboard');
}
```

### AI Agent Communication
```typescript
// Send message to AI agent
dispatch(addMessage({
  sessionId: activeSessionId,
  message: {
    type: 'user',
    content: messageText,
    timestamp: new Date(),
  },
}));
```

### Blockchain Integration
```typescript
// Issue new credential on blockchain
const result = await client.blockchain.issueCredential({
  studentData: { studentId, blockchainAddress, name, email },
  credentialData: { title, program, degree, grade, graduationDate },
  governanceFrameworks: ['AACSB', 'BOLOGNA_PROCESS']
});
```

### Bologna Process Management
```typescript
// Set Bologna Process compliance
await client.blockchain.setBolognaCompliance({
  credentialId: 12345,
  ectsCredits: 120,
  eqfLevel: 7,
  diplomaSupplementIssued: true,
  learningOutcomes: [...],
  qualityAssuranceAgency: "AQ Austria"
});
```

## Development Commands

```bash
# Start development server
npm start

# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint

# Format code
npm run format

# Type checking
npm run type-check
```

## Configuration

### Environment Variables
```env
REACT_APP_API_BASE_URL=http://localhost:4000/api/v1
REACT_APP_BLOCKCHAIN_ENABLED=true
REACT_APP_DEBUG=false
```

### API Integration
The web platform integrates with the CollegiumAI API server:
- **Authentication**: `/auth/login`, `/auth/me`
- **Agents**: `/api/v1/agents/{type}/query`
- **Blockchain**: `/api/v1/blockchain/credentials/*`
- **Governance**: `/api/v1/governance/audits`
- **Bologna Process**: `/api/v1/blockchain/credentials/bologna/*`

## User Roles & Permissions

### Student Role
- View personal dashboard and credentials
- Chat with AI agents for academic support
- Access Bologna Process mobility information
- View compliance status

### Faculty Role
- Manage courses and student records
- Access research assistant AI agent
- Issue and verify credentials
- View departmental compliance reports

### Staff Role
- Manage student services
- Access administrative AI agents
- Handle admissions and enrollment
- Manage institutional data

### Admin Role
- Full system access and configuration
- Governance and compliance management
- Blockchain network administration
- User and role management

## Browser Support

- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

## Contributing

1. Follow the existing code style and TypeScript conventions
2. Use Material-UI components and design patterns
3. Write tests for new functionality
4. Update documentation for new features

## License

Part of the CollegiumAI Framework - See main project LICENSE for details.