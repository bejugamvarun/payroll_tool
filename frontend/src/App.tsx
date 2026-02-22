import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Layout from './components/common/Layout';
import Dashboard from './pages/Dashboard';
import CollegeList from './pages/CollegeList';
import CollegeDetail from './pages/CollegeDetail';
import EmployeeList from './pages/EmployeeList';
import EmployeeDetail from './pages/EmployeeDetail';
import BulkUpload from './pages/BulkUpload';
import SalaryComponents from './pages/SalaryComponents';
import LeavePolicies from './pages/LeavePolicies';
import Holidays from './pages/Holidays';
import AttendanceUpload from './pages/AttendanceUpload';
import PayrollDashboard from './pages/PayrollDashboard';
import PayrollCycleDetail from './pages/PayrollCycleDetail';
import PayslipList from './pages/PayslipList';
import Reports from './pages/Reports';

// Create a professional theme for the payroll application
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
      contrastText: '#fff',
    },
    secondary: {
      main: '#9c27b0',
      light: '#ba68c8',
      dark: '#7b1fa2',
      contrastText: '#fff',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="colleges" element={<CollegeList />} />
          <Route path="colleges/:id" element={<CollegeDetail />} />
          <Route path="employees" element={<EmployeeList />} />
          <Route path="employees/:id" element={<EmployeeDetail />} />
          <Route path="employees/bulk-upload" element={<BulkUpload />} />
          <Route path="salary-components" element={<SalaryComponents />} />
          <Route path="leave-policies" element={<LeavePolicies />} />
          <Route path="holidays" element={<Holidays />} />
          <Route path="attendance" element={<AttendanceUpload />} />
          <Route path="payroll" element={<PayrollDashboard />} />
          <Route path="payroll/:cycleId" element={<PayrollCycleDetail />} />
          <Route path="payslips" element={<PayslipList />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
};

export default App;
