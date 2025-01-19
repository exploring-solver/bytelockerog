import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import SecurityView from './pages/SecurityView';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import Layout from './components/layout/Layout';
import VLMInterface from './components/vlm/VLMInterface';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="security" element={<SecurityView />} />
          <Route path="vlm" element={<VLMInterface />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="settings" element={<Settings />} />
          <Route path="*" element={<Dashboard />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;