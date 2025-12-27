// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import UploadMaterial from "./components/UploadMaterial";
// import QuizEvaluation from "./components/QuizEvaluation";

// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<UploadMaterial />} />
//         <Route path="/evaluation" element={<QuizEvaluation />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;


// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import UploadMaterial from "./components/UploadMaterial";
// import QuizEvaluation from "./components/QuizEvaluation";

// import WeakConcepts from "./components/WeakConcepts";
// import LearningPath from "./components/LearningPath";
// import ExamReadiness from "./components/ExamReadiness";
// import PracticeQuestions from "./components/PracticeQuestions";

// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<UploadMaterial />} />
//         <Route path="/evaluation" element={<QuizEvaluation />} />

//         {/* AGENT ROUTES */}
//         <Route path="/agent/weak" element={<WeakConcepts />} />
//         <Route path="/agent/learning-path" element={<LearningPath />} />
//         <Route path="/agent/exam-readiness" element={<ExamReadiness />} />
//         <Route path="/agent/practice-questions" element={<PracticeQuestions />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;



// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import UploadMaterial from "./components/UploadMaterial";
// import QuizEvaluation from "./components/QuizEvaluation";

// import WeakConcepts from "./components/WeakConcepts";
// import LearningPath from "./components/LearningPath";
// import ExamReadiness from "./components/ExamReadiness";
// import PracticeQuestions from "./components/PracticeQuestions";

// function App() {
//   return (
//     <Router>
//       <Routes>
//         {/* Main pages */}
//         <Route path="/" element={<UploadMaterial />} />
//         <Route path="/evaluation" element={<QuizEvaluation />} />

//         <Route path="/dashboard" element={<Dashboard />} />
//         {/* Agent pages (4 agents) */}
        
//         <Route path="/agent/weak" element={<WeakConcepts />} />
//         <Route path="/agent/learning-path" element={<LearningPath />} />
//         <Route path="/agent/exam-readiness" element={<ExamReadiness />} />
//         <Route path="/agent/practice-questions" element={<PracticeQuestions />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;


import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import UploadMaterial from "./components/UploadMaterial";
import QuizEvaluation from "./components/QuizEvaluation";

import Dashboard from "./components/Dashboard";

import WeakConcepts from "./components/WeakConcepts";
import LearningPath from "./components/LearningPath";
import ExamReadiness from "./components/ExamReadiness";
import PracticeQuestions from "./components/PracticeQuestions";

function App() {
  return (
    <Router>
      <Routes>

        {/* Main Entry Pages */}
        <Route path="/" element={<UploadMaterial />} />
        <Route path="/evaluation" element={<QuizEvaluation />} />

        {/* Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />

        {/* Agent Pages */}
        <Route path="/agent/weak" element={<WeakConcepts />} />
        <Route path="/agent/learning-path" element={<LearningPath />} />
        <Route path="/agent/exam-readiness" element={<ExamReadiness />} />
        <Route path="/agent/practice-questions" element={<PracticeQuestions />} />

      </Routes>
    </Router>
  );
}

export default App;
