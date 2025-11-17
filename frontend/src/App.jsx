import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UploadMaterial from "./components/UploadMaterial";
import QuizEvaluation from "./components/QuizEvaluation";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadMaterial />} />
        <Route path="/evaluation" element={<QuizEvaluation />} />
      </Routes>
    </Router>
  );
}

export default App;
