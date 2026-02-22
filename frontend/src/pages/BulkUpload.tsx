import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  LinearProgress,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon, CloudUpload as UploadIcon } from '@mui/icons-material';
import PageHeader from '../components/common/PageHeader';
import { employeesApi } from '../api/employees';
import { collegesApi } from '../api/colleges';
import { College } from '../types';
import { useSnackbar } from '../context/SnackbarContext';
import { useEffect } from 'react';

const BulkUpload: React.FC = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useSnackbar();
  const [colleges, setColleges] = useState<College[]>([]);
  const [selectedCollege, setSelectedCollege] = useState<number>(0);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{ success: number; errors: string[] } | null>(null);

  useEffect(() => {
    const fetchColleges = async () => {
      try {
        const data = await collegesApi.getAll();
        setColleges(data);
        if (data.length > 0) {
          setSelectedCollege(data[0].id);
        }
      } catch (error) {
        showError('Failed to load colleges');
        console.error(error);
      }
    };
    fetchColleges();
  }, [showError]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setUploadResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file || !selectedCollege) {
      showError('Please select a college and file');
      return;
    }

    try {
      setUploading(true);
      const result = await employeesApi.bulkUpload(file, selectedCollege);
      setUploadResult(result);
      showSuccess(`Successfully uploaded ${result.success} employees`);
      if (result.errors.length === 0) {
        setTimeout(() => navigate('/employees'), 2000);
      }
    } catch (error) {
      showError('Failed to upload employees');
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

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
        title="Bulk Employee Upload"
        subtitle="Upload multiple employees using Excel file"
      />

      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Alert severity="info">
              Upload an Excel file (.xlsx, .xls) with employee data. Required columns: employee_code,
              first_name, last_name, date_of_joining, ctc, monthly_gross, college_id, department_id, designation_id.
              Optional columns: email, phone, bank_name, bank_account_number, ifsc_code, pan_number.
            </Alert>

            <FormControl fullWidth>
              <InputLabel>Select College</InputLabel>
              <Select
                value={selectedCollege}
                label="Select College"
                onChange={(e) => setSelectedCollege(e.target.value as number)}
              >
                {colleges.map((college) => (
                  <MenuItem key={college.id} value={college.id}>
                    {college.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Box>
              <input
                accept=".xlsx,.xls"
                style={{ display: 'none' }}
                id="file-upload"
                type="file"
                onChange={handleFileChange}
              />
              <label htmlFor="file-upload">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<UploadIcon />}
                  fullWidth
                  sx={{ py: 2 }}
                >
                  {file ? file.name : 'Choose Excel File'}
                </Button>
              </label>
            </Box>

            {uploading && (
              <Box>
                <Typography variant="body2" gutterBottom>
                  Uploading...
                </Typography>
                <LinearProgress />
              </Box>
            )}

            {uploadResult && (
              <Box>
                <Alert severity={uploadResult.errors.length === 0 ? 'success' : 'warning'}>
                  <Typography variant="body2">
                    Successfully uploaded: {uploadResult.success} employees
                  </Typography>
                  {uploadResult.errors.length > 0 && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="body2" fontWeight="bold">
                        Errors:
                      </Typography>
                      {uploadResult.errors.map((error, index) => (
                        <Typography key={index} variant="caption" display="block">
                          • {error}
                        </Typography>
                      ))}
                    </Box>
                  )}
                </Alert>
              </Box>
            )}

            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!file || !selectedCollege || uploading}
              size="large"
            >
              Upload Employees
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default BulkUpload;
