import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { WebLayout } from './components/layout/WebLayout';
import { AlertFeed } from './pages/AlertFeed';
import { Profile } from './pages/Profile';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<WebLayout />}>
          <Route index element={<Navigate to="/alerts" replace />} />
          <Route path="alerts" element={<AlertFeed />} />
          <Route path="profile" element={<Profile />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
