import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Papers from './pages/Papers';
import PaperDetail from './pages/PaperDetail';
import Authors from './pages/Authors';
import AuthorDetail from './pages/AuthorDetail';
import Institutions from './pages/Institutions';
import InstitutionDetail from './pages/InstitutionDetail';
import Topics from './pages/Topics';
import Explore from './pages/Explore';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="papers" element={<Papers />} />
        <Route path="papers/:id" element={<PaperDetail />} />
        <Route path="authors" element={<Authors />} />
        <Route path="authors/:id" element={<AuthorDetail />} />
        <Route path="institutions" element={<Institutions />} />
        <Route path="institutions/:id" element={<InstitutionDetail />} />
        <Route path="topics" element={<Topics />} />
        <Route path="explore" element={<Explore />} />
      </Route>
    </Routes>
  );
}
