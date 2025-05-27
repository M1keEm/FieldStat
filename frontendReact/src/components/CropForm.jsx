import { useState, useEffect } from 'react';
import axios from 'axios';

const CropForm = () => {
  const [formData, setFormData] = useState({
    year: new Date().getFullYear(),
    crop: 'CHICKEN',
    group: '',
    commodity: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [groups, setGroups] = useState([]);
  const [commodities, setCommodities] = useState([]);
  const [loading, setLoading] = useState({
    groups: true,
    commodities: false
  });
  const years = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i);
  const [plotData, setPlotData] = useState(null);

  // Fetch groups on component mount
  useEffect(() => {
    axios.get('http://localhost:5000/api/groups_commodities')
      .then(res => {
        setGroups(res.data.groups || []);
        setLoading(prev => ({ ...prev, groups: false }));
      })
      .catch((error) => {
        console.error('Error fetching groups:', error);
        setLoading(prev => ({ ...prev, groups: false }));
      });
  }, []);

  // Fetch commodities when group changes
  useEffect(() => {
    // Clear commodities when group changes
    setCommodities([]);
    setFormData(prev => ({ ...prev, commodity: '' }));

    if (formData.group) {
      setLoading(prev => ({ ...prev, commodities: true }));
      axios.get(`http://localhost:5000/api/commodities_by_group?group=${encodeURIComponent(formData.group)}`)
        .then(res => {
          setCommodities(res.data.commodities || []);
          setLoading(prev => ({ ...prev, commodities: false }));
        })
        .catch((error) => {
          console.error('Error fetching commodities:', error);
          setLoading(prev => ({ ...prev, commodities: false }));
        });
    }
  }, [formData.group]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');
    try {
      // Use selected commodity instead of crop
      const saveResponse = await axios.post('http://localhost:5000/api/crops', formData);
      setMessage(`Saved data: ${saveResponse.data.message}`);
      const plotResponse = await axios.get('http://localhost:5000/crop_yield', {
        params: {
          commodity: formData.commodity, // Use commodity instead of crop
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
            disabled={loading.groups}
          >
            <option value="">Select group</option>
            {groups.map(group => (
              <option key={group} value={group}>{group}</option>
            ))}
          </select>
          {loading.groups && <span className="loading-text"> Loading...</span>}
        </div>

        <div className="form-group">
          <label htmlFor="commodity">Commodity:</label>
          <select
            id="commodity"
            name="commodity"
            value={formData.commodity}
            onChange={handleChange}
            disabled={!formData.group || loading.commodities}
          >
            <option value="">Select commodity</option>
            {commodities.map(commodity => (
              <option key={commodity} value={commodity}>{commodity}</option>
            ))}
          </select>
          {loading.commodities && <span className="loading-text"> Loading...</span>}
          {!formData.group && <span className="helper-text"> Please select a group first</span>}
        </div>

        {/*<div className="form-group">*/}
        {/*  <label htmlFor="crop">Crop:</label>*/}
        {/*  <select id="crop" name="crop" value={formData.crop} onChange={handleChange} required>*/}
        {/*    <option value="CHICKEN">Chicken</option>*/}
        {/*    <option value="CORN">Corn</option>*/}
        {/*    <option value="EGGS">Eggs</option>*/}
        {/*    <option value="OATS">Oats</option>*/}
        {/*    <option value="PEANUTS">Peanuts</option>*/}
        {/*    <option value="RICE">Rice</option>*/}
        {/*    <option value="TURKEYS">Turkey</option>*/}
        {/*  </select>*/}
        {/*</div>*/}

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Sending...' : 'Save'}
        </button>

        {message && <div className="message">{message}</div>}
      </form>
    </div>
  );
};

export default CropForm;
