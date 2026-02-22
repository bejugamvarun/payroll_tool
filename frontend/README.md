# Payroll Management System - Frontend

A modern React-based frontend for the Payroll Management System, built with Vite, TypeScript, and Material UI.

## Tech Stack

- **Framework**: React 18.2+ with TypeScript
- **Build Tool**: Vite 5
- **UI Library**: Material UI (MUI) v5
- **Routing**: React Router v6
- **Data Grid**: MUI X Data Grid
- **HTTP Client**: Axios
- **Date Utilities**: date-fns

## Features

### Management
- **Colleges**: Create, edit, view, and delete college institutions
- **Employees**: Comprehensive employee management with bulk upload support
- **Salary Components**: Configure earnings and deductions

### Configuration
- **Leave Policies**: Define leave allocation rules
- **Holidays**: Manage holiday calendar

### Operations
- **Attendance**: Upload and track monthly attendance
- **Payroll**: Calculate and process payroll cycles
- **Payslips**: Generate and download employee payslips
- **Reports**: Generate various payroll reports

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API client modules
│   │   ├── client.ts     # Axios instance
│   │   ├── colleges.ts
│   │   ├── employees.ts
│   │   ├── salaryComponents.ts
│   │   ├── leavePolicies.ts
│   │   ├── attendance.ts
│   │   ├── holidays.ts
│   │   ├── payroll.ts
│   │   ├── payslips.ts
│   │   └── reports.ts
│   ├── components/
│   │   └── common/       # Shared components
│   │       ├── Layout.tsx
│   │       └── PageHeader.tsx
│   ├── context/          # React context providers
│   │   └── SnackbarContext.tsx
│   ├── pages/            # Page components
│   │   ├── Dashboard.tsx
│   │   ├── CollegeList.tsx
│   │   ├── CollegeDetail.tsx
│   │   ├── EmployeeList.tsx
│   │   ├── EmployeeDetail.tsx
│   │   ├── BulkUpload.tsx
│   │   ├── SalaryComponents.tsx
│   │   ├── LeavePolicies.tsx
│   │   ├── Holidays.tsx
│   │   ├── AttendanceUpload.tsx
│   │   ├── PayrollDashboard.tsx
│   │   ├── PayrollCycleDetail.tsx
│   │   ├── PayslipList.tsx
│   │   └── Reports.tsx
│   ├── types/            # TypeScript type definitions
│   │   └── index.ts
│   ├── App.tsx           # Main app component with routing
│   ├── main.tsx          # Entry point
│   └── index.css         # Global styles
├── Dockerfile            # Docker configuration
├── vite.config.ts        # Vite configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Dependencies
```

## Getting Started

### Prerequisites

- Node.js 20+
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The build output will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Docker

### Build Docker Image

```bash
docker build -t payroll-frontend .
```

### Run Docker Container

```bash
docker run -p 5173:5173 payroll-frontend
```

## API Configuration

The frontend is configured to proxy API requests to `http://localhost:8000`. This is set in `vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

Update this configuration if your backend runs on a different host/port.

## Development Guidelines

### Component Architecture

- All components are functional components using React hooks
- TypeScript is mandatory for all new components
- Use Material UI components consistently
- Follow the existing folder structure

### API Integration

- All API calls are centralized in `src/api/` modules
- Use the Snackbar context for user notifications
- Handle loading states with CircularProgress or Skeleton components
- Always wrap API calls in try-catch blocks

### Styling

- Use MUI's `sx` prop for component-specific styling
- Maintain consistent spacing using theme.spacing()
- Follow the established color palette and typography

### Forms

- Use controlled components with state management
- Implement proper validation
- Show inline error messages
- Display loading states on submit buttons
- Show success/error notifications after operations

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Proprietary - All rights reserved
