import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./components/Dashboard";
import SubjectList from "./components/SubjectList";
import LogList from "./components/LogList";
import AddSubjectForm from "./components/SubjectForm";
import LogForm from "./components/LogForm";
function App() {

  return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />


          <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/dashboard/:id" element={<Dashboard  />} />
            <Route path="/subjects/:userId" element={<SubjectList />} />
           <Route path="/subjects/:userId/:subjectId" element={<LogList />} />
            <Route path="/add_subject/:userId" element={<AddSubjectForm />} />
            <Route path="/logs/:userId/:subjectId" element={<LogForm />} />
        </Routes>
      </Router>
  );
}

export default App;
