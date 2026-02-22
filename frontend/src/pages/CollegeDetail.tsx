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
} from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import PageHeader from '../components/common/PageHeader';
import { collegesApi } from '../api/colleges';
import { departmentsApi } from '../api/departments';
import { employeesApi } from '../api/employees';
import { College, Department, Employee } from '../types';
import { useSnackbar } from '../context/SnackbarContext';

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

const CollegeDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { showError } = useSnackbar();
  const [college, setCollege] = useState<College | null>(null);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;

      try {
        setLoading(true);
        const collegeData = await collegesApi.getById(parseInt(id));
        setCollege(collegeData);

        const [deptData, empData] = await Promise.all([
          departmentsApi.getByCollege(parseInt(id)),
          employeesApi.getAll(0, 100, parseInt(id)),
        ]);
        setDepartments(deptData);
        setEmployees(empData);
      } catch (error) {
        showError('Failed to load college details');
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

  if (!college) {
    return (
      <Box>
        <Typography>College not found</Typography>
      </Box>
    );
  }

  const departmentColumns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Department Name', flex: 1 },
  ];

  const employeeColumns: GridColDef[] = [
    { field: 'employee_code', headerName: 'Code', width: 120 },
    { field: 'first_name', headerName: 'First Name', flex: 1 },
    { field: 'last_name', headerName: 'Last Name', flex: 1 },
    { field: 'email', headerName: 'Email', flex: 1 },
    { field: 'phone', headerName: 'Phone', width: 150 },
  ];

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/colleges')}
        sx={{ mb: 2 }}
      >
        Back to Colleges
      </Button>

      <PageHeader title={college.name} subtitle="College Details" />

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label="Information" />
          <Tab label="Departments" />
          <Tab label="Employees" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <Card>
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Serial Number
                </Typography>
                <Typography variant="body1">{college.serial_number}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  College Code
                </Typography>
                <Typography variant="body1">{college.college_code}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2" color="text.secondary">
                  Address
                </Typography>
                <Typography variant="body1">{college.address || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Created At
                </Typography>
                <Typography variant="body1">{new Date(college.created_at).toLocaleString()}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="text.secondary">
                  Updated At
                </Typography>
                <Typography variant="body1">{new Date(college.updated_at).toLocaleString()}</Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box sx={{ height: 400, width: '100%' }}>
          <DataGrid
            rows={departments}
            columns={departmentColumns}
            pageSizeOptions={[10, 25, 50]}
            initialState={{
              pagination: { paginationModel: { pageSize: 10 } },
            }}
            disableRowSelectionOnClick
          />
        </Box>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Box sx={{ height: 400, width: '100%' }}>
          <DataGrid
            rows={employees}
            columns={employeeColumns}
            pageSizeOptions={[10, 25, 50]}
            initialState={{
              pagination: { paginationModel: { pageSize: 10 } },
            }}
            disableRowSelectionOnClick
            onRowClick={(params) => navigate(`/employees/${params.id}`)}
            sx={{ cursor: 'pointer' }}
          />
        </Box>
      </TabPanel>
    </Box>
  );
};

export default CollegeDetail;
