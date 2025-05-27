import { useState } from 'react';
import axios from 'axios';

const CropForm = () => {
  const [formData, setFormData] = useState({
    year: new Date().getFullYear(),
    crop: 'Chicken'
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  const crops = [
    { value: 'CHICKEN', label: 'Chicken' },
    { value: 'CORN', label: 'Corn' },
    { value: 'EGGS', label: 'Eggs' },
    { value: 'OATS', label: 'Oats' },
    { value: 'PEANUTS', label: 'Peanuts' },
    { value: 'RICE', label: 'Rice' },
    { value: 'TURKEYS', label: 'Turkey' }
  ];

  const years = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i);

const [plotData, setPlotData] = useState(null);


  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');

    try {
    // 1. Zapisz dane
    const saveResponse = await axios.post('http://localhost:5000/api/crops', formData);
    setMessage(`Saved data: ${saveResponse.data.message}`);

    // 2. Pobierz dane do wykresu
    const plotResponse = await axios.get('http://localhost:5000/crop_yield', {
      params: {
        commodity: formData.crop,
        year: formData.year
      }
    });

    setPlotData(plotResponse.data.data);

  } catch (error) {
    setMessage(`Error: ${error.response?.data?.error || error.message}`);
    if (error.code === 'ECONNABORTED') {
      setMessage('Request timeout - try again later');
    }
  } finally {
    setIsSubmitting(false);
  }
    // try {
    //   const response = await axios.post('http://localhost:5000/api/crops', formData);
    //   setMessage(`Saved data: ${response.data.message}`);
    // } catch (error) {
    //   setMessage(`Erorr: ${error.response?.data?.error || error.message}`);
    // } finally {
    //   setIsSubmitting(false);
    // }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="crop-form">
      <h2>Choose Crop Data</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="year">Year:</label>
          <select
            id="year"
            name="year"
            value={formData.year}
            onChange={handleChange}
            required
          >
            {years.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="crop">Crop:</label>
          <select
            id="crop"
            name="crop"
            value={formData.crop}
            onChange={handleChange}
            required
          >
            {crops.map(crop => (
              <option key={crop.value} value={crop.value}>{crop.label}</option>
            ))}
          </select>
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Sending...' : 'Save'}
        </button>

        {message && <div className="message">{message}</div>}
      </form>
    </div>
  );
};

export default CropForm;
