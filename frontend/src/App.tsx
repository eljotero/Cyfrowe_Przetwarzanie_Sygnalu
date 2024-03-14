import { Route, Routes, BrowserRouter } from 'react-router-dom';
import MainPage from './components/MainPage.tsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<MainPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
