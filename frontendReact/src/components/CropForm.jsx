import { useState, useEffect } from 'react';
import axios from 'axios';
import CropCharts from './CropCharts';

// Predefined static data for groups and commodities
const Formgroups = [
  { value: 'FIELDCROPS', label: 'FIELD CROPS' },
  { value: 'FRUIT&TREENUTS', label: 'FRUIT & TREE NUTS' },
  { value: 'VEGETABLES', label: 'VEGETABLES' }
];

const crops = [
  { value: 'BARLEY', label: 'BARLEY' },
  { value: 'BEANS', label: 'BEANS' },
  { value: 'CANOLA', label: 'CANOLA' },
  { value: 'CHICKPEAS', label: 'CHICKPEAS' },
  { value: 'CORN', label: 'CORN' },
  { value: 'COTTON', label: 'COTTON' },
  { value: 'FLAXSEED', label: 'FLAXSEED' },
  { value: 'HAY', label: 'HAY' },
  { value: 'HAY & HAYLAGE', label: 'HAY & HAYLAGE' },
  { value: 'HAYLAGE', label: 'HAYLAGE' },
  { value: 'HEMP', label: 'HEMP' },
  { value: 'HOPS', label: 'HOPS' },
  { value: 'LEGUMES', label: 'LEGUMES' },
  { value: 'LENTILS', label: 'LENTILS' },
  { value: 'MAPLE SYRUP', label: 'MAPLE SYRUP' },
  { value: 'MILLET', label: 'MILLET' },
  { value: 'MINT', label: 'MINT' },
  { value: 'MUSTARD', label: 'MUSTARD' },
  { value: 'OATS', label: 'OATS' },
  { value: 'PEANUTS', label: 'PEANUTS' },
  { value: 'PEAS', label: 'PEAS' },
  { value: 'RAPESEED', label: 'RAPESEED' },
  { value: 'RICE', label: 'RICE' },
  { value: 'RYE', label: 'RYE' },
  { value: 'SUGARBEETS', label: 'SUGARBEETS' },
  { value: 'SUGARCANE', label: 'SUGARCANE' }
];

const vegetables = [
  { value: 'ARTICHOKES', label: 'ARTICHOKES' },
  { value: 'ASPARAGUS', label: 'ASPARAGUS' },
  { value: 'BEANS', label: 'BEANS' },
  { value: 'BEETS', label: 'BEETS' },
  { value: 'BROCCOLI', label: 'BROCCOLI' },
  { value: 'CABBAGE', label: 'CABBAGE' },
  { value: 'CARROTS', label: 'CARROTS' },
  { value: 'CAULIFLOWER', label: 'CAULIFLOWER' },
  { value: 'CELERY', label: 'CELERY' }
];

const fruit = [
  { value: 'CHERRIES', label: 'CHERRIES' },
  { value: 'COFFEE', label: 'COFFEE' },
  { value: 'DATES', label: 'DATES' },
  { value: 'GRAPEFRUIT', label: 'GRAPEFRUIT' },
  { value: 'GRAPES', label: 'GRAPES' },
  { value: 'LEMONS', label: 'LEMONS' },
  { value: 'OLIVES', label: 'OLIVES' },
  { value: 'PAPAYAS', label: 'PAPAYAS' },
  { value: 'PEACHES', label: 'PEACHES' }
];

// Map group values to their respective commodity lists
const commoditiesByGroup = {
  'FIELDCROPS': crops,
  'FRUIT&TREENUTS': fruit,
  'VEGETABLES': vegetables
};

const CropForm = () => {
  const [formData, setFormData] = useState({
    year: new Date().getFullYear(),
    group: '',
    commodity: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [commodities, setCommodities] = useState([]);
  const years = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i);
  const [plotData, setPlotData] = useState(null);

  // Update commodities when group changes
  useEffect(() => {
    if (formData.group) {
      setCommodities(commoditiesByGroup[formData.group] || []);
    } else {
      setCommodities([]);
    }
    // Reset commodity when group changes
    setFormData(prev => ({ ...prev, commodity: '' }));
  }, [formData.group]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.commodity) {
      setMessage('Please select a commodity');
      return;
    }

    setIsSubmitting(true);
    setMessage('');
    try {
      const saveResponse = await axios.post('http://localhost:5000/api/crops', formData);
      setMessage(`Saved data: ${saveResponse.data.message}`);
      const plotResponse = await axios.get('http://localhost:5000/crop_yield', {
        params: {
          commodity: formData.commodity,
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
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <>
      <div className="crop-form">
        <h2>Choose Crop Data</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="year">Year:</label>
            <select id="year" name="year" value={formData.year} onChange={handleChange} required>
              {years.map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="group">Group:</label>
            <select
              id="group"
              name="group"
              value={formData.group}
              onChange={handleChange}
            >
              <option value="">Select group</option>
              {Formgroups.map(group => (
                <option key={group.value} value={group.value}>{group.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="commodity">Commodity:</label>
            <select
              id="commodity"
              name="commodity"
              value={formData.commodity}
              onChange={handleChange}
              disabled={!formData.group}
            >
              <option value="">Select commodity</option>
              {commodities.map(commodity => (
                <option key={commodity.value} value={commodity.value}>{commodity.label}</option>
              ))}
            </select>
            {!formData.group && <span className="helper-text"> Please select a group first</span>}
          </div>

          <button type="submit" disabled={isSubmitting || !formData.commodity}>
            {isSubmitting ? 'Sending...' : 'Save'}
          </button>

          {message && <div className="message">{message}</div>}
        </form>
      </div>

      {plotData && (
        <CropCharts
          plotData={plotData}
          commodity={formData.commodity}
          year={formData.year}
        />
      )}
    </>
  );
};

export default CropForm;
