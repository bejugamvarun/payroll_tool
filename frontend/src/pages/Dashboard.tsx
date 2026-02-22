import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  CircularProgress,
} from '@mui/material';
import {
  Business,
  People,
  AttachMoney,
  Receipt,
  Add,
  Upload,
  Calculate,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/common/PageHeader';
import { useSnackbar } from '../context/SnackbarContext';
import {
  collegesApi,
  employeesApi,
  payrollApi,
  payslipsApi,
} from '../api';
import { PayrollCycle } from '../types';

interface DashboardStats {
  totalColleges: number;
  totalEmployees: number;
  activePayrollCycles: number;
  generatedPayslips: number;
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { showError } = useSnackbar();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats>({
    totalColleges: 0,
    totalEmployees: 0,
    activePayrollCycles: 0,
    generatedPayslips: 0,
  });
  const [recentCycles, setRecentCycles] = useState<PayrollCycle[]>([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);

      const [colleges, employees, cycles, payslips] = await Promise.all([
        collegesApi.getAll(0, 1000),
        employeesApi.getAll(0, 1000),
        payrollApi.getCycles(),
        payslipsApi.getForCycle(),
      ]);

      const activeCycles = cycles.filter(
        (cycle) => cycle.status === 'DRAFT' || cycle.status === 'PROCESSING' || cycle.status === 'COMPLETED'
      );

      setStats({
        totalColleges: colleges.length,
        totalEmployees: employees.length,
        activePayrollCycles: activeCycles.length,
        generatedPayslips: payslips.length,
      });

      setRecentCycles(cycles.slice(0, 5));
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      title: 'Total Colleges',
      value: stats.totalColleges,
      icon: <Business sx={{ fontSize: 40 }} />,
      color: '#1976d2',
    },
    {
      title: 'Total Employees',
      value: stats.totalEmployees,
      icon: <People sx={{ fontSize: 40 }} />,
      color: '#2e7d32',
    },
    {
      title: 'Active Payroll Cycles',
      value: stats.activePayrollCycles,
      icon: <AttachMoney sx={{ fontSize: 40 }} />,
      color: '#ed6c02',
    },
    {
      title: 'Generated Payslips',
      value: stats.generatedPayslips,
      icon: <Receipt sx={{ fontSize: 40 }} />,
      color: '#9c27b0',
    },
  ];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <PageHeader
        title="Dashboard"
        subtitle="Overview of your payroll system"
      />

      <Grid container spacing={3} sx={{ mb: 4 }}>
        {statCards.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{ height: '100%', position: 'relative', overflow: 'visible' }}>
              <CardContent>
                <Box
                  sx={{
                    position: 'absolute',
                    top: -20,
                    left: 20,
                    bgcolor: stat.color,
                    color: 'white',
                    p: 2,
                    borderRadius: 1,
                    boxShadow: 3,
                  }}
                >
                  {stat.icon}
                </Box>
                <Box sx={{ textAlign: 'right', mt: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {stat.title}
                  </Typography>
                  <Typography variant="h4" component="div">
                    {stat.value}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Payroll Cycles
              </Typography>
              {recentCycles.length === 0 ? (
                <Typography variant="body2" color="text.secondary" sx={{ py: 2 }}>
                  No payroll cycles found. Calculate your first payroll to get started.
                </Typography>
              ) : (
                <Box sx={{ mt: 2 }}>
                  {recentCycles.map((cycle) => (
                    <Box
                      key={cycle.id}
                      sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        py: 1.5,
                        borderBottom: '1px solid',
                        borderColor: 'divider',
                        '&:last-child': { borderBottom: 'none' },
                        cursor: 'pointer',
                        '&:hover': { bgcolor: 'action.hover' },
                      }}
                      onClick={() => navigate(`/payroll/cycles/${cycle.id}`)}
                    >
                      <Box>
                        <Typography variant="body1" fontWeight="medium">
                          {cycle.college_name || `College ${cycle.college_id}`}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {new Date(cycle.year, cycle.month - 1).toLocaleDateString('en-US', {
                            month: 'long',
                            year: 'numeric',
                          })}
                        </Typography>
                      </Box>
                      <Box
                        sx={{
                          px: 2,
                          py: 0.5,
                          borderRadius: 1,
                          bgcolor:
                            cycle.status === 'LOCKED'
                              ? 'success.light'
                              : cycle.status === 'COMPLETED'
                              ? 'info.light'
                              : cycle.status === 'PROCESSING'
                              ? 'warning.light'
                              : 'grey.300',
                          color:
                            cycle.status === 'LOCKED'
                              ? 'success.dark'
                              : cycle.status === 'COMPLETED'
                              ? 'info.dark'
                              : cycle.status === 'PROCESSING'
                              ? 'warning.dark'
                              : 'grey.700',
                        }}
                      >
                        <Typography variant="body2" fontWeight="medium">
                          {cycle.status}
                        </Typography>
                      </Box>
                    </Box>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                <Button
                  variant="contained"
                  startIcon={<Add />}
                  fullWidth
                  onClick={() => navigate('/colleges')}
                >
                  Add College
                </Button>
                <Button
                  variant="contained"
                  startIcon={<Upload />}
                  fullWidth
                  color="secondary"
                  onClick={() => navigate('/attendance/upload')}
                >
                  Upload Attendance
                </Button>
                <Button
                  variant="contained"
                  startIcon={<Calculate />}
                  fullWidth
                  color="success"
                  onClick={() => navigate('/payroll')}
                >
                  Calculate Payroll
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
