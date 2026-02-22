import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Tabs,
  Tab,
  Grid,
  CircularProgress,
  Button,
  Chip,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import PageHeader from '../components/common/PageHeader';
import { employeesApi } from '../api/employees';
import { Employee, EmployeeSalaryStructure, EmployeeLeaveBalance } from '../types';
import { useSnackbar } from '../context/SnackbarContext';
import { format } from 'date-fns';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => (
  <div role="tabpanel" hidden={value !== index}>
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const EmployeeDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { showError } = useSnackbar();
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [salaryStructure, setSalaryStructure] = useState<EmployeeSalaryStructure[]>([]);
  const [leaveBalance, setLeaveBalance] = useState<EmployeeLeaveBalance | null>(null);
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;

      try {
        setLoading(true);
        const empData = await employeesApi.getById(parseInt(id));
        setEmployee(empData);

        const [salaryData, leaveData] = await Promise.all([
          employeesApi.getSalaryStructure(parseInt(id)),
          employeesApi.getLeaveBalance(parseInt(id), new Date().getFullYear()),
        ]);
        setSalaryStructure(salaryData);
        setLeaveBalance(leaveData);
      } catch (error) {
        showError('Failed to load employee details');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id, showError]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!employee) {
    return (
      <Box>
        <Typography>Employee not found</Typography>
      </Box>
    );
  }

  const salaryColumns: GridColDef[] = [
    {
      field: 'salary_component',
      headerName: 'Component',
      flex: 1,
      valueGetter: (params) => params.row.salary_component?.name || 'N/A',
    },
    {
      field: 'component_type',
      headerName: 'Type',
      width: 120,
      valueGetter: (params) => params.row.salary_component?.component_type || 'N/A',
    },
    {
      field: 'amount',
      headerName: 'Amount',
      width: 150,
      valueFormatter: (params) => `₹${params.value.toLocaleString()}`,
    },
    {
      field: 'effective_from',
      headerName: 'Effective From',
      width: 150,
      valueFormatter: (params) => format(new Date(params.value), 'dd MMM yyyy'),
    },
  ];

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/employees')}
        sx={{ mb: 2 }}
      >
        Back to Employees
      </Button>

      <PageHeader
        title={`${employee.first_name} ${employee.last_name}`}
        subtitle={`Employee Code: ${employee.employee_code}`}
      />

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label="Profile" />
          <Tab label="Salary Structure" />
          <Tab label="Leave Balance" />
          <Tab label="Attendance" />
          <Tab label="Payslips" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <Card>
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Chip
                  label={employee.is_active ? 'Active' : 'Inactive'}
                  color={employee.is_active ? 'success' : 'default'}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Email
                </Typography>
                <Typography variant="body1">{employee.email || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Phone Number
                </Typography>
                <Typography variant="body1">{employee.phone || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Date of Joining
                </Typography>
                <Typography variant="body1">
                  {format(new Date(employee.date_of_joining), 'dd MMM yyyy')}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Bank Account Number
                </Typography>
                <Typography variant="body1">{employee.bank_account_number || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Bank Name
                </Typography>
                <Typography variant="body1">{employee.bank_name || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Bank IFSC Code
                </Typography>
                <Typography variant="body1">{employee.ifsc_code || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  PAN Number
                </Typography>
                <Typography variant="body1">{employee.pan_number || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  CTC
                </Typography>
                <Typography variant="body1">₹{employee.ctc.toLocaleString()}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Monthly Gross
                </Typography>
                <Typography variant="body1">₹{employee.monthly_gross.toLocaleString()}</Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box sx={{ height: 400, width: '100%' }}>
          <DataGrid
            rows={salaryStructure}
            columns={salaryColumns}
            pageSizeOptions={[10, 25]}
            initialState={{
              pagination: { paginationModel: { pageSize: 10 } },
            }}
            disableRowSelectionOnClick
          />
        </Box>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Leave Balance for {new Date().getFullYear()}
            </Typography>
            {leaveBalance ? (
              <Grid container spacing={3} sx={{ mt: 1 }}>
                <Grid item xs={6} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Paid Leaves Total
                  </Typography>
                  <Typography variant="h4">
                    {leaveBalance.paid_leaves_total}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Paid Leaves Used
                  </Typography>
                  <Typography variant="h4">
                    {leaveBalance.paid_leaves_used}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Paid Leaves Remaining
                  </Typography>
                  <Typography variant="h4">
                    {leaveBalance.paid_leaves_total - leaveBalance.paid_leaves_used}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Comp Leaves Earned
                  </Typography>
                  <Typography variant="h4">
                    {leaveBalance.comp_leaves_earned}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Comp Leaves Used
                  </Typography>
                  <Typography variant="h4">
                    {leaveBalance.comp_leaves_used}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Comp Leaves Remaining
                  </Typography>
                  <Typography variant="h4">
                    {leaveBalance.comp_leaves_earned - leaveBalance.comp_leaves_used}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Carry Forward Leaves
                  </Typography>
                  <Typography variant="h4">
                    {leaveBalance.carry_forward_leaves}
                  </Typography>
                </Grid>
              </Grid>
            ) : (
              <Typography variant="body2" color="text.secondary">
                No leave balance data available for this year.
              </Typography>
            )}
          </CardContent>
        </Card>
      </TabPanel>

      <TabPanel value={tabValue} index={3}>
        <Typography variant="body2" color="text.secondary">
          Attendance history will be displayed here.
        </Typography>
      </TabPanel>

      <TabPanel value={tabValue} index={4}>
        <Typography variant="body2" color="text.secondary">
          Employee payslips will be displayed here.
        </Typography>
      </TabPanel>
    </Box>
  );
};

export default EmployeeDetail;
