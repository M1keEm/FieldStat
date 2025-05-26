import { useState } from 'react';
import axios from 'axios';
import CropForm from './components/CropForm';


function App() {
  const [data, setData] = useState(null);

  // const fetchData = async () => {
  //   try {
  //     const response = await axios.get('http://localhost:5000/api/data');
  //     setData(response.data);
  //   } catch (error) {
  //     console.error('Error fetching data:', error);
  //   }
  // };

  return (
    <div className="App">
      <h1>Form</h1>
      {/* <button onClick={fetchData}>Get Data from Flask</button>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>} */}
      <CropForm />
    </div>
  );
}

export default App;