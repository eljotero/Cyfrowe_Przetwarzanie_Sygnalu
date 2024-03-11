import { Route, Routes, BrowserRouter } from 'react-router-dom';
import MainPage from './components/MainPage.tsx';
import Chart from './components/Chart.tsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<MainPage />} />
        <Route path='/chart/:data' element={<Chart />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
